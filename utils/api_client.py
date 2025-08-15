# utils/api_client.py
import os, tempfile, requests, hashlib, json, time
import concurrent.futures
from typing import Iterable, Dict, Any


def _env(name: str, default: str) -> str:
    # Docker compose exports *_AGENT_URL. Local may not.
    return os.getenv(name) or default


AUDIO_URL = _env("AUDIO_AGENT_URL", "http://localhost:8000")
MOOD_URL = _env("MOOD_AGENT_URL", "http://localhost:8001")
# Increase timeout for larger uploads and allow retries on transient failures
TIMEOUT_S = int(_env("MOODMIXR_TIMEOUT_S", "300"))
RETRIES = int(_env("MOODMIXR_RETRIES", "3"))
BACKOFF_FACTOR = float(_env("MOODMIXR_BACKOFF", "1.0"))


def ping_agents() -> Dict[str, Any]:
    out = {}
    for n, u in {"audio": AUDIO_URL, "mood": MOOD_URL}.items():
        try:
            r = requests.get(f"{u}/ping", timeout=5)
            out[n] = {"ok": r.ok, "status": r.status_code, "url": f"{u}/ping"}
        except requests.exceptions.RequestException as e:
            out[n] = {"ok": False, "error": str(e), "url": f"{u}/ping"}
    return out


def _post_file(url: str, path: str) -> Dict[str, Any]:
    """POST a file with a small retry/backoff loop and return parsed JSON or error dict."""
    last_exc = None
    for attempt in range(1, RETRIES + 1):
        try:
            with open(path, "rb") as f:
                files = {
                    "file": (os.path.basename(path), f, "application/octet-stream")
                }
                r = requests.post(url, files=files, timeout=TIMEOUT_S)

            # raise for HTTP errors so callers see 4xx/5xx details
            r.raise_for_status()

            # attempt to parse JSON
            try:
                return r.json()
            except ValueError as e:
                return {"error": f"invalid-json: {e}", "raw": r.text}

        except FileNotFoundError as e:
            return {"error": f"file-not-found: {e}"}
        except requests.exceptions.RequestException as e:
            last_exc = e
            # If this was the last attempt, return the error. Otherwise backoff and retry.
            if attempt == RETRIES:
                return {"error": str(e)}
            backoff = BACKOFF_FACTOR * (2 ** (attempt - 1))
            time.sleep(backoff)

    # Should not reach here, but return last exception if so
    return {"error": str(last_exc) if last_exc is not None else "unknown-error"}


def analyze_audio_file(path: str) -> Dict[str, Any]:
    # tolerant alias; your agents also expose /analyze
    try:
        return _post_file(f"{AUDIO_URL}/audio", path)
    except FileNotFoundError as e:
        return {"error": f"file-not-found: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def analyze_mood_file(path: str) -> Dict[str, Any]:
    try:
        return _post_file(f"{MOOD_URL}/mood", path)
    except FileNotFoundError as e:
        return {"error": f"file-not-found: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def analyze_batch(files: Iterable[bytes], names: Iterable[str], on_progress=None):
    """
    Parallelized analyze_batch: write temp files, reuse cache when available, and run agent calls
    concurrently to reduce wall time for multi-file uploads. Returns a list of items preserving
    input order.
    """
    results = [None] * len(list(names))
    # Prepare cache directory (per-repo) to avoid re-analyzing identical uploads
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cache_dir = os.path.join(repo_root, "data", "analysis_cache")
    os.makedirs(cache_dir, exist_ok=True)

    # Build a list of entries to process and handle cached items immediately
    entries = []
    # We need to iterate files and names together but also know index; convert to list
    file_list = list(files)
    name_list = list(names)

    for idx, (blob, name) in enumerate(zip(file_list, name_list), start=1):
        try:
            b = bytes(blob)
        except Exception:
            b = blob.tobytes() if hasattr(blob, "tobytes") else blob

        sha = hashlib.sha1(b).hexdigest()
        cache_path = os.path.join(cache_dir, f"{sha}.json")

        # Persist to temp file (agents expect a filesystem path)
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(name)[-1]
        ) as tmp:
            tmp.write(b)
            tmp_path = tmp.name

        # Fast-path: if cache exists reuse and skip agent calls
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as cf:
                    cached = json.load(cf)
                    item = {
                        "name": name,
                        "ok": True,
                        "audio": cached.get("audio"),
                        "mood": cached.get("mood"),
                        "merged": cached.get("merged"),
                    }
                    results[idx - 1] = item
                    if on_progress:
                        on_progress(idx, name, item)
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass
                    continue
            except Exception:
                # cache read failed; fallthrough to re-analyze
                pass

        # collect for parallel processing
        entries.append(
            {"idx": idx, "name": name, "tmp_path": tmp_path, "cache_path": cache_path}
        )

    # Worker function for a single file entry
    def _process_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
        idx = entry["idx"]
        name = entry["name"]
        tmp_path = entry["tmp_path"]
        cache_path = entry["cache_path"]

        item = {"name": name, "ok": False, "audio": None, "mood": None, "merged": None}
        try:
            audio = analyze_audio_file(tmp_path)
            item["audio"] = audio
        except Exception as e:
            item["audio"] = {"ok": False, "error": str(e)}

        try:
            mood = analyze_mood_file(tmp_path)
            item["mood"] = mood
        except Exception as e:
            item["mood"] = {"ok": False, "error": str(e)}

        # Merge audio + mood dicts if present
        merged = {}
        for src in (item.get("audio") or {}, item.get("mood") or {}):
            if isinstance(src, dict):
                merged.update(src)

        merged.setdefault("bpm", None)
        merged.setdefault("key", None)
        merged.setdefault("energy", None)
        merged.setdefault(
            "mood", merged.get("mood_label") or merged.get("emotion") or None
        )

        # normalization helper (same logic as prior implementation)
        def _normalize_merged(m: Dict[str, Any]) -> Dict[str, Any]:
            NOTE_NAMES = [
                "C",
                "C#",
                "D",
                "D#",
                "E",
                "F",
                "F#",
                "G",
                "G#",
                "A",
                "A#",
                "B",
            ]
            out = dict(m)

            # BPM
            bpm_val = out.get("bpm")
            try:
                if bpm_val is None:
                    bpm_num = None
                else:
                    bpm_num = float(bpm_val)
                    if bpm_num <= 0:
                        bpm_num = None
                out["bpm"] = bpm_num
            except (ValueError, TypeError):
                out["bpm"] = None

            # Key
            key_val = out.get("key") or out.get("Key") or out.get("key_label")
            if key_val is None:
                out["key"] = None
            else:
                try:
                    if isinstance(key_val, (int, float)):
                        idxn = int(key_val) % 12
                        out["key"] = NOTE_NAMES[idxn]
                    else:
                        out["key"] = str(key_val).strip()
                except (ValueError, TypeError, IndexError):
                    out["key"] = None

            # Energy
            energy_val = out.get("energy")
            try:
                if energy_val is None:
                    out["energy"] = None
                else:
                    e = float(energy_val)
                    if e <= 0:
                        out["energy"] = None
                    elif e <= 1:
                        out["energy"] = round(e, 3)
                    else:
                        if e <= 10:
                            out["energy"] = round(e / 10.0, 3)
                        elif e <= 100:
                            out["energy"] = round(e / 100.0, 3)
                        else:
                            out["energy"] = round(min(e / 1000.0, 1.0), 3)
            except (ValueError, TypeError):
                out["energy"] = None

            # Mood
            mood_val = (
                out.get("mood")
                or out.get("mood_label")
                or out.get("label")
                or out.get("emotion")
            )
            if isinstance(mood_val, dict):
                mood_label = mood_val.get("label") or mood_val.get("mood")
            else:
                mood_label = mood_val
            out["mood"] = (
                str(mood_label).capitalize() if mood_label is not None else None
            )

            return out

        merged = _normalize_merged(merged)
        item["merged"] = merged
        item["ok"] = not any(
            [
                isinstance(item.get("audio"), dict) and item.get("audio").get("error"),
                isinstance(item.get("mood"), dict) and item.get("mood").get("error"),
            ]
        )

        # Persist to cache
        try:
            to_cache = {
                "audio": item.get("audio"),
                "mood": item.get("mood"),
                "merged": item.get("merged"),
            }
            with open(cache_path, "w", encoding="utf-8") as cf:
                json.dump(to_cache, cf)
        except Exception:
            pass

        # Cleanup temp file
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

        return (idx, item)

    # Run parallel processing
    if entries:
        max_workers = min(8, (os.cpu_count() or 1) * 2)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(_process_entry, e) for e in entries]
            for fut in concurrent.futures.as_completed(futures):
                try:
                    idx, item = fut.result()
                    results[idx - 1] = item
                    if on_progress:
                        on_progress(idx, item.get("name"), item)
                except Exception as e:
                    # best-effort: record a failure item
                    # locate which future failed (best-effort)
                    try:
                        failed_idx = None
                        # attempt to access fut._args (not guaranteed); fallback to -1
                    except Exception:
                        failed_idx = -1
                    failure_item = {
                        "name": getattr(e, "name", "unknown"),
                        "ok": False,
                        "audio": {"error": str(e)},
                        "mood": None,
                        "merged": None,
                    }
                    if failed_idx and 1 <= failed_idx <= len(results):
                        results[failed_idx - 1] = failure_item
                    else:
                        # append to the end if we cannot determine index
                        results.append(failure_item)

    # Final sanity: ensure every slot is populated (convert None to minimal item)
    for i in range(len(results)):
        if results[i] is None:
            results[i] = {
                "name": name_list[i],
                "ok": False,
                "audio": None,
                "mood": None,
                "merged": {"bpm": None, "key": None, "energy": None, "mood": None},
            }

    return results


# utils/api_client.py — replace these two functions


def call_mood_agent_api(path: str) -> Dict[str, Any]:
    """Send a single file to the mood agent's /analyze endpoint (multipart/form-data)."""
    return _post_file(f"{MOOD_URL}/analyze", path)


def call_audio_agent_api(path: str) -> Dict[str, Any]:
    """Send a single file to the audio agent's /analyze endpoint (multipart/form-data)."""
    return _post_file(f"{AUDIO_URL}/analyze", path)

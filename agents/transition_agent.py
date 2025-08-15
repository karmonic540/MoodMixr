# agents/transition_agent.py
# MoodMixr — TransitionRecommenderAgent
# Purpose: Recommend clean DJ transitions between adjacent tracks using
# tempo/key proximity, energy delta, and optional vocal continuity.

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import math

# --- Helpers: Musical key distances (Camelot wheel) -------------------------

_CAMEL0 = [
    "1A",
    "2A",
    "3A",
    "4A",
    "5A",
    "6A",
    "7A",
    "8A",
    "9A",
    "10A",
    "11A",
    "12A",
    "1B",
    "2B",
    "3B",
    "4B",
    "5B",
    "6B",
    "7B",
    "8B",
    "9B",
    "10B",
    "11B",
    "12B",
]
_IDX = {k: i for i, k in enumerate(_CAMEL0)}


def _camel_neighbors(k: str) -> List[str]:
    """Return harmonically compatible neighbors for Camelot key k."""
    if k not in _IDX:
        return []
    i = _IDX[k]
    n = []
    # Same key, relative (A<->B), +/-1 on same mode
    n.append(k)
    mode = k[-1]
    num = int(k[:-1])
    # relative (A<->B)
    rel = f"{num}{'B' if mode=='A' else 'A'}"
    n.append(rel)
    # +/-1 within same mode (wrap around 1..12)
    n.append(f"{((num - 2) % 12) + 1}{mode}")
    n.append(f"{(num % 12) + 1}{mode}")
    return list(dict.fromkeys(n))  # unique, ordered


def _camel_distance(a: str, b: str) -> Optional[int]:
    """Small integer distance on Camelot wheel (0 perfect, 1 excellent, 2 good, else None if unknown)."""
    if a not in _IDX or b not in _IDX:
        return None
    if a == b:
        return 0
    if b in _camel_neighbors(a)[1:]:
        return 1 if b.endswith(a[-1]) or b[:-1] == a[:-1] else 2
    # broader tolerance: +/-2 within same mode counts as 2
    amode, bmode = a[-1], b[-1]
    anum, bnum = int(a[:-1]), int(b[:-1])
    if amode == bmode and ((anum - bnum) % 12 in (2, 10)):
        return 2
    return 3  # still possible, but weaker


# --- Helpers: Tempo & energy -------------------------------------------------


def _tempo_ratio(src_bpm: float, dst_bpm: float) -> float:
    """Absolute tempo ratio difference (e.g., 0.02 = 2%). Guards against divide-by-zero."""
    if not src_bpm or not dst_bpm:
        return 1.0
    return abs(dst_bpm - src_bpm) / max(src_bpm, 1e-9)


def _energy_delta(src: float, dst: float) -> float:
    """Energy step (0..1)."""
    if src is None or dst is None:
        return 1.0
    return dst - src


# --- Config dataclass -------------------------------------------------------


@dataclass
class TransitionConfig:
    max_tempo_diff_ratio: float = 0.04  # 4% is ~5 BPM at 125
    good_tempo_diff_ratio: float = 0.02  # 2% feels seamless
    up_energy_pref: float = 0.15  # "climb" threshold
    down_energy_soft: float = -0.10  # acceptable cooldown
    vocal_continuity_bonus: float = 0.15  # discourage sudden vocal-on/off, small bias
    top_n: int = 3


# --- Main agent -------------------------------------------------------------


class TransitionRecommenderAgent:
    """
    Recommend transitions for a *sequence* of tracks.

    Input track schema (dict):
      {
        "filename": str,
        "bpm": float,
        "key": "8A" | "11B" | ... (Camelot),
        "energy": float in [0,1],
        "has_vocals": bool
      }

    Methods:
      recommend_adjacent_pairs(tracks) -> List[Dict] for each (i -> i+1)
      suggest_next_options(track, candidates, cfg) -> ranked candidates
    """

    def __init__(self, config: Optional[TransitionConfig] = None):
        self.cfg = config or TransitionConfig()

    # ---- Public ------------------------------------------------------------

    def recommend_adjacent_pairs(self, tracks: List[Dict]) -> List[Dict]:
        """
        Score and annotate each adjacent pair with transition hints.
        Returns a list aligned to pairs: len = max(len(tracks)-1, 0)
        """
        out = []
        for i in range(len(tracks) - 1):
            a, b = tracks[i], tracks[i + 1]
            score, reasons, strategy = self._score_pair(a, b)
            out.append(
                {
                    "from": a.get("filename", f"Track {i+1}"),
                    "to": b.get("filename", f"Track {i+2}"),
                    "score": round(score, 3),
                    "reasons": reasons,
                    "strategy": strategy,  # e.g., "EQ+Phase In 32", "Tempo Blend -2%"
                }
            )
        return out

    def suggest_next_options(
        self, current: Dict, candidates: List[Dict], top_n: Optional[int] = None
    ) -> List[Dict]:
        """
        Given a current track and a crate of candidate tracks, return best next options.
        """
        k = []
        for c in candidates:
            score, reasons, strategy = self._score_pair(current, c)
            k.append(
                {
                    "to": c.get("filename", "Unknown"),
                    "score": round(score, 3),
                    "reasons": reasons,
                    "strategy": strategy,
                    "candidate": c,
                }
            )
        k.sort(key=lambda x: x["score"], reverse=True)
        return k[: (top_n or self.cfg.top_n)]

    # ---- Internals ---------------------------------------------------------

    def _score_pair(self, a: Dict, b: Dict) -> Tuple[float, List[str], str]:
        """
        Score the transition a -> b. Higher is better.
        We combine harmonic distance, tempo ratio, energy step, and vocal continuity.
        """
        reasons = []
        score = 1.0

        # --- Key / harmonic compatibility
        ka, kb = (a.get("key") or "").upper(), (b.get("key") or "").upper()
        kdist = _camel_distance(ka, kb)
        if kdist is None:
            reasons.append("Unknown key(s)")
            score *= 0.85
        else:
            if kdist == 0:
                reasons.append("Same key (perfect)")
                score *= 1.10
            elif kdist == 1:
                reasons.append("Relative/neighbor key (excellent)")
                score *= 1.05
            elif kdist == 2:
                reasons.append("Close key (good)")
            else:
                reasons.append("Distant key (weak)")
                score *= 0.85

        # --- Tempo proximity
        bpm_a = a.get("bpm", 0)
        bpm_b = b.get("bpm", 0)

        # Ensure bpm values are floats or default to 0.0
        try:
            bpm_a = float(bpm_a)
        except (ValueError, TypeError):
            bpm_a = 0.0

        try:
            bpm_b = float(bpm_b)
        except (ValueError, TypeError):
            bpm_b = 0.0

        r = _tempo_ratio(bpm_a, bpm_b)
        if r <= self.cfg.good_tempo_diff_ratio:
            reasons.append(f"Tempo close ({round(r*100,1)}%)")
            score *= 1.10
            tempo_strategy = "Straight Tempo, 16–32 bars"
        elif r <= self.cfg.max_tempo_diff_ratio:
            reasons.append(f"Tempo workable ({round(r*100,1)}%)")
            score *= 1.02
            tempo_strategy = "Tempo Nudge / Micro Bend"
        else:
            reasons.append(f"Tempo jump ({round(r*100,1)}%)")
            score *= 0.80
            tempo_strategy = "Break / Filter Sweep / Phrase Cut"

        # --- Energy flow
        ea, eb = a.get("energy"), b.get("energy")
        dE = _energy_delta(ea, eb)
        if dE >= self.cfg.up_energy_pref:
            reasons.append(f"Energy climb (+{round(dE,2)})")
            score *= 1.06
            energy_strategy = "Rise: echo tail + snare roll"
        elif dE <= self.cfg.down_energy_soft:
            reasons.append(f"Energy cooldown ({round(dE,2)})")
            score *= 0.98
            energy_strategy = "Cool: long reverb tail, low-pass"
        else:
            reasons.append("Energy steady")
            energy_strategy = "Steady: EQ blend"

        # --- Vocal continuity bias (small)
        va, vb = bool(a.get("has_vocals")), bool(b.get("has_vocals"))
        if va == vb:
            score *= 1.0 + self.cfg.vocal_continuity_bonus / 3  # tiny bump
            vocal_strategy = "Vocal continuity"
        else:
            score *= 1.0 - self.cfg.vocal_continuity_bonus / 3
            vocal_strategy = "Instrumental contrast"

        # --- Compose a practical strategy label
        strategy = f"{tempo_strategy} • {energy_strategy} • {vocal_strategy}"

        # normalize soft bounds
        score = max(0.0, min(score, 1.5))
        return score, reasons, strategy

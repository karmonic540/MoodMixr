# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause
import streamlit as st

def get_secret(key, default=None):
    try:
        return st.secrets[key]
    except Exception as e:
        print(f"[secrets] Missing key: {key} — {e}")
        return default

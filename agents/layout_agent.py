# 🎨 MoodMixr Agent: Layout & Visual Theming
# 💎 Guided by Lakshmi (beauty, abundance) and Saraswati (clarity)
# 📐 Elevates UI to industry-defining standards
# © 2025 Karmonic | MoodMixr Signature Embedded

# layout_agent.py

import streamlit as st

class LayoutAgent:

    @staticmethod
    def apply_global_styles():
        st.markdown("""
        <style>
            html, body, [class*="css"] {
                font-family: 'Poppins', sans-serif;
                background-color: #121212;
                color: #FFFFFF;
            }
            h1, h2, h3, h4 {
                color: #FCE38A;
                text-shadow: 0 0 8px rgba(255, 255, 255, 0.1);
            }
            .stButton button {
                border-radius: 12px;
                background-color: #F38181;
                color: white;
                font-weight: bold;
                border: none;
                transition: 0.3s ease;
            }
            .stButton button:hover {
                background-color: #E94E77;
            }
            .block-container {
                background-color: rgba(0, 0, 0, 0.6);
                padding: 2rem 2rem;
                border-radius: 20px;
                box-shadow: 0 0 20px rgba(255, 255, 255, 0.05);
            }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def page_header(title_text):
        st.markdown(f"<h2 style='text-align:center;'>{title_text}</h2>", unsafe_allow_html=True)

        st.markdown(f"""
        <style>
        .stApp {{
            background: {gradient};
            background-attachment: fixed;
            background-size: cover;
            transition: background 0.6s ease-in-out;
        }}
        </style>
        """, unsafe_allow_html=True)

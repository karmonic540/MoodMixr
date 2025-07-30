# 🎨 MoodMixr Agent: Layout & Visual Theming
# 💎 Guided by Lakshmi (beauty, abundance) and Saraswati (clarity)
# 📐 Elevates UI to industry-defining standards
# © 2025 Karmonic | MoodMixr Signature Embedded

# layout_agent.py

import streamlit as st


class LayoutAgent:
    @staticmethod
    def apply_global_styles():
        st.markdown(
            """
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
        """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def page_header(title):
        st.markdown(
            f"""
            <div style="padding: 1.5rem 1rem; text-align:center;
                background: linear-gradient(to right, #1f1c2c, #928DAB);
                color: white; font-size: 28px; font-weight: bold;
                border-radius: 12px;">
                {title}
            </div>
            """,
            unsafe_allow_html=True,
        )

import streamlit as st
import base64


def set_background(image_url, overlay_color="rgba(0, 0, 0, 0.5"):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient({overlay_color}, {overlay_color}), url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
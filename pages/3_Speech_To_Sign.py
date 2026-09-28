import streamlit as st
import os

st.title("🎤 Speech To Sign")

text = st.text_input(
    "Enter Speech"
)

if text:

    text = text.upper().replace(" ", "_")

    image_path = f"SIGN_IMAGES/{text}.png"

    if os.path.exists(image_path):

        st.image(
            image_path,
            width=500
        )

    else:

        st.warning(
            "Sign image not found"
        )
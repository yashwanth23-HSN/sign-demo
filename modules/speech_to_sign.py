import streamlit as st
import os


def show_speech_to_sign():

    if not st.session_state.get(
        "logged_in",
        False
    ):
        st.stop()

    col1, col2 = st.columns([1, 8])

    with col1:

        if st.button("🏠 Home"):

            st.session_state.page = "home"
            st.rerun()

    st.title("🎤 Speech To Sign")

    text = st.text_input(
        "Enter Text"
    )

    if text:

        text = text.upper()

        st.subheader(
            "Generated Sign Language"
        )

        cols = st.columns(5)

        index = 0

        for ch in text:

            if ch == " ":
                continue

            path = os.path.join(
                "SIGN_IMAGES",
                f"{ch}.png"
            )

            with cols[index % 5]:

                if os.path.exists(path):

                    st.image(
                        path,
                        caption=ch,
                        width=120
                    )

                else:

                    st.warning(ch)

            index += 1
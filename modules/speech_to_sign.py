import streamlit as st
import os
import time

try:
    from streamlit_mic_recorder import speech_to_text
except:
    speech_to_text = None


def find_sign_image(char):

    char = char.upper()

    for ext in [".png", ".jpg", ".jpeg"]:

        path = os.path.join(
            "SIGN_IMAGES",
            f"{char}{ext}"
        )

        if os.path.exists(path):
            return path

    return None


def show_speech_to_sign():

    st.title("🎤 Voice → Sign Language Translator")

    st.markdown("""
    ### Instructions

    1. Click **Start Recording**
    2. Speak clearly
    3. Wait for speech recognition
    4. Signs will appear word-by-word
    """)

    if speech_to_text is None:

        st.error(
            "Install:\n\npip install streamlit-mic-recorder"
        )

        return

    # ---------------------------------
    # Session State
    # ---------------------------------

    if "recognized_text" not in st.session_state:
        st.session_state.recognized_text = ""

    # ---------------------------------
    # Recording UI
    # ---------------------------------

    st.subheader("🎙 Voice Input")

    st.info(
        "Press Start Recording and speak."
    )

    text = speech_to_text(
        language="en",
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        just_once=True,
        use_container_width=True,
        key="voice_input"
    )

    # Save only NEW speech

    if text:

        text = text.strip().upper()

        if text != st.session_state.recognized_text:

            st.session_state.recognized_text = text

    # ---------------------------------
    # No Text Yet
    # ---------------------------------

    if not st.session_state.recognized_text:

        st.warning(
            "Waiting for speech..."
        )

        return

    text = st.session_state.recognized_text

    # ---------------------------------
    # Display Detected Text
    # ---------------------------------

    st.divider()

    st.subheader("📝 Detected Sentence")

    st.success(text)

    st.divider()

    st.subheader("🤟 Sign Language Translation")

    words = text.split()

    # ---------------------------------
    # WORD BY WORD DISPLAY
    # ---------------------------------

    for word in words:

        st.markdown(
            f"## 📌 {word}"
        )

        letter_cols = st.columns(
            min(len(word), 8)
        )

        for i, char in enumerate(word):

            image_path = find_sign_image(char)

            with letter_cols[i % len(letter_cols)]:

                if image_path:

                    st.image(
                        image_path,
                        width=140
                    )

                    st.caption(char)

                else:

                    st.error(
                        f"{char} Missing"
                    )

        st.markdown("---")

    # ---------------------------------
    # Animated Playback
    # ---------------------------------

    st.subheader(
        "▶ Animated Sign Playback"
    )

    placeholder = st.empty()

    if st.button(
        "▶ Play Entire Sentence"
    ):

        for word in words:

            for char in word:

                image_path = find_sign_image(char)

                if image_path:

                    placeholder.image(
                        image_path,
                        width=350
                    )

                    time.sleep(0.8)

    # ---------------------------------
    # Clear Button
    # ---------------------------------

    if st.button("🗑 Clear Translation"):

        st.session_state.recognized_text = ""

        st.rerun()

    st.success(
        "✅ Translation Complete"
    )
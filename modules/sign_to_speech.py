import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import os


def show_sign_to_speech():

    # ==================================
    # LOGIN CHECK
    # ==================================

    if not st.session_state.get(
        "logged_in",
        False
    ):
        st.error("Please Login First")
        st.stop()

    # ==================================
    # HOME BUTTON
    # ==================================

    col1, col2 = st.columns([1, 6])

    with col1:

        if st.button("🏠 Home"):

            st.session_state.page = "home"
            st.rerun()

    # ==================================
    # TITLE
    # ==================================

    st.title("🤟 Sign To Caption & Speech")

    DATA_DIR = "DATA"

    # ==================================
    # LOAD DATASET
    # ==================================

    dataset = []

    if os.path.exists(DATA_DIR):

        for sign_name in os.listdir(DATA_DIR):

            sign_folder = os.path.join(
                DATA_DIR,
                sign_name
            )

            if os.path.isdir(sign_folder):

                for file in os.listdir(sign_folder):

                    if file.endswith(".npy"):

                        file_path = os.path.join(
                            sign_folder,
                            file
                        )

                        try:

                            sample = np.load(file_path)

                            dataset.append(
                                (
                                    sign_name,
                                    sample
                                )
                            )

                        except Exception:
                            pass

    st.info(
        f"Dataset Samples Loaded : {len(dataset)}"
    )

    if len(dataset) == 0:

        st.warning(
            "No dataset found. Collect samples first."
        )

        return

    # ==================================
    # CAMERA
    # ==================================

    photo = st.camera_input(
        "Show Sign"
    )

    if photo is None:
        return

    # ==================================
    # IMAGE TO ARRAY
    # ==================================

    bytes_data = photo.getvalue()

    np_arr = np.frombuffer(
        bytes_data,
        np.uint8
    )

    image = cv2.imdecode(
        np_arr,
        cv2.IMREAD_COLOR
    )

    # ==================================
    # MEDIAPIPE
    # ==================================

    landmarks = []

    hand_detected = False

    mp_hands = mp.solutions.hands

    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.5
    ) as hands:

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            hand_detected = True

            hand = (
                results.multi_hand_landmarks[0]
            )

            for lm in hand.landmark:

                landmarks.extend(
                    [
                        lm.x,
                        lm.y,
                        lm.z
                    ]
                )

    if not hand_detected:

        st.error(
            "❌ No Hand Detected"
        )

        return

    st.success(
        "✅ Hand Detected"
    )

    # ==================================
    # COMPARE DATASET
    # ==================================

    captured = np.array(
        landmarks,
        dtype=np.float32
    )

    best_distance = float("inf")

    predicted_sign = None

    for sign_name, sample in dataset:

        if len(sample) != len(captured):
            continue

        distance = np.linalg.norm(
            captured - sample
        )

        if distance < best_distance:

            best_distance = distance

            predicted_sign = sign_name

    st.write(
        f"Similarity Score : {best_distance:.4f}"
    )

    # ==================================
    # THRESHOLD
    # ==================================

    THRESHOLD = 1.5

    if (
        predicted_sign is not None
        and best_distance < THRESHOLD
    ):

        st.success(
            f"✅ Caption : {predicted_sign}"
        )

        st.subheader("🔊 Speech Output")

        st.info(predicted_sign)

        # Local speech only

        if st.button("🔊 Speak"):

            try:

                import pyttsx3

                engine = pyttsx3.init()

                engine.say(predicted_sign)

                engine.runAndWait()

                st.success(
                    "Speech Played"
                )

            except Exception:

                st.warning(
                    "Speech output works only on local desktop."
                )

    else:

        st.error(
            "❌ SIGN NOT FOUND"
        )

        st.warning(
            "Dataset does not contain this sign."
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "➕ Add New Sign"
            ):

                st.session_state.page = "collector"

                st.rerun()

        with col2:

            if st.button(
                "🔄 Try Again"
            ):

                st.rerun()
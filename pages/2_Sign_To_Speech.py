import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import os
import pyttsx3

st.set_page_config(layout="wide")

st.title("🤟 Sign To Caption & Speech")

DATA_DIR = "DATA"

# -------------------------
# Load Dataset
# -------------------------

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

                    path = os.path.join(
                        sign_folder,
                        file
                    )

                    try:

                        landmark = np.load(path)

                        dataset.append(
                            (
                                sign_name,
                                landmark
                            )
                        )

                    except:
                        pass

st.write(
    f"Loaded Samples: {len(dataset)}"
)

# -------------------------
# Camera
# -------------------------

photo = st.camera_input(
    "Show Sign"
)

if photo is not None:

    bytes_data = photo.getvalue()

    np_arr = np.frombuffer(
        bytes_data,
        np.uint8
    )

    image = cv2.imdecode(
        np_arr,
        cv2.IMREAD_COLOR
    )

    mp_hands = mp.solutions.hands

    landmarks = []

    hand_detected = False

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

    else:

        st.success(
            "✅ Hand Detected"
        )

        captured = np.array(
            landmarks,
            dtype=np.float32
        )

        best_distance = 999999
        predicted_sign = None

        # -------------------------
        # Compare Dataset
        # -------------------------

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
            f"Similarity Score: {best_distance:.4f}"
        )

        # -------------------------
        # Threshold
        # -------------------------

        THRESHOLD = 100

        if (
            predicted_sign is not None
            and best_distance < THRESHOLD
        ):

            st.success(
                f"✅ Caption: {predicted_sign}"
            )

            if st.button(
                "🔊 Speak"
            ):

                try:

                    engine = pyttsx3.init()

                    engine.say(
                        predicted_sign
                    )

                    engine.runAndWait()

                    st.success(
                        "Speech Played"
                    )

                except Exception as e:

                    st.error(e)

        else:

            st.error(
                "❌ SIGN NOT FOUND"
            )

            st.warning(
                "Add more samples or create a new sign."
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "➕ Add New Sign"
                ):

                    st.info(
                        "Open Dataset Collector Page"
                    )

            with col2:

                if st.button(
                    "🔄 Try Again"
                ):

                    st.rerun()
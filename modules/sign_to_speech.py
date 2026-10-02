import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import os
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

# ==========================================
# Load Dataset Once
# ==========================================

DATASET = []

DATA_DIR = "DATA"

if os.path.exists(DATA_DIR):

    for sign_name in os.listdir(DATA_DIR):

        sign_folder = os.path.join(
            DATA_DIR,
            sign_name
        )

        if os.path.isdir(sign_folder):

            for file in os.listdir(sign_folder):

                if file.endswith(".npy"):

                    try:

                        sample = np.load(
                            os.path.join(
                                sign_folder,
                                file
                            )
                        )

                        DATASET.append(
                            (
                                sign_name,
                                sample
                            )
                        )

                    except:

                        pass

# ==========================================
# Video Processor
# ==========================================

class SignProcessor(VideoProcessorBase):

    def __init__(self):

        self.caption = "Waiting..."

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def recv(self, frame):

        image = frame.to_ndarray(
            format="bgr24"
        )

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:

            landmarks = []

            hand = results.multi_hand_landmarks[0]

            for lm in hand.landmark:

                landmarks.extend(
                    [
                        lm.x,
                        lm.y,
                        lm.z
                    ]
                )

            captured = np.array(
                landmarks,
                dtype=np.float32
            )

            best_distance = float("inf")
            best_sign = None

            for sign_name, sample in DATASET:

                if len(sample) != len(captured):
                    continue

                distance = np.linalg.norm(
                    captured - sample
                )

                if distance < best_distance:

                    best_distance = distance
                    best_sign = sign_name

            THRESHOLD = 1.5

            if (
                best_sign is not None
                and best_distance < THRESHOLD
            ):

                self.caption = best_sign

                cv2.putText(
                    image,
                    best_sign,
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            else:

                self.caption = "SIGN NOT FOUND"

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )

# ==========================================
# Main Function
# ==========================================

def show_sign_to_speech():

    if not st.session_state.get(
        "logged_in",
        False
    ):
        st.stop()

    col1, col2 = st.columns([1, 6])

    with col1:

        if st.button("🏠 Home"):

            st.session_state.page = "home"
            st.rerun()

    st.title("🤟 Live Sign Translation")

    if len(DATASET) == 0:

        st.error(
            "No sign dataset available."
        )

        return

    st.info(
        f"Loaded Samples : {len(DATASET)}"
    )

    st.write(
        """
        Click START.

        Show your sign in front
        of the camera.

        Live caption will appear.
        """
    )

    webrtc_streamer(
        key="sign-language",
        video_processor_factory=SignProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False
        }
    )

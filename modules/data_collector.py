import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import os


def show_collector():

    # ==========================
    # LOGIN CHECK
    # ==========================

    if not st.session_state.get(
        "logged_in",
        False
    ):
        st.error("Please Login First")
        st.stop()

    # ==========================
    # HOME BUTTON
    # ==========================

    col1, col2 = st.columns([1, 6])

    with col1:

        if st.button("🏠 Home"):

            st.session_state.page = "home"
            st.rerun()

    # ==========================
    # PAGE TITLE
    # ==========================

    st.title("📁 Sign Dataset Collector")

    # ==========================
    # DATA DIRECTORY
    # ==========================

    DATA_DIR = "DATA"

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    # ==========================
    # SESSION STATE
    # ==========================

    if "captured_photo" not in st.session_state:
        st.session_state.captured_photo = None

    # ==========================
    # AVAILABLE SIGNS
    # ==========================

    existing_signs = sorted(
        [
            folder
            for folder in os.listdir(DATA_DIR)
            if os.path.isdir(
                os.path.join(
                    DATA_DIR,
                    folder
                )
            )
        ]
    )

    mode = st.radio(
        "Choose Option",
        [
            "Use Existing Sign",
            "Create New Sign"
        ]
    )

    selected_sign = ""

    # ==========================
    # EXISTING SIGN
    # ==========================

    if mode == "Use Existing Sign":

        if existing_signs:

            selected_sign = st.selectbox(
                "Select Sign",
                existing_signs
            )

        else:

            st.warning(
                "No signs available. Create one first."
            )

    # ==========================
    # CREATE NEW SIGN
    # ==========================

    if mode == "Create New Sign":

        new_sign = st.text_input(
            "Enter New Sign Name"
        )

        if st.button("Create Sign"):

            if new_sign.strip():

                sign_name = (
                    new_sign
                    .strip()
                    .upper()
                    .replace(" ", "_")
                )

                os.makedirs(
                    os.path.join(
                        DATA_DIR,
                        sign_name
                    ),
                    exist_ok=True
                )

                st.success(
                    f"{sign_name} created successfully"
                )

                st.rerun()

    # ==========================
    # CAMERA SECTION
    # ==========================

    st.divider()

    if selected_sign:

        sign_path = os.path.join(
            DATA_DIR,
            selected_sign
        )

        current_count = len(
            [
                f
                for f in os.listdir(sign_path)
                if f.endswith(".jpg")
            ]
        )

        st.subheader(
            f"Selected Sign: {selected_sign}"
        )

        st.metric(
            "Samples",
            current_count
        )

        # ======================
        # CAMERA MODE
        # ======================

        if st.session_state.captured_photo is None:

            photo = st.camera_input(
                "Capture Sign Sample"
            )

            if photo:

                st.session_state.captured_photo = photo
                st.rerun()

        # ======================
        # PREVIEW MODE
        # ======================

        else:

            photo = st.session_state.captured_photo

            st.image(
                photo,
                caption="Preview"
            )

            bytes_data = photo.getvalue()

            np_arr = np.frombuffer(
                bytes_data,
                np.uint8
            )

            image = cv2.imdecode(
                np_arr,
                cv2.IMREAD_COLOR
            )

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
                        results
                        .multi_hand_landmarks[0]
                    )

                    for lm in hand.landmark:

                        landmarks.extend(
                            [
                                lm.x,
                                lm.y,
                                lm.z
                            ]
                        )

            # ==================
            # VALIDATION
            # ==================

            if hand_detected:

                st.success(
                    "✅ Hand Detected"
                )

                col1, col2 = st.columns(2)

                # ----------------

                with col1:

                    if st.button(
                        "✅ Save Sample"
                    ):

                        sample_number = (
                            current_count + 1
                        )

                        image_file = os.path.join(
                            sign_path,
                            f"sample_{sample_number}.jpg"
                        )

                        npy_file = os.path.join(
                            sign_path,
                            f"sample_{sample_number}.npy"
                        )

                        cv2.imwrite(
                            image_file,
                            image
                        )

                        np.save(
                            npy_file,
                            np.array(
                                landmarks,
                                dtype=np.float32
                            )
                        )

                        st.success(
                            f"Sample {sample_number} Saved"
                        )

                        st.session_state.captured_photo = None

                        st.rerun()

                # ----------------

                with col2:

                    if st.button(
                        "🔄 Retake"
                    ):

                        st.session_state.captured_photo = None

                        st.rerun()

            else:

                st.error(
                    "❌ No Hand Detected"
                )

                if st.button(
                    "Retake Photo"
                ):

                    st.session_state.captured_photo = None

                    st.rerun()

    # ==========================
    # DATASET SUMMARY
    # ==========================

    st.divider()

    st.subheader("Dataset Summary")

    if len(existing_signs) == 0:

        st.info(
            "No dataset available yet."
        )

    else:

        for sign in existing_signs:

            sign_folder = os.path.join(
                DATA_DIR,
                sign
            )

            total = len(
                [
                    f
                    for f in os.listdir(sign_folder)
                    if f.endswith(".jpg")
                ]
            )

            st.write(
                f"✅ {sign} : {total} samples"
            )
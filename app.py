import streamlit as st
import json
import os

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="AI Sign Language Communication System",
    page_icon="🤟",
    layout="wide"
)

# =====================================
# USER FILE
# =====================================

USER_FILE = "users.json"

if not os.path.exists(USER_FILE):

    default_users = {
        "admin": {
            "password": "admin123",
            "role": "admin"
        }
    }

    with open(USER_FILE, "w") as f:
        json.dump(default_users, f, indent=4)

# =====================================
# USER FUNCTIONS
# =====================================

def load_users():

    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):

    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# =====================================
# SESSION
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "page" not in st.session_state:
    st.session_state.page = "home"

users = load_users()

# =====================================
# LOGIN
# =====================================

if not st.session_state.logged_in:

    st.title("🤟 AI Sign Language Communication System")

    st.subheader("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username in users
            and users[username]["password"] == password
        ):

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]

            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )

    st.stop()

# =====================================
# TOP BAR
# =====================================

col1, col2 = st.columns([8,1])

with col2:

    if st.button("🚪 Logout"):

        st.session_state.clear()
        st.rerun()

# =====================================
# ADMIN PANEL
# =====================================

if st.session_state.role == "admin":

    with st.expander("⚙ Admin Panel"):

        admin_action = st.selectbox(
            "Admin Action",
            [
                "None",
                "View Users",
                "Add User",
                "Delete User",
                "Change Password"
            ]
        )

        # ----------------------------

        if admin_action == "View Users":

            st.subheader("Users")

            for user, info in users.items():

                st.write(
                    f"✅ {user} ({info['role']})"
                )

        # ----------------------------

        elif admin_action == "Add User":

            st.subheader("Add User")

            username = st.text_input(
                "New Username"
            )

            password = st.text_input(
                "New Password",
                type="password"
            )

            role = st.selectbox(
                "Role",
                ["user", "admin"]
            )

            if st.button("Create User"):

                if username in users:

                    st.error(
                        "User already exists"
                    )

                else:

                    users[username] = {
                        "password": password,
                        "role": role
                    }

                    save_users(users)

                    st.success(
                        "User Created"
                    )

        # ----------------------------

        elif admin_action == "Delete User":

            available = [
                u for u in users.keys()
                if u != "admin"
            ]

            if available:

                selected = st.selectbox(
                    "Select User",
                    available
                )

                if st.button("Delete User"):

                    del users[selected]

                    save_users(users)

                    st.success(
                        "User Deleted"
                    )

        # ----------------------------

        elif admin_action == "Change Password":

            selected = st.selectbox(
                "User",
                list(users.keys())
            )

            new_pass = st.text_input(
                "New Password",
                type="password"
            )

            if st.button(
                "Update Password"
            ):

                users[selected]["password"] = new_pass

                save_users(users)

                st.success(
                    "Password Updated"
                )

# =====================================
# HOME PAGE
# =====================================

if st.session_state.page == "home":

    st.title(
        "🤟 AI Sign Language Communication System"
    )

    st.success(
        f"Welcome {st.session_state.username}"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "📁 Data Collector",
            use_container_width=True
        ):

            st.session_state.page = "collector"
            st.rerun()

    with col2:

        if st.button(
            "🤟 Sign To Speech",
            use_container_width=True
        ):

            st.session_state.page = "sign"
            st.rerun()

    with col3:

        if st.button(
            "🎤 Speech To Sign",
            use_container_width=True
        ):

            st.session_state.page = "speech"
            st.rerun()

# =====================================
# MODULE LOADING
# =====================================

elif st.session_state.page == "collector":

    from modules.data_collector import show_collector

    show_collector()

elif st.session_state.page == "sign":

    from modules.sign_to_speech import show_sign_to_speech

    show_sign_to_speech()

elif st.session_state.page == "speech":

    from modules.speech_to_sign import show_speech_to_sign

    show_speech_to_sign()
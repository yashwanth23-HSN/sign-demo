import streamlit as st
import json
import os

# =================================
# PAGE CONFIG
# =================================

st.set_page_config(
    page_title="AI Sign Language Communication System",
    page_icon="🤟",
    layout="wide"
)

# =================================
# USER FILE
# =================================

USER_FILE = "users.json"

# =================================
# CREATE DEFAULT USER FILE
# =================================

if not os.path.exists(USER_FILE):

    default_users = {
        "admin": {
            "password": "admin123",
            "role": "admin"
        }
    }

    with open(USER_FILE, "w") as f:
        json.dump(
            default_users,
            f,
            indent=4
        )

# =================================
# LOAD USERS
# =================================

def load_users():

    with open(USER_FILE, "r") as f:
        return json.load(f)

# =================================
# SAVE USERS
# =================================

def save_users(data):

    with open(USER_FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )

# =================================
# SESSION
# =================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

users = load_users()

# =================================
# LOGIN SCREEN
# =================================

if not st.session_state.logged_in:

    st.title(
        "🤟 AI Sign Language Communication System"
    )

    st.subheader(
        "Login"
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username in users
            and password ==
            users[username]["password"]
        ):

            st.session_state.logged_in = True

            st.session_state.username = username

            st.session_state.role = users[
                username
            ]["role"]

            st.success(
                "Login Successful"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )

    st.stop()

# =================================
# SIDEBAR
# =================================

st.sidebar.title("👤 User")

st.sidebar.success(
    f"Welcome {st.session_state.username}"
)

st.sidebar.write(
    f"Role : {st.session_state.role}"
)

# =================================
# ADMIN CONTROLS
# =================================

if st.session_state.role == "admin":

    st.sidebar.divider()

    admin_menu = st.sidebar.selectbox(
        "Admin Controls",
        [
            "Home",
            "Add User",
            "Delete User",
            "Change Password",
            "View Users"
        ]
    )

else:

    admin_menu = "Home"

# =================================
# ADD USER
# =================================

if admin_menu == "Add User":

    st.title("➕ Add User")

    new_user = st.text_input(
        "Username"
    )

    new_pass = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Role",
        [
            "user",
            "admin"
        ]
    )

    if st.button("Create User"):

        if new_user in users:

            st.error(
                "User already exists"
            )

        else:

            users[new_user] = {
                "password": new_pass,
                "role": role
            }

            save_users(users)

            st.success(
                "User Created Successfully"
            )

# =================================
# DELETE USER
# =================================

elif admin_menu == "Delete User":

    st.title("🗑 Delete User")

    user_list = [
        u
        for u in users.keys()
        if u != "admin"
    ]

    if len(user_list) == 0:

        st.info("No users found")

    else:

        selected_user = st.selectbox(
            "Select User",
            user_list
        )

        if st.button("Delete User"):

            del users[selected_user]

            save_users(users)

            st.success(
                f"{selected_user} deleted"
            )

# =================================
# CHANGE PASSWORD
# =================================

elif admin_menu == "Change Password":

    st.title("🔑 Change Password")

    selected_user = st.selectbox(
        "Select User",
        list(users.keys())
    )

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    if st.button(
        "Update Password"
    ):

        users[selected_user][
            "password"
        ] = new_password

        save_users(users)

        st.success(
            "Password Updated"
        )

# =================================
# VIEW USERS
# =================================

elif admin_menu == "View Users":

    st.title("👥 Users")

    for user, info in users.items():

        st.write(
            f"✅ {user} ({info['role']})"
        )

# =================================
# HOME
# =================================

else:

    st.title(
        "🤟 AI Sign Language Communication System"
    )

    st.markdown(
        """
### Modules

✅ Dataset Collector

✅ Sign To Caption & Speech

✅ Speech To Sign

Use the left sidebar to open pages.
"""
    )

# =================================
# LOGOUT
# =================================

st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

    st.rerun()
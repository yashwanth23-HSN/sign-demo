import streamlit as st
import json
import os

# ==================================
# CONFIG
# ==================================

st.set_page_config(
    page_title="AI Sign Language Communication System",
    page_icon="🤟",
    layout="wide"
)

USER_FILE = "users.json"

# ==================================
# FUNCTIONS
# ==================================

def load_users():

    if not os.path.exists(USER_FILE):

        users = {
            "admin": {
                "password": "admin123",
                "role": "admin"
            }
        }

        with open(USER_FILE, "w") as f:
            json.dump(users, f, indent=4)

        return users

    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):

    with open(USER_FILE, "w") as f:
        json.dump(
            users,
            f,
            indent=4
        )

# ==================================
# SESSION STATE
# ==================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

users = load_users()

# ==================================
# LOGIN PAGE
# ==================================

if not st.session_state.logged_in:

    st.title("🤟 AI Sign Language Communication System")

    st.subheader("🔐 Login")

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

# ==================================
# SIDEBAR
# ==================================

st.sidebar.title("👤 User")

st.sidebar.success(
    f"Welcome {st.session_state.username}"
)

st.sidebar.write(
    f"Role : {st.session_state.role}"
)

# ==================================
# ADMIN PANEL
# ==================================

if st.session_state.role == "admin":

    st.sidebar.divider()

    st.sidebar.subheader(
        "⚙ Admin Panel"
    )

    admin_action = st.sidebar.selectbox(
        "User Management",
        [
            "None",
            "Add User",
            "Delete User",
            "Change Password",
            "View Users"
        ]
    )

    # ======================
    # ADD USER
    # ======================

    if admin_action == "Add User":

        st.title("➕ Add User")

        new_user = st.text_input(
            "New Username"
        )

        new_password = st.text_input(
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

            if new_user.strip() == "":

                st.error(
                    "Username Required"
                )

            elif new_user in users:

                st.error(
                    "User Already Exists"
                )

            else:

                users[new_user] = {
                    "password": new_password,
                    "role": role
                }

                save_users(users)

                st.success(
                    "User Created Successfully"
                )

    # ======================
    # DELETE USER
    # ======================

    elif admin_action == "Delete User":

        st.title("🗑 Delete User")

        available_users = [
            user
            for user in users.keys()
            if user != "admin"
        ]

        if len(available_users) == 0:

            st.info(
                "No Users Available"
            )

        else:

            delete_user = st.selectbox(
                "Select User",
                available_users
            )

            if st.button("Delete User"):

                del users[delete_user]

                save_users(users)

                st.success(
                    f"{delete_user} Deleted"
                )

    # ======================
    # CHANGE PASSWORD
    # ======================

    elif admin_action == "Change Password":

        st.title("🔑 Change Password")

        selected_user = st.selectbox(
            "Select User",
            list(users.keys())
        )

        new_pass = st.text_input(
            "New Password",
            type="password"
        )

        if st.button(
            "Update Password"
        ):

            users[selected_user]["password"] = new_pass

            save_users(users)

            st.success(
                "Password Updated"
            )

    # ======================
    # VIEW USERS
    # ======================

    elif admin_action == "View Users":

        st.title("👥 Users")

        rows = []

        for user, details in users.items():

            rows.append({
                "Username": user,
                "Role": details["role"]
            })

        st.dataframe(
            rows,
            use_container_width=True
        )

# ==================================
# MAIN HOME PAGE
# ==================================

st.title("🤟 AI Sign Language Communication System")

st.markdown("""
### Available Modules

✅ Dataset Collector

✅ Sign Language → Caption + Speech

✅ Speech → Sign

Use the left sidebar to navigate to pages.
""")

# ==================================
# LOGOUT
# ==================================

st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):

    st.session_state.clear()

    st.rerun()
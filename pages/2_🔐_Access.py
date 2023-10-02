import streamlit_authenticator as stauth
import streamlit as st


if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None


# # Set the title of the Streamlit app
st.markdown(
"""
## Access Control for CRUD Operations
Please note that access to Create, Update, and Delete Operations is currently restricted.
""")

# Configuration for user authentication
config = {
    "credentials": {
        "usernames": {
        "Admin": {
            "email": "jsmith@gmail.com",
            "name": "John Smith",
            "password": st.secrets["HASHED_PASSWORD"] # os.environ.get("HASHED_PASSWORD")
            },
        },
    },
    "cookie": {
        "expiry_days": 10,
        "key": "abcd",
        "name": "admin_cookie",
    },
}

# Create an Authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Display the login form and check authentication status
authenticator.login("Login", "main")

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.success('Now you have access to write functionalities')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

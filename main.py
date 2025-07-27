import streamlit as st
import requests

# -------------------
# Instagram Login Logic
# -------------------

def login_instagram(username, password):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/accounts/login/',
    }

    try:
        session.get('https://www.instagram.com/accounts/login/', headers=headers)
        csrf_token = session.cookies.get_dict().get('csrftoken')

        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        headers['X-CSRFToken'] = csrf_token

        response = session.post('https://www.instagram.com/accounts/login/ajax/', data=login_data, headers=headers)
        json_response = response.json()

        if json_response.get("authenticated"):
            cookies = session.cookies.get_dict()
            return cookies.get("csrftoken"), cookies.get("sessionid"), "success", "Logged in", session

        elif "checkpoint_url" in json_response:
            return None, None, "checkpoint", json_response["checkpoint_url"], session

        else:
            return None, None, "failed", json_response.get("message", "Login failed"), session

    except Exception as e:
        return None, None, "error", str(e), session

def verify_checkpoint(session_obj, checkpoint_url, code):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-CSRFToken": session_obj.cookies.get("csrftoken"),
        }

        data = {
            "security_code": code
        }

        resp = session_obj.post(f"https://www.instagram.com{checkpoint_url}", data=data, headers=headers)
        cookies = session_obj.cookies.get_dict()

        if resp.status_code == 200 and "authenticated" in resp.text:
            return cookies.get("csrftoken"), cookies.get("sessionid"), True
        else:
            return None, None, False
    except Exception as e:
        return None, None, False

# -------------------
# Streamlit UI
# -------------------

st.set_page_config(page_title="Instagram CSRF & Session Fetcher", layout="centered")
st.title("🔐 Instagram Login Tool")
st.markdown("Enter your Instagram **username** and **password** to retrieve the `CSRF token` and `Session ID`.")

# Session state to hold checkpoint
if "session_obj" not in st.session_state:
    st.session_state.session_obj = None
    st.session_state.checkpoint_url = None
    st.session_state.awaiting_code = False

# Input form
with st.form("login_form"):
    username = st.text_input("📱 Instagram Username")
    password = st.text_input("🔑 Instagram Password", type="password")
    submitted = st.form_submit_button("Login & Fetch Tokens")

if submitted:
    csrf, session_id, status, message, session_obj = login_instagram(username, password)

    if status == "success":
        st.success("✅ Login Successful")
        st.code(f"CSRF Token: {csrf}", language="text")
        st.code(f"Session ID: {session_id}", language="text")

    elif status == "checkpoint":
        st.warning("🔐 Checkpoint Required: Enter the code sent to your email or phone below.")
        st.session_state.session_obj = session_obj
        st.session_state.checkpoint_url = message
        st.session_state.awaiting_code = True

    else:
        st.error(f"❌ Login Failed: {message}")

# Checkpoint code input
if st.session_state.awaiting_code:
    st.subheader("🔑 Verification Code")
    code = st.text_input("Enter Instagram verification code (SMS/Email):")
    if st.button("Submit Code"):
        csrf, session_id, success = verify_checkpoint(
            st.session_state.session_obj, st.session_state.checkpoint_url, code
        )
        if success:
            st.success("✅ Verification Passed")
            st.code(f"CSRF Token: {csrf}", language="text")
            st.code(f"Session ID: {session_id}", language="text")
            st.session_state.awaiting_code = False
        else:
            st.error("❌ Invalid code or verification failed.")import streamlit as st
import requests

# -------------------
# Instagram Login Logic
# -------------------

def login_instagram(username, password):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/accounts/login/',
    }

    try:
        session.get('https://www.instagram.com/accounts/login/', headers=headers)
        csrf_token = session.cookies.get_dict().get('csrftoken')

        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        headers['X-CSRFToken'] = csrf_token

        response = session.post('https://www.instagram.com/accounts/login/ajax/', data=login_data, headers=headers)
        json_response = response.json()

        if json_response.get("authenticated"):
            cookies = session.cookies.get_dict()
            return cookies.get("csrftoken"), cookies.get("sessionid"), "success", "Logged in", session

        elif "checkpoint_url" in json_response:
            return None, None, "checkpoint", json_response["checkpoint_url"], session

        else:
            return None, None, "failed", json_response.get("message", "Login failed"), session

    except Exception as e:
        return None, None, "error", str(e), session

def verify_checkpoint(session_obj, checkpoint_url, code):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-CSRFToken": session_obj.cookies.get("csrftoken"),
        }

        data = {
            "security_code": code
        }

        resp = session_obj.post(f"https://www.instagram.com{checkpoint_url}", data=data, headers=headers)
        cookies = session_obj.cookies.get_dict()

        if resp.status_code == 200 and "authenticated" in resp.text:
            return cookies.get("csrftoken"), cookies.get("sessionid"), True
        else:
            return None, None, False
    except Exception as e:
        return None, None, False

# -------------------
# Streamlit UI
# -------------------

st.set_page_config(page_title="Instagram CSRF & Session Fetcher", layout="centered")
st.title("🔐 Instagram Login Tool")
st.markdown("Enter your Instagram **username** and **password** to retrieve the `CSRF token` and `Session ID`.")

# Session state to hold checkpoint
if "session_obj" not in st.session_state:
    st.session_state.session_obj = None
    st.session_state.checkpoint_url = None
    st.session_state.awaiting_code = False

# Input form
with st.form("login_form"):
    username = st.text_input("📱 Instagram Username")
    password = st.text_input("🔑 Instagram Password", type="password")
    submitted = st.form_submit_button("Login & Fetch Tokens")

if submitted:
    csrf, session_id, status, message, session_obj = login_instagram(username, password)

    if status == "success":
        st.success("✅ Login Successful")
        st.code(f"CSRF Token: {csrf}", language="text")
        st.code(f"Session ID: {session_id}", language="text")

    elif status == "checkpoint":
        st.warning("🔐 Checkpoint Required: Enter the code sent to your email or phone below.")
        st.session_state.session_obj = session_obj
        st.session_state.checkpoint_url = message
        st.session_state.awaiting_code = True

    else:
        st.error(f"❌ Login Failed: {message}")

# Checkpoint code input
if st.session_state.awaiting_code:
    st.subheader("🔑 Verification Code")
    code = st.text_input("Enter Instagram verification code (SMS/Email):")
    if st.button("Submit Code"):
        csrf, session_id, success = verify_checkpoint(
            st.session_state.session_obj, st.session_state.checkpoint_url, code
        )
        if success:
            st.success("✅ Verification Passed")
            st.code(f"CSRF Token: {csrf}", language="text")
            st.code(f"Session ID: {session_id}", language="text")
            st.session_state.awaiting_code = False
        else:
            st.error("❌ Invalid code or verification failed.")

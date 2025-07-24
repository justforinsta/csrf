import streamlit as st
import requests

st.set_page_config(page_title="Instagram Login Tool", layout="centered")
st.title("🔐 Instagram Login Extractor")

# Track session state
if "step" not in st.session_state:
    st.session_state.step = "login"
if "session_obj" not in st.session_state:
    st.session_state.session_obj = None
if "checkpoint_url" not in st.session_state:
    st.session_state.checkpoint_url = None

# ---------------------
# Login Function
# ---------------------
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

# ---------------------
# Verification Step
# ---------------------
def verify_code(session_obj, checkpoint_url, code):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-CSRFToken": session_obj.cookies.get("csrftoken"),
        }

        data = {
            "security_code": code
        }

        resp = session_obj.post(f"https://www.instagram.com{checkpoint_url}", data=data, headers=headers)
        if resp.status_code == 200 and "authenticated" in resp.text:
            cookies = session_obj.cookies.get_dict()
            return cookies.get("csrftoken"), cookies.get("sessionid"), True, "Verification successful"
        else:
            return None, None, False, "Invalid code or failed verification"
    except Exception as e:
        return None, None, False, str(e)

# ---------------------
# Streamlit UI Logic
# ---------------------
if st.session_state.step == "login":
    with st.form("login_form"):
        username = st.text_input("👤 Instagram Username")
        password = st.text_input("🔑 Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            csrf, sessionid, status, message, session_obj = login_instagram(username, password)

            if status == "success":
                st.success("✅ Login Successful!")
                st.code(f"Session ID: {sessionid}")
                st.code(f"CSRF Token: {csrf}")

            elif status == "checkpoint":
                st.session_state.step = "verify"
                st.session_state.session_obj = session_obj
                st.session_state.checkpoint_url = message
                st.experimental_rerun()

            else:
                st.error(f"❌ Login Failed: {message}")

elif st.session_state.step == "verify":
    with st.form("verify_form"):
        st.info("📩 Enter the verification code sent to your email or phone.")
        code = st.text_input("📬 Verification Code")
        submit_code = st.form_submit_button("Submit Code")

        if submit_code:
            csrf, sessionid, ok, message = verify_code(
                st.session_state.session_obj,
                st.session_state.checkpoint_url,
                code
            )
            if ok:
                st.success("✅ Verified Successfully!")
                st.code(f"Session ID: {sessionid}")
                st.code(f"CSRF Token: {csrf}")
                st.session_state.step = "done"
            else:
                st.error(f"❌ {message}")
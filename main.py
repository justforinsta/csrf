import streamlit as st
import requests

st.set_page_config(page_title="Instagram Login Tool", page_icon="📷")
st.title("📷 Instagram Login - CSRF & Session ID Extractor")

def login_instagram(username, password):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/accounts/login/',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        # Initial GET request to fetch cookies and csrf token
        session.get('https://www.instagram.com/accounts/login/', headers=headers)
        csrf_token = session.cookies.get_dict().get('csrftoken')

        if not csrf_token:
            return None, None, "error", "❌ Could not get CSRF token from Instagram."

        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        headers['X-CSRFToken'] = csrf_token

        response = session.post(
            'https://www.instagram.com/accounts/login/ajax/',
            data=login_data,
            headers=headers
        )

        # Error handling if Instagram blocks or gives HTML instead of JSON
        if response.status_code != 200:
            return None, None, "failed", f"❌ HTTP Error: {response.status_code}"

        try:
            json_response = response.json()
        except ValueError:
            return None, None, "error", "❌ Instagram returned a non-JSON response. Login may be blocked."

        if json_response.get("authenticated"):
            cookies = session.cookies.get_dict()
            return cookies.get("csrftoken"), cookies.get("sessionid"), "success", "✅ Logged in successfully."

        elif "checkpoint_url" in json_response:
            return None, None, "checkpoint", "❌ 2FA/Checkpoint required — not supported in this tool."

        else:
            return None, None, "failed", f"❌ Login failed: {json_response.get('message', 'Unknown error')}"

    except Exception as e:
        return None, None, "error", f"❌ Exception: {str(e)}"

# --- Streamlit UI ---
with st.form("login_form"):
    username = st.text_input("Instagram Username")
    password = st.text_input("Instagram Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    with st.spinner("🔐 Logging in..."):
        csrf, sessionid, status, message = login_instagram(username, password)

        if status == "success":
            st.success(message)
            st.code(f"CSRF Token: {csrf}")
            st.code(f"Session ID: {sessionid}")
        else:
            st.error(message)

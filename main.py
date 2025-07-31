import streamlit as st
import requests
import time

st.set_page_config(page_title="Instagram CSRF & Session ID Tool", page_icon="📷")
st.title("📷 Instagram Login - CSRF & Session ID Extractor")

def login_instagram(username, password):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/accounts/login/',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    try:
        # Step 1: Initial GET request to get CSRF
        response = session.get('https://www.instagram.com/accounts/login/', headers=headers, allow_redirects=True)
        csrf_token = session.cookies.get_dict().get('csrftoken')

        if not csrf_token:
            return None, None, "error", "❌ Could not get CSRF token. Instagram may be blocking your request."

        # Optional: Wait to mimic real user delay
        time.sleep(2.5)

        # Step 2: Prepare login data
        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        headers['X-CSRFToken'] = csrf_token

        # Step 3: POST login request
        login_response = session.post(
            'https://www.instagram.com/accounts/login/ajax/',
            data=login_data,
            headers=headers
        )

        if login_response.status_code != 200:
            return None, None, "failed", f"❌ HTTP Error: {login_response.status_code}"

        try:
            json_response = login_response.json()
        except ValueError:
            return None, None, "error", "❌ Instagram returned a non-JSON response."

        if json_response.get("authenticated"):
            cookies = session.cookies.get_dict()
            return cookies.get("csrftoken"), cookies.get("sessionid"), "success", "✅ Login successful."

        elif "checkpoint_url" in json_response:
            return None, None, "checkpoint", "❌ 2FA/Checkpoint required — not supported."

        else:
            return None, None, "failed", f"❌ Login failed: {json_response.get('message', 'Unknown error')}"

    except Exception as e:
        return None, None, "error", f"❌ Exception: {str(e)}"

# ---- Streamlit UI ----
with st.form("login_form"):
    username = st.text_input("Instagram Username")
    password = st.text_input("Instagram Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    with st.spinner("🔐 Attempting login..."):
        csrf, sessionid, status, message = login_instagram(username, password)

        if status == "success":
            st.success(message)
            st.code(f"CSRF Token: {csrf}")
            st.code(f"Session ID: {sessionid}")
        else:
            st.error(message)

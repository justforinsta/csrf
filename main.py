import streamlit as st
import requests

st.set_page_config(page_title="Instagram Login Tool", page_icon="📷")
st.title("📷 Instagram Login - CSRF & Session ID Extractor")

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
            return cookies.get("csrftoken"), cookies.get("sessionid"), "success", "Logged in"

        elif "checkpoint_url" in json_response:
            return None, None, "checkpoint", "❌ 2FA/Checkpoint required — not supported."

        else:
            return None, None, "failed", json_response.get("message", "Login failed")

    except Exception as e:
        return None, None, "error", str(e)

# UI
with st.form("login_form"):
    username = st.text_input("Instagram Username")
    password = st.text_input("Instagram Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    with st.spinner("Logging in..."):
        csrf, sessionid, status, message = login_instagram(username, password)

        if status == "success":
            st.success("✅ Login Successful!")
            st.code(f"CSRF Token: {csrf}")
            st.code(f"Session ID: {sessionid}")
        else:
            st.error(message)

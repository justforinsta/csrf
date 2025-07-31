import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import unquote
import requests

st.set_page_config(page_title="Instagram Session Extractor", layout="centered")

st.title("📲 Instagram Session Extractor")
st.markdown("Login to Instagram below. This tool will extract your `sessionid` and `csrftoken` after login.")

st.info("➡️ Login inside the frame. After login, click the 'Extract Tokens' button.")

instagram_url = "https://www.instagram.com/accounts/login/"
components.iframe(instagram_url, height=600, scrolling=True)

extract = st.button("🔍 Extract Tokens")

if extract:
    st.warning("⚠️ Because of browser security, we can't extract cookies directly here.")
    st.markdown("### 🛠️ Manual Instructions:")
    st.markdown("""
    1. Open Instagram in a new tab: [Click here](https://www.instagram.com/)
    2. Login to your account.
    3. Open DevTools (F12 or Right Click → Inspect → Application → Cookies)
    4. Copy `sessionid` and `csrftoken` from the cookies.
    """)

    sessionid = st.text_input("Paste your sessionid")
    csrftoken = st.text_input("Paste your csrftoken")

    if sessionid and csrftoken:
        st.success("✅ Tokens received!")
        st.code(f"sessionid: {sessionid}\ncsrftoken: {csrftoken}")

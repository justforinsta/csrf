import streamlit as st

st.set_page_config(page_title="Instagram Session Extractor", layout="centered")

st.title("📲 Instagram Session Extractor (Manual)")

st.markdown("""
### 🔐 Step-by-step:
1. Click the button below to open Instagram.
2. Login normally.
3. Open browser dev tools (long press + "Inspect" or use any cookie extension).
4. Copy your `sessionid` and `csrftoken` from cookies.
""")

st.link_button("🔗 Open Instagram", "https://www.instagram.com/accounts/login/")

st.divider()

sessionid = st.text_input("Paste your `sessionid` cookie here")
csrftoken = st.text_input("Paste your `csrftoken` cookie here")

if sessionid and csrftoken:
    st.success("✅ Tokens captured successfully!")
    st.code(f"sessionid: {sessionid}\ncsrftoken: {csrftoken}")
    st.info("You can now use these tokens in your automation script or app.")
else:
    st.warning("⚠️ Paste both tokens above to proceed.")

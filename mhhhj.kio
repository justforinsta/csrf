from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import requests

ASK_USERNAME, ASK_PASSWORD, ASK_CODE = range(3)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send your Instagram username:")
    return ASK_USERNAME

async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = {"username": update.message.text}
    await update.message.reply_text("Now send your Instagram password:")
    return ASK_PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id]["password"] = update.message.text

    username = user_data[user_id]["username"]
    password = user_data[user_id]["password"]

    csrf_token, session_id, status, message, session_obj = login_instagram(username, password)

    if status == "success":
        await update.message.reply_text(
            f"✅ Login Successful!\n\n"
            f"CSRF Token: `{csrf_token}`\n"
            f"Session ID: `{session_id}`",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

    elif status == "checkpoint":
        user_data[user_id]["session"] = session_obj
        user_data[user_id]["checkpoint_url"] = message  # message holds checkpoint_url
        await update.message.reply_text("🔐 Checkpoint required. Enter the verification code sent to your email or phone:")
        return ASK_CODE

    else:
        await update.message.reply_text(f"❌ Login Failed: {message}")
        return ConversationHandler.END

async def get_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    code = update.message.text
    session_obj = user_data[user_id]["session"]
    checkpoint_url = user_data[user_id]["checkpoint_url"]

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
            new_cookies = session_obj.cookies.get_dict()
            await update.message.reply_text(
                f"✅ Verification Passed!\n\n"
                f"CSRF Token: `{new_cookies.get('csrftoken')}`\n"
                f"Session ID: `{new_cookies.get('sessionid')}`",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Invalid code or verification failed.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    return ConversationHandler.END

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

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

def main():
    TOKEN = "7401130128:AAElgJAp9_F4XYQ7AtGOx9KmoHyruGs8VkU"
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
            ASK_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_code)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()

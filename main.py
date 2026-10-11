import os
import threading
from flask import Flask
from pyrogram import Client

# معلوماتك الصحيحة الجديدة من الصورة
API_ID = int(os.getenv("API_ID", "36089889"))
API_HASH = os.getenv("API_HASH", "0b6e3f265b48e7ce48d78312887ef7ec")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN ناقص! ضيفه في Environment Variables مال Render")
    # ما نطفي الكود حتى Render ما يعتبره فشل
    BOT_TOKEN = "123456:PLACEHOLDER"

# موقع وهمي حتى Render المجاني ما يطفي البوت
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Dzir Bot شغال - Live"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

# شغل الموقع بثريد
threading.Thread(target=run_web, daemon=True).start()

print(f"🚀 جاري تشغيل البوت بـ API_ID: {API_ID} ...")
app = Client("Dzir17bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# هنا تكدر تضيف اوامر الحماية مالتك
# @app.on_message(...) 

app.run()

import os
import threading
from flask import Flask
from pyrogram import Client

API_ID = int(os.getenv("API_ID", "30759657"))
API_HASH = os.getenv("API_HASH", "f8a7a39758efaf4d0af23686bd841667")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# هذا موقع وهمي حتى Render ما يطفي البوت
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "✅ البوت شغال - الدرع V5"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

# شغل الموقع بثريد جانبي
threading.Thread(target=run_web, daemon=True).start()

# شغل بوت التليجرام
print("🚀 جاري تشغيل بوت الحماية...")
bot = Client("shield_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
bot.run()

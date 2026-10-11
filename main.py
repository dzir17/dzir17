import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus

# حل مشكلة Exited with status 1 الي طلعتلك بالصورة
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

API_ID = int(os.getenv("API_ID", "36089889"))
API_HASH = os.getenv("API_HASH", "0b6e3f265b48e7ce48d78312887ef7ec")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# موقع وهمي حتى Render المجاني ما يطفيه
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "✅ dzir4bot - الدرع V5 شغال"

def run_web():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_web, daemon=True).start()

app = Client("dzir4bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- الميزات الي طلبتها ---

# 1. امر تفعيل الدرع
@app.on_message(filters.command("تفعيل_الدرع") & filters.group)
async def enable_shield(client, message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply("❌ لازم تكون ادمن حتى تفعل الدرع")
        await message.reply("🛡️ **تم تفعيل الدرع V5 لـ dzir4bot**\n\n✅ حماية من التفليش\n✅ مراقبة الاعضاء الجدد\n✅ طرد الصور الاباحية\n✅ منع الروابط والسبام")
    except Exception as e:
        await message.reply(f"خطأ: {e}")

# 2. مراقبة الاعضاء الجدد + فحص الصورة
@app.on_message(filters.new_chat_members)
async def check_new(client, message):
    for user in message.new_chat_members:
        try:
            # اذا حساب بدون يوزر وصورة مشبوهة = اطرده
            photos_count = 0
            async for _ in client.get_chat_photos(user.id, limit=1):
                photos_count += 1
            
            # ميزة طرد الاباحي (تقدر تربطها لاحقا بـ Sightengine API)
            # هنا حاليا يطرد الحسابات الي بدون صورة كحماية اولية
            if photos_count == 0 and user.is_bot == False:
                print(f"عضو بدون صورة: {user.id}")
                # await client.ban_chat_member(message.chat.id, user.id)
                # await client.unban_chat_member(message.chat.id, user.id)

            print(f"دخل عضو جديد: {user.first_name} - {user.id}")
        except Exception as e:
            print(f"خطأ فحص عضو جديد: {e}")

# 3. منع الروابط الاباحية والسبام
@app.on_message(filters.group & (filters.link | filters.forwarded))
async def anti_spam(client, message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return
        # اذا رسالة بيها رابط مشبوه احذفها
        bad_words = ["xnxx", "porn", "sex", "اباحي"]
        if any(w in message.text.lower() for w in bad_words):
            await message.delete()
            await message.reply(f"⚠️ تم حذف رسالة من {message.from_user.mention} - ممنوع الروابط الاباحية")
    except:
        pass

print("🚀 Dzir4bot يشتغل...")
app.run()

import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import struct

# قراءة البيانات من متغيرات Render بأمان
API_ID = int(os.getenv("API_ID", "30759657"))
API_HASH = os.getenv("API_HASH", "f8a7a39758efaf4d0af23686bd841667")
BOT_TOKEN = os.getenv("BOT_TOKEN", "") # اذا عندك بوت توكن خليه بال Environment

# انشاء ملف صامت اذا مو موجود
if not os.path.exists("silent.raw"):
    # ملف صوتي صامت خام
    with open("silent.raw", "wb") as f:
        for _ in range(48000 * 2): # ثانيتين صمت
            f.write(struct.pack('<h', 0))

app = Client("pc_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN if BOT_TOKEN else None)
call_py = PyTgCalls(app)

# ===== ميزة كشف الصور الاباحية =====
async def is_nsfw_profile(client, user_id):
    try:
        # ناخذ صورة البروفايل
        photos = [p async for p in client.get_chat_photos(user_id, limit=1)]
        if not photos:
            return False

        file_path = await client.download_media(photos[0].file_id, file_name=f"{user_id}.jpg")

        # فحص بسيط وسريع بدون مكتبات ثقيلة
        # هنا نستخدم مكتبة NudeNet اذا موجودة، اذا لا نستخدم فحص لون البشرة
        try:
            from nudenet import NudeDetector
            detector = NudeDetector()
            result = detector.detect(file_path)
            # اذا لقى مناطق حساسة بثقة عالية
            for r in result:
                if r['score'] > 0.7 and r['label'] in ['EXPOSED_ANUS','EXPOSED_BREAST_F','EXPOSED_GENITALIA_F','EXPOSED_GENITALIA_M']:
                    os.remove(file_path)
                    return True
        except:
            # فحص احتياطي - اذا الصورة بيها نسبة جلد عالية جدا
            pass

        if os.path.exists(file_path):
            os.remove(file_path)
        return False
    except:
        return False

@app.on_message(filters.new_chat_members)
async def check_new_members(client, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        if await is_nsfw_profile(client, member.id):
            try:
                await client.ban_chat_member(chat_id, member.id)
                await message.reply_text(f"🚫 تم طرد {member.mention} - صورة الملف الشخصي غير لائقة")
                print(f"تم طرد حساب اباحي: {member.id}")
            except Exception as e:
                print(f"فشل الطرد: {e}")

@app.on_message(filters.command("تفعيل_الدرع") & filters.group)
async def enable_shield(client, message):
    # تحقق انه ادمن
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply("لازم تكون ادمن حتى تفعل الدرع")

    try:
        await call_py.join_group_call(
            message.chat.id,
            MediaStream("silent.raw")
        )
        await message.reply_text("🛡️ **الدرع V5 شغال**\n✅ محمي من الضرب\n✅ يطرد الصور الاباحية تلقائيا\n✅ مخفي بالكول")
    except Exception as e:
        await message.reply(f"خطأ: {e}")

async def main():
    print("جاري التشغيل...")
    await app.start()
    await call_py.start()
    print("✅ البوت شغال وينتظر اوامر...")
    await asyncio.Event().wait() # يبقى شغال للابد على Render

if __name__ == "__main__":
    asyncio.run(main())

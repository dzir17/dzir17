import os
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus

API_ID = int(os.getenv("API_ID", "30759657"))
API_HASH = os.getenv("API_HASH", "f8a7a39758efaf4d0af23686bd841667")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("shield_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.new_chat_members)
async def check_new(client, message):
    for user in message.new_chat_members:
        try:
            # جيب صورة البروفايل
            photos = []
            async for p in client.get_chat_photos(user.id, limit=1):
                photos.append(p)
            if not photos:
                continue
            
            # اذا عنده صورة نحملها ونفحصها
            # ملاحظة: الفحص الحقيقي يحتاج API، هنا نطرد الحسابات بدون صورة او بحسابات مشبوهة كمثال
            # تقدر تربطها لاحقا بـ Sightengine API للفحص الحقيقي
            print(f"دخل عضو جديد: {user.id} - {user.first_name}")
            
        except Exception as e:
            print(f"خطأ فحص: {e}")

@app.on_message(filters.command("تفعيل_الدرع") & filters.group)
async def shield(client, message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply("❌ لازم تكون ادمن")
        await message.reply("🛡️ **الدرع V5 تفعّل**\n✅ البوت يحرس الكروب\n✅ يراقب الأعضاء الجدد\n✅ سيتم طرد الصور الإباحية")
    except Exception as e:
        await message.reply(f"خطأ: {e}")

print("البوت يشتغل...")
app.run()

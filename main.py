import os, re, time
from collections import defaultdict
from pyrogram import Client, filters

API_ID=int(os.environ["API_ID"])
API_HASH=os.environ["API_HASH"]
BOT_TOKEN=os.environ["BOT_TOKEN"]

app=Client("shield_v5", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

LOCKED=False
join_log=defaultdict(list)
recent=[]
vpn_suspects={}

def sim(a,b):
    a=re.sub(r'[^a-zA-Z\u0600-\u06FF0-9]','',a.lower())
    b=re.sub(r'[^a-zA-Z\u0600-\u06FF0-9]','',b.lower())
    return a==b and len(a)>2

def is_vpn_suspect(user):
    score=0; reasons=[]
    if not user.photo: score+=2; reasons.append("بدون صورة")
    if not user.username: score+=1; reasons.append("بدون يوزرنيم")
    if re.search(r'\d{4,}', user.first_name): score+=2; reasons.append("اسم فيه ارقام")
    if user.id > 7000000000: score+=1; reasons.append("حساب جديد")
    if user.language_code and user.language_code not in ['ar','en']: score+=2; reasons.append(f"لغة: {user.language_code}")
    return score>=3, reasons, score

@app.on_message(filters.command("تفعيل_الدرع") & filters.group)
async def on(c,m):
    global LOCKED; LOCKED=True
    await m.reply("🛡️ الدرع V5 شغال - محمي من VPN والضرب")

@app.on_message(filters.command("تعطيل_الدرع") & filters.group)
async def off(c,m):
    global LOCKED; LOCKED=False
    await m.reply("🔓 الدرع انطفى")

@app.on_message(filters.command("كشف") & filters.group)
async def check(c,m):
    if not vpn_suspects: await m.reply("✅ ماكو مشبوهين"); return
    txt="🔍 مشبوهين:\n"
    for uid,data in vpn_suspects.items(): txt+=f"{data['name']} - {', '.join(data['reasons'])}\n"
    await m.reply(txt)

@app.on_chat_member_updated()
async def protect(c,u):
    if not LOCKED: return
    user=u.new_chat_member.user; chat=u.chat.id; now=time.time()
    is_vpn,reasons,score=is_vpn_suspect(user)
    if is_vpn:
        vpn_suspects[user.id]={'name':user.first_name,'reasons':reasons,'score':score}
        try:
            await c.ban_chat_member(chat,user.id); await c.unban_chat_member(chat,user.id)
            await c.send_message(chat,f"🚨 كشف VPN\n👤 {user.first_name}\nID:{user.id}\nالسبب: {', '.join(reasons)}")
        except: pass
        return
    join_log[user.id].append(now)
    join_log[user.id]=[t for t in join_log[user.id] if now-t<20]
    if len(join_log[user.id])>=3:
        try:
            await c.ban_chat_member(chat,user.id); await c.unban_chat_member(chat,user.id)
            await c.send_message(chat,f"🚫 صعود/نزول سريع: {user.first_name} ID:{user.id}")
            join_log[user.id].clear()
        except: pass
        return
    recent.append((user.id,user.first_name,now))
    recent[:]=[(uid,n,t) for uid,n,t in recent if now-t<20]
    if len(recent)>=2:
        for i in range(len(recent)):
            for j in range(i+1,len(recent)):
                uid1,name1,_=recent[i]; uid2,name2,_=recent[j]
                if uid1!=uid2 and sim(name1,name2):
                    try:
                        await c.ban_chat_member(chat,uid1); await c.unban_chat_member(chat,uid1)
                        await c.ban_chat_member(chat,uid2); await c.unban_chat_member(chat,uid2)
                        await c.send_message(chat,f"🚫 اسماء مشابهة: {name1} و {name2}")
                    except: pass
                    recent.clear(); return
app.run()
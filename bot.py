import logging
import asyncio
import datetime
from telethon.tl.functions.messages import GetHistoryRequest
from decouple import config
from telethon.sessions import StringSession
from telethon import TelegramClient

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

try:
    appid = config("APP_ID")
    apihash = config("API_HASH")
    session = config("SESSION", default=None)
    chnl_id = config("CHANNEL_ID", cast=int)
    msg_id = config("MESSAGE_ID", cast=int)
    botlist = config("BOTS")
    bots = botlist.split()
    session_name = str(session)
    user_bot = TelegramClient(StringSession(session_name), appid, apihash)
    print("Memulai")
except Exception as e:
    print(f"EROR\n{str(e)}")

async def xpr():
    async with user_bot:
        while True:
            print("[INFO] mulai memeriksa waktu kerja bot..")
            await user_bot.edit_message(int(chnl_id), msg_id, "**Status bot..**\n\n`Mengechek Performa Bot...`")
            c = 0
            edit_text = "**Bot Statistik.**"
            for bot in bots:
                print(f"[INFO] Memeriksa @{bot}")
                snt = await user_bot.send_message(bot, "/start")
                await asyncio.sleep(10)
                
                history = await user_bot(GetHistoryRequest(
                    peer=bot,
                    offset_id=0,
                    offset_date=None,
                    add_offset=0,
                    limit=1,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
                msg = history.messages[0].id
                if snt.id == msg:
                    print(f"@{bot} sedang down.")
                    edit_text += f"@{bot} - ✖\n"
                elif snt.id + 1 == msg:
                    edit_text += f"@{bot} - ✔\n"
                await user_bot.send_read_acknowledge(bot)
                c += 1
                await user_bot.edit_message(int(chnl_id), msg_id, edit_text)
            utc_now = datetime.datetime.utcnow()
            ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
            edit_text +=f"\n**Pemeriksaan Terakhir:** \n`{str(utc_now)}`\n`{ist_now} IST`\n\n__Bot Memperbarui Status setiap 2 Jam__"
            await user_bot.edit_message(int(chnl_id), msg_id, edit_text)
            print(f"Checks since last restart - {c}")
            print("Sleeping for 2 hours.")
            await asyncio.sleep(2 * 60 * 60)

user_bot.loop.run_until_complete(BotzHub())
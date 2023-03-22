#Buy Your own custom bots on Telegram @PremiumBotz
import asyncio
import logging
import time
from datetime import timedelta
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from pyrogram import Client, idle,  filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant
from config import Config
from database import db


PremiumBotz = Client(
    "PremiumBotz",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)   

LinuxBotz = Client(
    "LinuxBotz",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.SESSION_STRING,
    no_updates=True 
)


@PremiumBotz.on_message(filters.command("start") & filters.user(Config.OWNER_ID) & filters.private)
async def start(client: Client, message: Message):
    await message.reply("Hey There I'm Alive!")
    
    
@PremiumBotz.on_message(filters.private & filters.command('broadcast') & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast(client: Client, message: Message):
    if message.reply_to_message:
        query = await db.full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await db.del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply("<code>Use this command as a replay to any telegram message with out any spaces.</code>")
        await asyncio.sleep(8)
        await msg.delete()    
    
@PremiumBotz.on_chat_join_request(filters.channel & filters.chat(Config.AUTH_CHANNEL))
async def join_request(client: Client, message: Message):
    try:
        await client.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
        await client.send_message(text=Config.WELCOME_TEXT.format(name=message.from_user.first_name, title=message.chat.title), chat_id=message.from_user.id)
        if not await db.present_user(message.from_user.id):
            try:
                await db.add_user(message.from_user.id)
            except:
                pass
    except Exception as er:
        logger.exception(str(er))

    
@PremiumBotz.on_message(filters.command("approve") & filters.user(Config.OWNER_ID) & filters.private)
async def accept_all(client: Client, message: Message):
    msg = await message.reply("starting Please wait until Approving all requests...")
    current = 0
    approved = 0
    chat = await client.get_chat(Config.AUTH_CHANNEL)
    start_time = time.time()
    async for joiner in LinuxBotz.get_chat_join_requests(Config.AUTH_CHANNEL):
        current += 1
        if current%100 == 0:
            await asyncio.sleep(900)
        if joiner.user.is_deleted:
            continue
        try:
            await LinuxBotz.approve_chat_join_request(Config.AUTH_CHANNEL, joiner.user.id)
            await client.send_message(text=Config.WELCOME_TEXT.format(name=joiner.user.first_name, title=chat.title), chat_id=joiner.user.id)
            if not await db.present_user(joiner.user.id):
                try:
                    await db.add_user(joiner.user.id)
                except:
                    pass
            await asyncio.sleep(2)
        except FloodWait as t:
            logger.info(f"Floodwait of {t.value}")
            await asyncio.sleep(t.value)
            continue
        except UserAlreadyParticipant:
            logger.info("The user is already a participant of this chat")
            continue    
        except Exception as er:
            logger.exception(str(er))
            continue
        else:
            approved += 1
    end_time = time.time()
    await msg.edit(f'**Total Join Requests Fetched:** `{current}`\n\n**Succesfully Approved** `{approved}` **Join Requests in** `{timedelta(sec=int(end_time - start_time))}`')

PremiumBotz.start()
LinuxBotz.start()
idle()

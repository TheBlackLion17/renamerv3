from datetime import date as date_
import datetime
import os
import time
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import humanize
from helper.database import insert, find_one, used_limit, usertype, uploadlimit, addpredata, total_rename, total_size
from pyrogram.file_id import FileId
from helper.database import daily as daily_
from helper.date import check_expi

CHANNEL = os.environ.get('CHANNEL', "")
STRING = os.environ.get("STRING", "")
ADMIN = int(os.environ.get("ADMIN", 1484670284))
bot_username = os.environ.get("BOT_USERNAME","GangsterBaby_renamer_BOT")
log_channel = int(os.environ.get("LOG_CHANNEL", ""))
token = os.environ.get('TOKEN', '')
botid = token.split(':')[0]
FLOOD = 500
LAZY_PIC = os.environ.get("LAZY_PIC", "")

# Part of Day --------------------
currentTime = datetime.datetime.now()

if currentTime.hour < 12:
    wish = "❤️ Good morning sweetheart ❤️"
elif 12 <= currentTime.hour < 12:
    wish = '🤍 Good afternoon my Love 🤍'
else:
    wish = '🦋 Good evening baby 🦋'

# -------------------------------

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    old = insert(int(message.chat.id))
    try:
        id = message.text.split(' ')[1]
    except:
        txt = f"""Hello {wish} {message.from_user.first_name } \n\nI am a file renamer bot. Please send any Telegram document, video, or audio and enter a new filename to rename it."""
        await message.reply_photo(photo=LAZY_PIC,
                                  caption=txt,
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton("🔺 Update Channel 🔺", url="https://t.me/LazyDeveloper")],
                                       [InlineKeyboardButton("🦋 Subscribe us 🦋", url="https://youtube.com/@LazyDeveloperr")],
                                       [InlineKeyboardButton("Support Group", url='https://t.me/LazyPrincessSupport'),
                                        InlineKeyboardButton("Movie Channel", url='https://t.me/real_MoviesAdda2')],
                                       [InlineKeyboardButton("☕ Buy Me A Coffee ☕", url='https://p.paytm.me/xCTH/vo37hii9')]
                                       ]))
        return
    if id:
        if old == True:
            try:
                await client.send_message(id, "Your friend is already using our bot.")
                await message.reply_photo(photo=LAZY_PIC,
                                          caption=txt,
                                          reply_markup=InlineKeyboardMarkup(
                                              [[InlineKeyboardButton("🔺 Update Channel 🔺", url="https://t.me/LazyDeveloper")],
                                               [InlineKeyboardButton("🦋 Subscribe us 🦋", url="https://youtube.com/@LazyDeveloperr")],
                                               [InlineKeyboardButton("Support Group", url='https://t.me/LazyPrincessSupport'),
                                                InlineKeyboardButton("Movie Channel", url='https://t.me/real_MoviesAdda2')],
                                               [InlineKeyboardButton("☕ Buy Me A Coffee ☕", url='https://p.paytm.me/xCTH/vo37hii9')]
                                               ]))
            except:
                return
        else:
            await client.send_message(id, "Congrats! You won 100MB upload limit.")
            _user_ = find_one(int(id))
            limit = _user_["uploadlimit"]
            new_limit = limit + 104857600
            uploadlimit(int(id), new_limit)
            await message.reply_text(text=f"""
Hello {wish} {message.from_user.first_name }\n\n
I am a file renamer bot. Please send any Telegram document, video, or audio and enter a new filename to rename it.
""", reply_to_message_id=message.id,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton("🔺 Update Channel 🔺", url="https://t.me/LazyDeveloper")],
                                          [InlineKeyboardButton("🦋 Subscribe us 🦋", url="https://youtube.com/@LazyDeveloperr")],
                                          [InlineKeyboardButton("Support Group", url='https://t.me/LazyPrincessSupport'),
                                           InlineKeyboardButton("Movie Channel", url='https://t.me/real_MoviesAdda2')],
                                          [InlineKeyboardButton("☕ Buy Me A Coffee ☕", url='https://p.paytm.me/xCTH/vo37hii9')]
                                          ]))


@Client.on_message((filters.private & (filters.document | filters.audio | filters.video)) | filters.channel & (filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    update_channel = CHANNEL
    user_id = message.from_user.id
    if update_channel:
        try:
            await client.get_chat_member(update_channel, user_id)
        except UserNotParticipant:
            _newus = find_one(message.from_user.id)
            user = _newus["usertype"]
            await message.reply_text("**__You are not subscribed to my channel__** ",
                                     reply_to_message_id=message.id,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton("🔺 Update Channel 🔺", url=f"https://t.me/{update_channel}")]]))
            await client.send_message(log_channel, f"🦋 #GangsterBaby_LOGS 🦋,\n\n**ID** : `{user_id}`\n**Name**: {message.from_user.first_name} {message.from_user.last_name}\n**User-Plan** : {user}\n\n ",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔺 Restrict User ( **pm** ) 🔺", callback_data="ceasepower")]]))
            return

    try:
        bot_data = find_one(int(botid))
        prrename = bot_data['total_rename']
        prsize = bot_data['total_size']
        user_deta = find_one(user_id)
    except:
        await message.reply_text("Use the /about command first.")
        return

    try:
        used_date = user_deta["date"]
        buy_date = user_deta["prexdate"]
        daily = user_deta["daily"]
        user_type = user_deta["usertype"]
    except:
        await message.reply_text(text=f"Hello dear {message.from_user.first_name}, we are currently working on this issue. Please try to rename files from another account.",
                                  reply_markup=InlineKeyboardMarkup([
                                      [InlineKeyboardButton("🦋 Contact LazyDeveloper 🦋", url='https://telegram.me/LazyDeveloper')],
                                      [InlineKeyboardButton("🔺 Watch Tutorial 🔺", url='https://youtube.com/@LazyDeveloperr')],
                                      [InlineKeyboardButton("🦋 Visit Channel  ", url='https://t.me/LazyDeveloper'),
                                       InlineKeyboardButton("  Support Group 🦋", url='https://t.me/LazyPrincessSupport')],
                                      [InlineKeyboardButton("☕ Buy Me A Coffee ☕", url='https://p.paytm.me/xCTH/vo37hii9')]
                                  ]))
        await message.reply_text(text=f"🦋")
        return

    c_time = time.time()

    if user_type == "Free":
        LIMIT = 600
    else:
        LIMIT = 50
    then = used_date + LIMIT
    left = round(then - c_time)
    conversion = datetime.timedelta(seconds=left)
    ltime = str(conversion)
    if left > 0:
        await message.reply_text(f"Sorry, I am currently busy. Please wait for {ltime}.", reply_to_message_id=message.id)
    else:
        media = await client.get_messages(message.chat.id, message.id)
        file = media.document or media.video or media.audio
        dcid = FileId.decode(file.file_id).dc_id
        filename = file.file_name
        value = 2147483648
        used_ = find_one(message.from_user.id)
        used = used_["used_limit"]
        limit = used_["uploadlimit"]
        expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
        if expi != 0:
            today = date_.today()
            pattern = '%Y-%m-%d'
            epcho = int(time.mktime(time.strptime(str(today), pattern)))
            daily_(message.from_user.id, epcho)
            used_limit(message.from_user.id, 0)
        remain = limit - used
        if remain < int(file.file_size):
            await message.reply_text(f"100% of daily {humanize.naturalsize(limit)} data quota exhausted.\n\nFile size detected: {humanize.naturalsize(file.file_size)}\nUsed Daily Limit: {humanize.naturalsize(used)}\n\nYou have only **{humanize.naturalsize(remain)}** left on your account.\nIf you want to rename a larger file, upgrade your plan.",
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Upgrade 💰💳", callback_data="upgrade")]]))
            return
        if value < file.file_size:
            if STRING:
                if buy_date == None:
                    await message.reply_text(f"You can't upload more than {humanize.naturalsize(limit)}.\nUsed daily limit: {humanize.naturalsize(used)}.",
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Upgrade 💰💳", callback_data="upgrade")]]))
                    return
                pre_check = check_expi(buy_date)
                if pre_check == True:
                    await message.reply_text(f"What do you want me to do with this file?\n\nFile Name: {filename}\nFile Size: {humanize.naturalsize(file.file_size)}\nDc ID: {dcid}",
                                             reply_to_message_id=message.id,
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Rename", callback_data="rename"),
                                                                                InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))
                    total_rename(int(botid), prrename)
                    total_size(int(botid), prsize, file.file_size)
                else:
                    uploadlimit(message.from_user.id, 1288490188)
                    usertype(message.from_user.id, "Free")
                    await message.reply_text(f'Your plan expired on {buy_date}', quote=True)
                    return
            else:
                await message.reply_text("Can't upload files bigger than 2GB.")
                return
        else:
            if buy_date:
                pre_check = check_expi(buy_date)
                if pre_check == False:
                    uploadlimit(message.from_user.id, 1288490188)
                    usertype(message.from_user.id, "Free")
            filesize = humanize.naturalsize(file.file_size)
            fileid = file.file_id
            total_rename(int(botid), prrename)
            total_size(int(botid), prsize, file.file_size)
            await message.reply_text(f"What do you want me to do with this file?\n\nFile Name: {filename}\nFile Size: {filesize}\nDc ID: {dcid}",
                                     reply_to_message_id=message.id,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton("📝 Rename", callback_data="rename"),
                                           InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))

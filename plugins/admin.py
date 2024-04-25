from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
import os
from helper.date import add_date
from helper.database import uploadlimit, usertype, addpre

# Get environment variables
ADMIN = int(os.environ.get("ADMIN", 1484670284))
log_channel = int(os.environ.get("LOG_CHANNEL", ""))

# Error handling for admin-restricted commands
def admin_required(func):
    async def wrapper(bot, message):
        if not await bot.get_chat_member(message.chat.id, bot.me.id).is_chat_admin():
            await message.reply_text("Admin privileges required.")
            return
        await func(bot, message)
    return wrapper

# Initialize Pyrogram client
app = Client("my_bot")

# Command handler for the /warn command
@app.on_message(filters.private & filters.user(ADMIN) & filters.command(["warn"]))
@admin_required
async def warn(bot, message):
    try:
        user_id, *reason = message.text.split(' ', 2)[1:]
        reason = ' '.join(reason)
        await message.reply_text("User Notified Successfully")
        await bot.send_message(chat_id=int(user_id), text=reason)
    except Exception as e:
        await message.reply_text("User Not Notified Successfully 😔")

# Command handler for the /addpremium command
@app.on_message(filters.private & filters.user(ADMIN) & filters.command(["addpremium"]))
@admin_required
async def buypremium(bot, message):
    await message.reply_text("🦋 Select Plan to upgrade...", quote=True, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("🪙 Silver", callback_data="vip1")],
        [InlineKeyboardButton("💫Gold", callback_data="vip2")],
        [InlineKeyboardButton("💎 Diamond", callback_data="vip3")]
    ]))

# Command handler for the /ceasepower command
@app.on_message((filters.channel | filters.private) & filters.user(ADMIN) & filters.command(["ceasepower"]))
@admin_required
async def ceasepremium(bot, message):
    await message.reply_text(" POWER CEASE MODE", quote=True, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("•× Limit 500MB ×•", callback_data="cp1"),
         InlineKeyboardButton("•× Limit 100MB ×•", callback_data="cp2")],
        [InlineKeyboardButton("•••× CEASE ALL POWER ×•••", callback_data="cp3")]
    ]))

# Command handler for the /resetpower command
@app.on_message((filters.channel | filters.private) & filters.user(ADMIN) & filters.command(["resetpower"]))
@admin_required
async def resetpower(bot, message):
    await message.reply_text(text=f"Do you really want to reset daily limit to default data limit 1.2GB ?",quote=True,reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("• YES ! Set as Default •",callback_data = "dft")],
        [InlineKeyboardButton("❌ Cancel ❌",callback_data = "cancel")]
    ]))

# Callback query handler for upgrading to Silver
@app.on_callback_query(filters.regex('vip1'))
async def vip1(bot, update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    inlimit = 10737418240
    uploadlimit(int(user_id), 10737418240)
    usertype(int(user_id),"🪙 **SILVER**")
    addpre(int(user_id))
    await update.message.edit("Added successfully To Premium Upload limit 10 GB")
    await bot.send_message(user_id,"Hey you are Upgraded To silver. check your plan here /myplan")
    await bot.send_message(log_channel,f"⚡️ Plan Upgraded successfully 💥\n\nHey you are Upgraded To silver. check your plan here /myplan")

# Callback query handler for upgrading to Gold
@app.on_callback_query(filters.regex('vip2'))
async def vip2(bot, update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    inlimit = 53687091200
    uploadlimit(int(user_id), 53687091200)
    usertype(int(user_id),"💫 **GOLD**")
    addpre(int(user_id))
    await update.message.edit("Added successfully To Premium Upload limit 50 GB")
    await bot.send_message(user_id,"Hey you are Upgraded To Gold. check your plan here /myplan")
    await bot.send_message(log_channel, "⚡️ Plan Upgraded successfully 💥\n\nHey you are Upgraded To Gold. check your plan here /myplan")

# Callback query handler for upgrading to Diamond
@app.on_callback_query(filters.regex('vip3'))
async def vip3(bot, update):
    id = update.message.reply_to_message.text.split("/addpremium")
    user_id = id[1].replace(" ", "")
    inlimit = 107374182400
    uploadlimit(int(user_id), 107374182400)
    usertype(int(user_id),"💎 **DIAMOND**")
    addpre(int(user_id))
    await update.message.edit("Added successfully To Premium Upload limit 100 GB")
    await bot.send_message(user_id,"Hey you are Upgraded To Diamond. check your plan here /myplan")
    await bot.send_message(log_channel, "⚡️ Plan Upgraded successfully 💥\n\nHey you are Upgraded To Diamond. check your plan here /myplan")


# Callback query handler for CEASE POWER MODE option 1
@app.on_callback_query(filters.regex('cp1'))
async def cp1(bot, update):
    id = update.message.reply_to_message.text.split("/ceasepower")
    user_id = id[1].replace(" ", "")
    inlimit = 524288000
    uploadlimit(int(user_id), 524288000)
    usertype(int(user_id),"**ACCOUNT DOWNGRADED**")
    addpre(int(user_id))
    await update.message.edit("ACCOUNT DOWNGRADED\nThe user can only use 100MB/day from Data quota")
    await bot.send_message(user_id,"⚠️ Warning ⚠️\n\n- ACCOUNT DOWNGRADED\nYou can only use 500MB/day from Data quota.\nCheck your plan here - /myplan\n- Contact Admin 🦋<a href='https://t.me/+Tv3IyViX0uw1ZWI1'>**LazyDeveloper**</a>🦋")
    
# Callback query handler for CEASE POWER MODE option 2
@app.on_callback_query(filters.regex('cp2'))
async def cp2(bot, update):
    id = update.message.reply_to_message.text.split("/ceasepower")
    user_id = id[1].replace(" ", "")
    inlimit = 104857600
    uploadlimit(int(user_id), 104857600)
    usertype(int(user_id),"**ACCOUNT DOWNGRADED Lv-2**")
    addpre(int(user_id))
    await update.message.edit("ACCOUNT DOWNGRADED to Level 2\nThe user can only use 100MB/day from Data quota")
    await bot.send_message(user_id,"⛔️ Last Warning ⛔️\n\n- ACCOUNT DOWNGRADED to Level 2\nYou can only use 100MB/day from Data quota.\nCheck your plan here - /myplan\n- Contact Admin 🦋")


# Callback query handler for resetting power
@app.on_callback_query(filters.regex('dft'))
async def dft(bot, update):
    id = update.message.reply_to_message.text.split("/resetpower")
    user_id = id[1].replace(" ", "")
    inlimit = 1288490188
    uploadlimit(int(user_id), 1288490188)
    usertype(int(user_id),"**Free**")
    addpre(int(user_id))
    await update.message.edit("Daily Data limit has been reset successfully.\nThis account has default 1.2 GB renaming capacity ")
    await bot.send_message(user_id,"Your Daily Data limit has been reset successfully.\n\nCheck your plan here - /myplan\n- Contact Admin 🦋")


# Start the bot
app.run()

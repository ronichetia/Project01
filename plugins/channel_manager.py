from pyrogram import Client, filters
from database import db
from config import Config

@Client.on_message(filters.command("addchannel") & filters.user(Config.ADMINS))
async def add_channel(client, message):
    try:
        cmd, ch_id, ch_name = message.text.split(" ", 2)
        await db.add_channel(int(ch_id), ch_name)
        await message.reply_text(f"> ✅ **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗔𝗱𝗱𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!**\n\n**𝗜𝗗:** `{ch_id}`\n**𝗡𝗮𝗺𝗲:** {ch_name}")
    except ValueError:
        await message.reply_text("❌ **𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗼𝗿𝗺𝗮𝘁!**\n𝖴𝗌𝖾: `/addchannel -100123456789 Channel_Name`")

@Client.on_message(filters.command("delchannel") & filters.user(Config.ADMINS))
async def del_channel(client, message):
    try:
        ch_id = int(message.text.split(" ")[1])
        await db.remove_channel(ch_id)
        await message.reply_text(f"> 🗑️ **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗥𝗲𝗺𝗼𝘃𝗲𝗱:** `{ch_id}`")
    except:
        await message.reply_text("❌ **𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗼𝗿𝗺𝗮𝘁!**\n𝖴𝗌𝖾: `/delchannel -100123456789`")
        
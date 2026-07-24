from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified, PeerIdInvalid
from config import Config
from database import db
import re
import secrets
import asyncio

# Temp dictionary bot run time ke liye
post_data = {} 

@Client.on_message((filters.document | filters.video) & filters.user(Config.ADMINS) & filters.private)
async def handle_video_upload(client, message):
    file_id = message.document.file_id if message.document else message.video.file_id
    caption = message.caption or "No Caption"
    
    # 🔍 𝗦𝗺𝗮𝗿𝘁 𝗥𝗲𝗴𝗲𝘅 - 𝗘𝗽𝗶𝘀𝗼𝗱𝗲 𝗗𝗲𝘁𝗲𝗰𝘁𝗶𝗼𝗻
    match = re.search(r"(?i)(?:ep|episode|episodes)\s*0*(\d+)", caption)
    if match:
        ep_num = match.group(1)
        btn_name = f"🎬 𝗘𝗣𝗜𝗦𝗢𝗗𝗘 {ep_num}"
    else:
        btn_name = "📥 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗩𝗶𝗱𝗲𝗼"

    # 🔗 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗦𝗲𝗰𝘂𝗿𝗲 𝗦𝘁𝗮𝗿𝘁 𝗟𝗶𝗻𝗸 (Fixed: token_hex use kiya taaki '_' na aaye)
    file_hash = secrets.token_hex(6) 
    await db.save_file(file_id, file_hash, caption)
    bot_info = await client.get_me()
    start_link = f"https://t.me/{bot_info.username}?start={file_hash}"

    # 𝗦𝗮𝘃𝗲 𝘁𝗼 𝘁𝗲𝗺𝗽 𝗺𝗲𝗺𝗼𝗿𝘆 𝗳𝗼𝗿 𝗽𝗼𝘀𝘁𝗶𝗻𝗴
    post_data[file_hash] = {
        "file_id": file_id,
        "caption": caption,
        "btn_name": btn_name,
        "start_link": start_link
    }

    # 📺 𝗦𝗲𝗹𝗲𝗰𝘁 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗳𝗼𝗿 𝗣𝗼𝘀𝘁𝗶𝗻𝗴
    channels = await db.get_channels()
    if not channels:
        return await message.reply_text("❌ 𝖪𝗈𝗂 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖺𝖽𝖽𝖾𝖽 𝗇𝖺𝗁𝗂 𝗁𝖺𝗂. 𝖯𝖾𝗁𝗅𝖾 `/addchannel` 𝗄𝖺𝗋𝖾𝗂𝗇.")

    buttons = []
    # Fixed: _ ki jagah | (pipe) ka use kiya split ke liye
    for ch in channels:
        buttons.append([InlineKeyboardButton(ch['name'], callback_data=f"post|{file_hash}|{ch['_id']}")])
    
    await message.reply_text(
        f"> 🔗 **𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!**\n\n"
        f"**𝗙𝗶𝗹𝗲:** `{caption[:30]}...`\n"
        f"**𝗕𝘂𝘁𝘁𝗼𝗻 𝗡𝗮𝗺𝗲:** {btn_name}\n\n"
        f"👇 𝖯𝗈𝗌𝗍 𝗄𝖺𝗋𝗇𝖾 𝗄𝖾 𝗅𝗂𝗒𝖾 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝗌𝖾𝗅𝖾𝖼𝗍 𝗄𝖺𝗋𝖾𝗂𝗇:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex(r"^post\|"))
async def ask_timer(client, query: CallbackQuery):
    data = query.data.split("|")
    file_hash = data[1]
    channel_id = data[2]
    
    # ⏱️ 𝗔𝘀𝗸 𝗳𝗼𝗿 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹𝗲𝘁𝗲 𝗧𝗶𝗺𝗲𝗿
    text = "> ⏱️ **𝗦𝗲𝗹𝗲𝗰𝘁 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹𝗲𝘁𝗲 𝗧𝗶𝗺𝗲𝗿**\n\n𝖯𝗈𝗌𝗍 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗆𝖾 𝗄𝗂𝗍𝗇𝖾 𝗍𝗂𝗆𝖾 𝗍𝖺𝗄 𝗋𝖺𝗄𝗁𝗇𝗂 𝗁𝖺𝗂?"
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("10 Minutes", callback_data=f"send|{file_hash}|{channel_id}|600"),
         InlineKeyboardButton("1 Hour", callback_data=f"send|{file_hash}|{channel_id}|3600")],
        [InlineKeyboardButton("1 Day", callback_data=f"send|{file_hash}|{channel_id}|86400"),
         InlineKeyboardButton("Skip (Permanent)", callback_data=f"send|{file_hash}|{channel_id}|0")]
    ])
    
    try:
        await query.message.edit(text, reply_markup=buttons)
    except MessageNotModified:
        await query.answer("You already selected this option!", show_alert=False)

@Client.on_callback_query(filters.regex(r"^send\|"))
async def final_post_to_channel(client, query: CallbackQuery):
    data = query.data.split("|")
    file_hash = data[1]
    channel_id = int(data[2])
    timer = int(data[3])
    
    p_data = post_data.get(file_hash)
    
    if not p_data:
         return await query.answer("❌ Error: Ye session expire ho gaya hai, kripya video wapas upload karein.", show_alert=True)

    # 🎨 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗠𝘂𝗹𝘁𝗶-𝗥𝗼𝘄 𝗕𝘂𝘁𝘁𝗼𝗻𝘀 𝗟𝗼𝗴𝗶𝗰
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(p_data["btn_name"], url=p_data["start_link"])],
        [InlineKeyboardButton("🔔 𝗨𝗽𝗱𝗮𝘁𝗲𝘀", url=Config.FSUB_INVITE_LINK), 
         InlineKeyboardButton("💬 𝗛𝗲𝗹𝗽", url=f"https://t.me/{(await client.get_me()).username}")]
    ])

    try:
        # Send message to channel
        sent_msg = await client.send_message(
            chat_id=channel_id,
            text=f"**{p_data['caption']}**",
            reply_markup=keyboard
        )
        await query.message.edit("> ✅ **𝗣𝗼𝘀𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗦𝗲𝗻𝘁 𝘁𝗼 𝗖𝗵𝗮𝗻𝗻𝗲𝗹!**")
        
    except PeerIdInvalid:
        # Agar bot channel me na ho ya id wrong ho
        return await query.message.edit("❌ **𝗘𝗿𝗿𝗼𝗿:** Bot ko channel nahi mil raha! Kya bot us channel me **Admin** hai? Kripya ID check karein.")
    except Exception as e:
        return await query.message.edit(f"❌ **𝗘𝗿𝗿𝗼𝗿:** `{str(e)}`")

    # ⏱️ 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗣𝗼𝘀𝘁 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹𝗲𝘁𝗲 𝗟𝗼𝗴𝗶𝗰
    if timer > 0:
        await asyncio.sleep(timer)
        try:
            await client.delete_messages(chat_id=channel_id, message_ids=sent_msg.id)
        except:
            pass

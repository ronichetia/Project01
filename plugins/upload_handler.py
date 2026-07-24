from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import db
import re
import secrets
import asyncio

# Temp dictionary bot run time ke liye
post_data = {} 

# ⏱️ Helper function: String Timer ("5m", "1h") ko seconds me convert karne ke liye
def parse_time(time_str):
    if not time_str or str(time_str).lower() in ["0", "off", "none"]:
        return 0
    time_str = str(time_str).lower()
    if time_str.endswith('s'): return int(time_str[:-1])
    if time_str.endswith('m'): return int(time_str[:-1]) * 60
    if time_str.endswith('h'): return int(time_str[:-1]) * 3600
    if time_str.endswith('d'): return int(time_str[:-1]) * 86400
    try:
        return int(time_str)
    except:
        return 0


@Client.on_message((filters.document | filters.video) & filters.user(Config.ADMINS) & filters.private)
async def handle_video_upload(client, message):
    file_id = message.document.file_id if message.document else message.video.file_id
    caption = message.caption or "No Caption"
    
    # 🔍 𝗦𝗺𝗮𝗿𝘁 𝗥𝗲𝗴𝗲𝘅 - 𝗘𝗽𝗶𝘀𝗼𝗱𝗲 𝗗𝗲𝘁𝗲𝗰𝘁𝗶𝗼𝗻 (Updated for E09, E.09, Ep09)
    match = re.search(r"(?i)(?:ep|episode|episodes|e)[\s_.\-]*0*(\d+)", caption)
    if match:
        ep_num = match.group(1)
        btn_name = f"🎬 𝗘𝗣𝗜𝗦𝗢𝗗𝗘 {ep_num}"
    else:
        btn_name = "📥 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗩𝗶𝗱𝗲𝗼" 

    # 🔗 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗦𝗲𝗰𝘂𝗿𝗲 𝗦𝘁𝗮𝗿𝘁 𝗟𝗶𝗻𝗸
    file_hash = secrets.token_urlsafe(8)
    await db.save_file(file_id, file_hash, caption)
    bot_info = await client.get_me()
    start_link = f"https://t.me/{bot_info.username}?start={file_hash}"

    # 𝗦𝗮𝘃𝗲 𝘁𝗼 𝘁𝗲𝗺𝗽 𝗺𝗲𝗺𝗼𝗿𝘆 𝗳𝗼𝗿 𝗽𝗼𝘀𝘁𝗶𝗻𝗴
    post_data[file_hash] = {
        "file_id": file_id,
        "caption": caption,
        "btn_name": btn_name,
        "start_link": start_link,
        "msg_id": message.id,       
        "chat_id": message.chat.id  
    }

    # 📺 𝗦𝗲𝗹𝗲𝗰𝘁 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗳𝗼𝗿 𝗣𝗼𝘀𝘁𝗶𝗻𝗴
    channels = await db.get_channels()
    if not channels:
        return await message.reply_text("❌ 𝖪𝗈𝗂 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖺𝖽𝖽𝖾𝖽 𝗇𝖺𝗁𝗂 𝗁𝖺𝗂. 𝖯𝖾𝗁𝗅𝖾 `/addchannel` 𝗄𝖺𝗋𝖾𝗂𝗇.")

    buttons = []
    for ch in channels:
        # ✅ Changed '_' to ':' here to prevent collision with token_urlsafe underscores
        buttons.append([InlineKeyboardButton(ch.get('name', 'Channel'), callback_data=f"post:{file_hash}:{ch['_id']}")])
    
    await message.reply_text(
        f"> 🔗 **𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!**\n\n"
        f"**𝗙𝗶𝗹𝗲:** `{caption[:30]}...`\n"
        f"**𝗕𝘂𝘁𝘁𝗼𝗻 𝗡𝗮𝗺𝗲:** {btn_name}\n\n"
        f"👇 𝖯𝗈𝗌𝗍 𝗄𝖺𝗋𝗇𝖾 𝗄𝖾 𝗅𝗂𝗒𝖾 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝗌𝖾𝗅𝖾𝖼𝗍 𝗄𝖺𝗋𝖾𝗂𝗇:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# 🚀 𝗙𝗮𝘀𝘁 𝗣𝗼𝘀𝘁𝗶𝗻𝗴 (Dynamic Links & Buttons Integrated)
@Client.on_callback_query(filters.regex(r"^post:"))
async def final_post_to_channel(client, query: CallbackQuery):
    data = query.data.split(":")
    file_hash = data[1]
    channel_id = int(data[2])
    
    p_data = post_data.get(file_hash)
    if not p_data:
        return await query.answer("❌ Data expired! Please re-upload the file.", show_alert=True)
        
    await query.message.edit("> ⏳ **𝗣𝗼𝘀𝘁𝗶𝗻𝗴 𝘁𝗼 𝗖𝗵𝗮𝗻𝗻𝗲𝗹...**")
    
    # 1️⃣ Channel Data Database Se Nikaalna
    channels = await db.get_channels()
    target_channel = next((ch for ch in channels if ch["_id"] == channel_id), None)
    
    if not target_channel:
        return await query.message.edit("❌ **Channel Database me nahi mila!**")

    # Values extract karna
    post_mode = target_channel.get("post_mode", "Link").capitalize()
    auto_del_str = target_channel.get("auto_delete", "0")
    poster_id = target_channel.get("poster_id")
    
    # Updated: Getting Description (Genres) and Channel Title
    description = target_channel.get("description", "")
    ch_title = target_channel.get("name", "")
    
    timer_seconds = parse_time(auto_del_str)
    sent_msg = None
    
    try:
        # 2️⃣ Post Mode ke Hisaab se Action Lena
        if post_mode == "Forward":
            # Original file ko channel me forward karega
            sent_msg = await client.forward_messages(
                chat_id=channel_id,
                from_chat_id=p_data["chat_id"],
                message_ids=p_data["msg_id"]
            )
        
        elif post_mode == "Copy":
            # Original file ko bina forwarded tag ke copy karega
            sent_msg = await client.copy_message(
                chat_id=channel_id,
                from_chat_id=p_data["chat_id"],
                message_id=p_data["msg_id"]
            )
            
        else: 
            # Default "Link" Mode (Poster Image + Description + Dynamic Buttons)
            
            # Fetch Global DB Settings for Links
            settings = await db.get_settings()
            bot_username = (await client.get_me()).username
            
            u_link = settings.get("updates_link") or Config.FSUB_INVITE_LINK
            h_link = settings.get("help_link") or f"https://t.me/{bot_username}"
            
            # Main Episode Download Button
            btn_rows = [
                [InlineKeyboardButton(p_data["btn_name"], url=p_data["start_link"])]
            ]
            
            # Dynamic Second Row (Updates / Help)
            second_row = []
            if u_link and str(u_link).lower() != "off":
                second_row.append(InlineKeyboardButton("🔔 𝗨𝗽𝗱𝗮𝘁𝗲𝘀", url=u_link))
            if h_link and str(h_link).lower() != "off":
                second_row.append(InlineKeyboardButton("💬 𝗛𝗲𝗹𝗽", url=h_link))
                
            if second_row:
                btn_rows.append(second_row)
                
            keyboard = InlineKeyboardMarkup(btn_rows)
            
            # Text Formatting (Updated to show Title and Genres instead of Caption and Description)
            post_text = f"**{ch_title}**\n\n" if ch_title else f"**{p_data['caption']}**\n\n"
            
            if description and description.lower() != "skipped":
                # User ne agar by mistake Genres: likh diya ho toh usko remove karke bas actual genres rakhega
                clean_genres = re.sub(r"(?i)^genres?:\s*", "", description)
                post_text += f"**Genres:** {clean_genres}"
                
            if poster_id:
                sent_msg = await client.send_photo(
                    chat_id=channel_id,
                    photo=poster_id,
                    caption=post_text,
                    reply_markup=keyboard
                )
            else:
                sent_msg = await client.send_message(
                    chat_id=channel_id,
                    text=post_text,
                    reply_markup=keyboard
                )
                
        await query.message.edit(f"> ✅ **𝗣𝗼𝘀𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗦𝗲𝗻𝘁!**\n\n**𝗠𝗼𝗱𝗲:** `{post_mode}`\n**𝗔𝘂𝘁𝗼-𝗗𝗲𝗹𝗲𝘁𝗲:** `{auto_del_str}`")
        
    except Exception as e:
        return await query.message.edit(f"❌ **Error While Posting:**\n`{e}`")

    # 3️⃣ Auto Delete Background Task
    if timer_seconds > 0 and sent_msg:
        asyncio.create_task(delete_post_later(client, channel_id, sent_msg.id, timer_seconds))


# Background Helper Task Timer ke liye
async def delete_post_later(client, chat_id, msg_id, delay):
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id=chat_id, message_ids=msg_id)
    except:
        pass

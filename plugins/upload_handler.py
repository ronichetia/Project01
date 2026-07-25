from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config, admin_filter
from database import db
import re
import secrets
import asyncio
import json

# Temp dictionary bot run time ke liye
post_data = {} 
user_batches = {} # Batch files temporary store karne ke liye

# ⏱️ Helper function
def parse_time(time_str):
    if not time_str or str(time_str).lower() in ["0", "off", "none"]: return 0
    time_str = str(time_str).lower()
    if time_str.endswith('s'): return int(time_str[:-1])
    if time_str.endswith('m'): return int(time_str[:-1]) * 60
    if time_str.endswith('h'): return int(time_str[:-1]) * 3600
    if time_str.endswith('d'): return int(time_str[:-1]) * 86400
    try: return int(time_str)
    except: return 0

# 🔗 Helper function
def format_url(url):
    if not url: return None
    url = str(url).strip()
    if not (url.startswith("http://") or url.startswith("https://") or url.startswith("tg://")):
        return f"https://{url}"
    return url

# 🔍 𝗦𝗺𝗮𝗿𝘁 𝗥𝗲𝗴𝗲𝘅 - 𝗘𝗽𝗶𝘀𝗼𝗱𝗲 𝗗𝗲𝘁𝗲𝗰𝘁𝗶𝗼𝗻 (S01EP05, epi01, e06, ep83, E1)
EP_REGEX = r"(?i)(?:s\d{1,2})?[\s_.\-]*(?:ep|episode|epi|e)[\s_.\-]*(\d+)"


# --- 🟢 BATCH MODE COMMANDS ---

@Client.on_message(filters.command("batch") & admin_filter & filters.private)
async def start_batch(client, message):
    user_batches[message.from_user.id] = []
    await message.reply_text("✅ **Batch Mode Started!**\n\nAb saari videos/documents send karein. Jab sab send ho jayein tab `/done` command bhejein.")

@Client.on_message(filters.command("cancel") & admin_filter & filters.private)
async def cancel_batch(client, message):
    if message.from_user.id in user_batches:
        del user_batches[message.from_user.id]
        await message.reply_text("❌ **Batch Mode Cancelled.**")


@Client.on_message(filters.command("done") & admin_filter & filters.private)
async def finish_batch(client, message):
    user_id = message.from_user.id
    if user_id not in user_batches or not user_batches[user_id]:
        return await message.reply_text("❌ **Koi files nahi mili!** Pehle `/batch` start karein.")

    files = user_batches[user_id]
    await message.reply_text(f"⏳ **Processing {len(files)} files...**")

    ep_numbers = []
    file_ids = []
    main_caption = files[0]['caption'] # Pehli video ka caption use karenge

    for f in files:
        file_ids.append(f['file_id'])
        match = re.search(EP_REGEX, f['caption'])
        if match:
            ep_numbers.append(int(match.group(1))) # 05 ko 5 bana dega

    # 🔗 Generate Batch Start Link
    file_hash = secrets.token_urlsafe(8)
    
    # Save as JSON string for multiple files
    await db.save_file(json.dumps(file_ids), file_hash, main_caption)
    bot_info = await client.get_me()
    start_link = f"https://t.me/{bot_info.username}?start={file_hash}"

    # 🎬 Dynamic Button Naming for Batch
    if ep_numbers:
        min_ep = min(ep_numbers)
        max_ep = max(ep_numbers)
        if min_ep == max_ep:
            btn_name = f"🎬 𝗘𝗣𝗜𝗦𝗢𝗗𝗘 {min_ep}"
        else:
            btn_name = f"🎬 𝗘𝗣𝗜𝗦𝗢𝗗𝗘 {min_ep} - {max_ep}"
    else:
        btn_name = f"📥 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 {len(files)} 𝗩𝗶𝗱𝗲𝗼𝘀"

    post_data[file_hash] = {
        "caption": main_caption,
        "btn_name": btn_name,
        "start_link": start_link,
        "msg_ids": [f['msg_id'] for f in files],       
        "chat_id": files[0]['chat_id'],
        "is_batch": True
    }

    del user_batches[user_id] # Clear state
    await send_channel_selection(message, file_hash, main_caption, btn_name)


# --- 🟢 FILE UPLOAD HANDLER ---

@Client.on_message((filters.document | filters.video) & admin_filter & filters.private)
async def handle_video_upload(client, message):
    user_id = message.from_user.id
    file_id = message.document.file_id if message.document else message.video.file_id
    caption = message.caption or "No Caption"

    # Agar batch mode on hai, toh files batch me add hongi
    if user_id in user_batches:
        user_batches[user_id].append({
            "file_id": file_id,
            "caption": caption,
            "msg_id": message.id,
            "chat_id": message.chat.id
        })
        return await message.reply_text(f"✅ **File added to batch!** (Total: {len(user_batches[user_id])})\n_Jab done ho jaye tab /done bhejein._", quote=True)

    # 🔍 Single File Upload Logic
    match = re.search(EP_REGEX, caption)
    if match:
        ep_num = int(match.group(1))
        btn_name = f"🎬 𝗘𝗣𝗜𝗦𝗢𝗗𝗘 {ep_num}"
    else:
        btn_name = "📥 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗩𝗶𝗱𝗲𝗼" 

    # 🔗 Generate Secure Start Link
    file_hash = secrets.token_urlsafe(8)
    await db.save_file(json.dumps([file_id]), file_hash, caption) # Single file ko bhi list me daala taki start me issue na ho
    
    bot_info = await client.get_me()
    start_link = f"https://t.me/{bot_info.username}?start={file_hash}"

    post_data[file_hash] = {
        "caption": caption,
        "btn_name": btn_name,
        "start_link": start_link,
        "msg_ids": [message.id],       
        "chat_id": message.chat.id,
        "is_batch": False
    }

    await send_channel_selection(message, file_hash, caption, btn_name)


# Helper: Send Channel List
async def send_channel_selection(message, file_hash, caption, btn_name):
    channels = await db.get_channels()
    if not channels:
        return await message.reply_text("❌ Koi channel added nahi hai. Pehle /addchannel karein.")

    buttons = [[InlineKeyboardButton(ch.get('name', 'Channel'), callback_data=f"post:{file_hash}:{ch['_id']}")] for ch in channels]
    
    await message.reply_text(
        f"> 🔗 **𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!**\n\n"
        f"**𝗙𝗶𝗹𝗲:** `{caption[:40]}...`\n"
        f"**𝗕𝘂𝘁𝘁𝗼𝗻 𝗡𝗮𝗺𝗲:** {btn_name}\n\n"
        f"👇 𝖯𝗈𝗌𝗍 𝗄𝖺𝗋𝗇𝖾 𝗄𝖾 𝗅𝗂𝗒𝖾 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝗌𝖾𝗅𝖾𝖼𝗍 𝗄𝖺𝗋𝖾𝗂𝗇:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# --- 🟢 FAST POSTING ---

@Client.on_callback_query(filters.regex(r"^post:"))
async def final_post_to_channel(client, query: CallbackQuery):
    data = query.data.split(":")
    file_hash = data[1]
    channel_id = int(data[2])
    
    p_data = post_data.get(file_hash)
    if not p_data:
        return await query.answer("❌ Data expired! Please re-upload.", show_alert=True)
        
    await query.message.edit("> ⏳ **𝗣𝗼𝘀𝘁𝗶𝗻𝗴 𝘁𝗼 𝗖𝗵𝗮𝗻𝗻𝗲𝗹...**")
    
    channels = await db.get_channels()
    target_channel = next((ch for ch in channels if ch["_id"] == channel_id), None)
    
    if not target_channel:
        return await query.message.edit("❌ **Channel Database me nahi mila!**")

    settings = await db.get_settings()
    post_mode = settings.get("post_mode", "Link").capitalize()
    auto_del_str = settings.get("auto_delete", "0")
    
    poster_id = target_channel.get("poster_id")
    description = target_channel.get("description", "")
    ch_title = target_channel.get("name", "")
    
    timer_seconds = parse_time(auto_del_str)
    sent_msg_ids = [] # Ek ya multiple post ki IDs
    
    try:
        if post_mode == "Forward":
            # Pyrogram forward_messages supports list of IDs directly
            sent_msgs = await client.forward_messages(
                chat_id=channel_id,
                from_chat_id=p_data["chat_id"],
                message_ids=p_data["msg_ids"]
            )
            # Handle if single message returned instead of list
            if not isinstance(sent_msgs, list):
                sent_msgs = [sent_msgs]
            sent_msg_ids = [m.id for m in sent_msgs]
            
        elif post_mode == "Copy":
            for mid in p_data["msg_ids"]:
                msg = await client.copy_message(
                    chat_id=channel_id,
                    from_chat_id=p_data["chat_id"],
                    message_id=mid
                )
                sent_msg_ids.append(msg.id)
                await asyncio.sleep(1) # Batch copy rate-limit prevention
                
        else: # Link Mode
            btn_rows = [[InlineKeyboardButton(p_data["btn_name"], url=format_url(p_data["start_link"]))]]
            post_buttons = settings.get("post_buttons", [])
            
            if post_buttons:
                current_row = []
                for btn in post_buttons:
                    valid_url = format_url(btn.get("url", ""))
                    if valid_url: current_row.append(InlineKeyboardButton(btn["name"], url=valid_url))
                    if len(current_row) == 2:  
                        btn_rows.append(current_row)
                        current_row = []
                if current_row: btn_rows.append(current_row)
            else:
                bot_username = (await client.get_me()).username
                btn_rows.append([InlineKeyboardButton("💬 𝗛𝗲𝗹𝗽", url=f"https://t.me/{bot_username}")])
                
            keyboard = InlineKeyboardMarkup(btn_rows)
            post_text = f"**{ch_title}**\n\n" if ch_title else f"**{p_data['caption']}**\n\n"
            
            if description and description.lower() != "skipped":
                clean_genres = re.sub(r"(?i)^genres?:\s*", "", description)
                post_text += f"**Genres:** {clean_genres}"
                
            if poster_id:
                msg = await client.send_photo(channel_id, photo=poster_id, caption=post_text, reply_markup=keyboard)
            else:
                msg = await client.send_message(channel_id, text=post_text, reply_markup=keyboard)
            
            sent_msg_ids = [msg.id]
                
        await query.message.edit(f"> ✅ **𝗣𝗼𝘀𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗦𝗲𝗻𝘁!**\n\n**𝗠𝗼𝗱𝗲:** `{post_mode}`\n**𝗔𝘂𝘁𝗼-𝗗𝗲𝗹𝗲𝘁𝗲:** `{auto_del_str}`")
        
    except Exception as e:
        return await query.message.edit(f"❌ **Error While Posting:**\n`{e}`")

    # 🗑️ Auto Delete Background Task
    if timer_seconds > 0:
        if sent_msg_ids:
            asyncio.create_task(delete_post_later(client, channel_id, sent_msg_ids, timer_seconds))
        
        asyncio.create_task(delete_post_later(client, p_data["chat_id"], p_data["msg_ids"], timer_seconds))
        asyncio.create_task(delete_post_later(client, query.message.chat.id, [query.message.id], timer_seconds))

# Background Helper Task (Supports both single ID and list of IDs)
async def delete_post_later(client, chat_id, msg_ids, delay):
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id=chat_id, message_ids=msg_ids)
    except:
        pass

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from config import Config
import asyncio
import re

# ==================== 1. ADD CHANNEL COMMAND (Step-by-Step) ====================
@Client.on_message(filters.command("addchannel") & filters.user(Config.ADMINS))
async def add_channel_step_by_step(client, message):
    chat = message.chat
    
    # 🔴 Red/Blue Buttons Format (Like Video)
    cancel_btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 BACK", callback_data="cancel_flow"),
         InlineKeyboardButton("❌ CLOSE", callback_data="cancel_flow")]
    ])

    try:
        # STEP 1: CHANNEL ID
        id_msg = await chat.ask(
            "➕ **Add channel**\n\nSend the channel ID (numeric, e.g. `-1001234567890`).\n\nSend `/cancel` to go back.",
            timeout=120
        )
        if id_msg.text.lower() == "/cancel":
            return await message.reply("🚫 **Cancelled.**")
        ch_id = int(id_msg.text)

        # 🛡️ VERIFICATION STEP: Check if bot is an Admin in the channel (Peer ID Fix)
        try:
            verify_chat = await client.get_chat(ch_id)
        except Exception as e:
            return await message.reply(
                f"❌ **Error:** `Peer id invalid`\n\n"
                f"⚠️ **Main is channel ko access nahi kar pa raha hu!**\n"
                f"Kripya pehle mujhe is channel (`{ch_id}`) mein **Admin** banayein, uske baad add karein.\n\n"
                f"**System Error:** `{e}`"
            )

        # STEP 2: TITLE
        fetched_title = verify_chat.title if verify_chat else "Unknown"
        title_msg = await chat.ask(
            f"Send the title for this channel (e.g. \"One Piece\"):\n\n**ID:** `{ch_id}`\n**Fetched Title:** `{fetched_title}`",
            reply_markup=cancel_btn, timeout=120
        )
        if title_msg.text.lower() == "/cancel": return
        title = title_msg.text

        # STEP 3: GENRES (Replaced Description)
        genre_msg = await chat.ask(
            "Send **Genres** for this channel (e.g., Romance, Drama) or send `/skip`:\n\n(No need to write 'Genres:', just send the names.)",
            reply_markup=cancel_btn, timeout=120
        )
        if genre_msg.text.lower() == "/cancel": return
        
        desc = ""
        if genre_msg.text.lower() != "/skip":
            # Agar user ne galti se 'Genres: Drama' likha hai to automatically clean kar dega
            desc = re.sub(r"(?i)^genres?:\s*", "", genre_msg.text)

        # STEP 4: POST MODE
        mode_msg = await chat.ask(
            "Choose post mode:\n\nType: `Link`, `Forward`, or `Copy`",
            reply_markup=cancel_btn, timeout=120
        )
        if mode_msg.text.lower() == "/cancel": return
        post_mode = mode_msg.text.capitalize()

        # STEP 5: AUTO DELETE TIMER (Dynamic Setup)
        timer_msg = await chat.ask(
            "Send auto-delete time:\n\n`30s` = 30 seconds\n`5m` = 5 minutes\n`2h` = 2 hours\n`1d` = 1 day\n`0` = off",
            reply_markup=cancel_btn, timeout=120
        )
        if timer_msg.text.lower() == "/cancel": return
        auto_del = timer_msg.text.lower()

        # STEP 6: POSTER IMAGE
        poster_msg = await chat.ask(
            "Send a poster image for this channel, or send `/skip` to skip:",
            reply_markup=cancel_btn, timeout=120
        )
        
        poster_id = None
        if poster_msg.photo:
            poster_id = poster_msg.photo.file_id

        # SAVE FULL DATA TO MONGODB
        channel_data = {
            "name": title,
            "description": desc,
            "post_mode": post_mode,
            "auto_delete": auto_del,
            "poster_id": poster_id
        }
        await db.add_channel(ch_id, channel_data)

        # FINAL SUCCESS MESSAGE (Video Format)
        success_text = (
            "✅ **Channel Added Successfully!**\n\n"
            f"**Title:** {title}\n"
            f"**ID:** `{ch_id}`\n"
            f"**Genres:** {desc if desc else 'Skipped'}\n"
            f"**Mode:** {post_mode}\n"
            f"**Auto-Delete:** {auto_del}\n"
        )

        if poster_id:
            await message.reply_photo(photo=poster_id, caption=success_text)
        else:
            await message.reply_text(success_text)

    except asyncio.TimeoutError:
        await message.reply("⏰ **Time is up! Process reset. Try again.**")
    except ValueError:
        await message.reply("❌ **Invalid ID provided! Channel ID must be numbers.**")


# Button cancel handler for Add Channel flow
@Client.on_callback_query(filters.regex("cancel_flow"))
async def cancel_flow_handler(client, query):
    await query.message.edit_text("🚫 **Process closed by Admin.**")


# ==================== 2. DELETE CHANNEL COMMAND ====================
@Client.on_message(filters.command("delchannel") & filters.user(Config.ADMINS))
async def del_channel(client, message):
    try:
        # Command se ID extract karega (e.g., /delchannel -100123456789)
        ch_id = int(message.text.split(" ")[1])
        await db.remove_channel(ch_id)
        await message.reply_text(f"> 🗑️ **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗥𝗲𝗺𝗼𝘃𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆:** `{ch_id}`")
    except IndexError:
        await message.reply_text("❌ **𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗼𝗿𝗺𝗮𝘁!**\n𝖴𝗌𝖾: `/delchannel -100123456789`")
    except ValueError:
        await message.reply_text("❌ **Invalid ID!**\nChannel ID numbers mein honi chahiye.")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{e}`")

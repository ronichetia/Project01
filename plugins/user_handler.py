from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import Config
from database import db
import asyncio

# 🛡️ 𝗦𝗺𝗮𝗿𝘁 𝗙-𝗦𝘂𝗯 𝗖𝗵𝗲𝗰𝗸𝗲𝗿 (Database + Config Connected)
async def check_fsub(client, user_id):
    settings = await db.get_settings()
    
    # Agar Admin ne Admin Panel se F-Sub OFF rakha hai, toh check skip kar do
    if not settings.get("fsub", False) or not Config.FSUB_CHANNEL:
        return True

    try:
        await client.get_chat_member(Config.FSUB_CHANNEL, user_id)
        return True
    except UserNotParticipant:
        return False
    except Exception:
        return True # Admin ne bot ko channel me admin nahi banaya hoga toh pass kar do

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    await db.add_user(user_id) # Broadcast ke liye user save karo
    
    args = message.text.split()
    settings = await db.get_settings()
    
    # -------------------------------------------------------------
    # 1️⃣ 𝗔𝗴𝗮𝗿 𝗨𝘀𝗲𝗿 𝗟𝗶𝗻𝗸/𝗕𝘂𝘁𝘁𝗼𝗻 (𝗗𝗲𝗲𝗽-𝗟𝗶𝗻𝗸) 𝘀𝗲 𝗔𝗮𝘆𝗮 𝗛𝗮𝗶 (𝗩𝗶𝗱𝗲𝗼 𝗙𝗶𝗹𝗲)
    # -------------------------------------------------------------
    if len(args) > 1:
        file_hash = args[1]
        
        # 🔒 𝗙-𝗦𝘂𝗯 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻
        if not await check_fsub(client, user_id):
            btn = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗧𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 𝗙𝗶𝗹𝗲", url=Config.FSUB_INVITE_LINK)],
                [InlineKeyboardButton("🔄 𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻", url=f"https://t.me/{(await client.get_me()).username}?start={file_hash}")]
            ])
            return await message.reply_text(
                "> 🔒 **𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱!**\n\n"
                "𝖥𝗂𝗅𝖾 𝖽𝖾𝗄𝗁𝗇𝖾 𝗄𝖾 𝗅𝗂𝗒𝖾 𝗉𝖾𝗁𝗅𝖾 𝗁𝖺𝗆𝖺𝗋𝖺 𝗆𝖺𝗂𝗇 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗃𝗈𝗂𝗇 𝗄𝖺𝗋𝖾𝗂𝗇. 𝖩𝗈𝗂𝗇 𝗄𝖺𝗋𝗇𝖾 𝗄𝖾 𝖻𝖺𝖺𝖽 **𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻** 𝗉𝖺𝗋 𝖼𝗅𝗂𝖼𝗄 𝗄𝖺𝗋𝖾𝗂𝗇.",
                reply_markup=btn
            )

        # 📂 𝗙𝗲𝘁𝗰𝗵 𝗙𝗶𝗹𝗲 𝗳𝗿𝗼𝗺 𝗗𝗕
        file_data = await db.get_file(file_hash)
        if not file_data:
            return await message.reply_text("❌ **𝖸𝖾 𝗅𝗂𝗇𝗄 𝖾𝗑𝗉𝗂𝗋𝖾 𝗁𝗈 𝖼𝗁𝗎𝗄𝗂 𝗁𝖺𝗂 𝗒𝖺 𝖿𝗂𝗅𝖾 𝖽𝖾𝗅𝖾𝗍𝖾 𝗄𝖺𝗋 𝖽𝗂 𝗀𝖺𝗒𝗂 𝗁𝖺𝗂.**")

        # ⏱️ Get Dynamic Timer (Fallback to Config if not set)
        auto_del_sec = settings.get("auto_delete", Config.AUTO_DELETE_TIME)
        del_min = auto_del_sec // 60

        # 📤 𝗦𝗲𝗻𝗱 𝗩𝗶𝗱𝗲𝗼 𝘁𝗼 𝗨𝘀𝗲𝗿
        sent_video = await client.send_cached_media(
            chat_id=message.chat.id,
            file_id=file_data["file_id"],
            caption=f"**{file_data['caption']}**\n\n> ⚠️ *𝖸𝖾 𝖿𝗂𝗅𝖾 {del_min} 𝗆𝗂𝗇𝗎𝗍𝖾𝗌 𝗆𝖾 𝖺𝗎𝗍𝗈-𝖽𝖾𝗅𝖾𝗍𝖾 𝗁𝗈 𝗃𝖺𝗒𝖾𝗀𝗂.*"
        )
        
        # 🗑️ 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹𝗲𝘁𝗲 𝗧𝗶𝗺𝗲𝗿
        await asyncio.sleep(auto_del_sec)
        try:
            await sent_video.delete()
            await message.reply_text("🗑️ **Your video was deleted due to Copyright Policy!**")
        except Exception:
            pass

    # -------------------------------------------------------------
    # 2️⃣ 𝗡𝗼𝗿𝗺𝗮𝗹 /𝘀𝘁𝗮𝗿𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 (𝗪𝗶𝘁𝗵 𝗡𝗲𝘄 𝗨𝗜 & 𝗕𝘂𝘁𝘁𝗼𝗻𝘀)
    # -------------------------------------------------------------
    else:
        # Custom Welcome Message Check
        custom_msg = settings.get("welcome_msg", "default")
        
        if custom_msg != "default":
            welcome_text = custom_msg
        else:
            welcome_text = (
                f"> 🌟 **𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 {(await client.get_me()).first_name}**\n\n"
                "Hello! Main ek premium file sharing bot hoon.\n"
                "Niche diye gaye buttons ka use karke explore karein:"
            )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦", callback_data="open_settings")],
            [InlineKeyboardButton("❓ 𝗛𝗲𝗹𝗽", callback_data="bot_help"),
             InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲", callback_data="close_panel")]
        ])
        
        await message.reply_text(welcome_text, reply_markup=buttons)

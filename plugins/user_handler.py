from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant
from config import Config
from database import db
import asyncio

# 🛡️ 𝗙-𝗦𝘂𝗯 𝗖𝗵𝗲𝗰𝗸𝗲𝗿 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻
async def check_fsub(client, user_id):
    if not Config.FSUB_CHANNEL:
        return True
    try:
        await client.get_chat_member(Config.FSUB_CHANNEL, user_id)
        return True
    except UserNotParticipant:
        return False
    except Exception:
        return True # Admin ne bot ko channel me admin nahi banaya hoga toh skip karo

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    await db.add_user(user_id) # Save user for Broadcast
    
    args = message.text.split()
    
    # Agar start link parameters ke sath hai (Matalab video link par click kiya hai)
    if len(args) > 1:
        file_hash = args[1]
        
        # 1. 𝗙-𝗦𝘂𝗯 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻
        if not await check_fsub(client, user_id):
            btn = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗧𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 𝗙𝗶𝗹𝗲", url=Config.FSUB_INVITE_LINK)],
                [InlineKeyboardButton("🔄 𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻", url=f"https://t.me/{(await client.get_me()).username}?start={file_hash}")]
            ])
            return await message.reply_text(
                "> 🔒 **𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱!**\n\n"
                "𝖥𝗂𝗅𝖾 𝖽𝖾𝗄𝗁𝗇𝖾 𝗄𝖾 𝗅𝗂𝗒𝖾 𝗉𝖾𝗁𝗅𝖾 𝗁𝖺𝗆𝖺𝗋𝖺 𝗆𝖺𝗂𝗇 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗃𝗈𝗂𝗇 𝗄𝖺𝗋𝖾𝗂𝗇. 𝖩𝗈𝗂𝗇 𝗄𝖺𝗋𝗇𝖾 𝗄𝖾 𝖻𝖺𝖺𝖽 𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻 𝗉𝖺𝗋 𝖼𝗅𝗂𝖼𝗄 𝗄𝖺𝗋𝖾𝗂𝗇.",
                reply_markup=btn
            )

        # 2. 𝗙𝗲𝘁𝗰𝗵 𝗙𝗶𝗹𝗲 𝗳𝗿𝗼𝗺 𝗗𝗕
        file_data = await db.get_file(file_hash)
        if not file_data:
            return await message.reply_text("❌ 𝖸𝖾 𝗅𝗂𝗇𝗄 𝖾𝗑𝗉𝗂𝗋𝖾 𝗁𝗈 𝖼𝗁𝗎𝗄𝗂 𝗁𝖺𝗂 𝗒𝖺 𝖿𝗂𝗅𝖾 𝖽𝖾𝗅𝖾𝗍𝖾 𝗄𝖺𝗋 𝖽𝗂 𝗀𝖺𝗒𝗂 𝗁𝖺𝗂.")

        # 3. 𝗦𝗲𝗻𝗱 𝗩𝗶𝗱𝗲𝗼 𝘁𝗼 𝗨𝘀𝗲𝗿
        sent_video = await client.send_cached_media(
            chat_id=message.chat.id,
            file_id=file_data["file_id"],
            caption=f"**{file_data['caption']}**\n\n> ⚠️ *𝖸𝖾 𝖿𝗂𝗅𝖾 {Config.AUTO_DELETE_TIME // 60} 𝗆𝗂𝗇𝗎𝗍𝖾𝗌 𝗆𝖾 𝖺𝗎𝗍𝗈-𝖽𝖾𝗅𝖾𝗍𝖾 𝗁𝗈 𝗃𝖺𝗒𝖾𝗀𝗂.*"
        )
        
        # 4. 𝗕𝗼𝘁 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹𝗲𝘁𝗲 𝗟𝗼𝗴𝗶𝗰 (Copyright Protection)
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        try:
            await sent_video.delete()
        except:
            pass

    else:
        # 𝗡𝗼𝗿𝗺𝗮𝗹 /𝘀𝘁𝗮𝗿𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲
        await message.reply_text(
            "> 🎬 **𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗕𝗼𝘁**\n\n"
            "𝖸𝖾 𝖾𝗄 𝖺𝗎𝗍𝗈-𝗉𝗈𝗌𝗍𝗂𝗇𝗀 𝖻𝗈𝗍 𝗁𝖺𝗂. 𝖥𝗂𝗅𝖾𝗌 𝗄𝖾 𝗅𝗂𝗇𝗄𝗌 𝗉𝖺𝗋 𝖼𝗅𝗂𝖼𝗄 𝗄𝖺𝗋𝗄𝖾 𝖺𝖺𝗉 𝗒𝖺𝗁𝖺𝗇 𝗏𝗂𝖽𝖾𝗈𝗌 𝖽𝖾𝗄𝗁 𝗌𝖺𝗄𝗍𝖾 𝗁𝖺𝗂𝗇."
        )
        
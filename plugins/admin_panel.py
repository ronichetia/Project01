from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import db
import asyncio

# 𝗔𝗱𝗺𝗶𝗻 𝗣𝗮𝗻𝗲𝗹 𝗠𝗲𝗻𝘂
@Client.on_message(filters.command("admin") & filters.user(Config.ADMINS))
async def admin_panel(client, message):
    text = (
        "> 👑 **𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗻𝘁𝗿𝗼𝗹 𝗣𝗮𝗻𝗲𝗹**\n\n"
        "**𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗕𝗼𝘀𝘀!** 𝖸𝖺𝗁𝖺𝗇 𝗌𝖾 𝖺𝖺𝗉 𝖻𝗈𝗍 𝗄𝗈 𝖼𝗈𝗇𝗍𝗋𝗈𝗅 𝗄𝖺𝗋 𝗌𝖺𝗄𝗍𝖾 𝗁𝖺𝗂𝗇.\n"
        "𝖪𝗂𝗌𝗂 𝖻𝗁𝗂 𝗈𝗉𝗍𝗂𝗈𝗇 𝗉𝖺𝗋 𝖼𝗅𝗂𝖼𝗄 𝗄𝖺𝗋𝖾𝗂𝗇:"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁", callback_data="admin_broadcast")],
        [InlineKeyboardButton("📺 𝗠𝗮𝗻𝗮𝗴𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀", callback_data="admin_channels")],
        [InlineKeyboardButton("⚙️ 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀", callback_data="admin_settings")],
        [InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲", callback_data="close_panel")]
    ])
    await message.reply_text(text, reply_markup=buttons)

# 𝗖𝗮𝗹𝗹𝗯𝗮𝗰𝗸 𝗛𝗮𝗻𝗱𝗹𝗲𝗿 𝗳𝗼𝗿 𝗣𝗮𝗻𝗲𝗹 (𝗘𝗱𝗶𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲)
@Client.on_callback_query(filters.regex(r"^admin_") | filters.regex(r"^close_panel"))
async def admin_callbacks(client, query: CallbackQuery):
    data = query.data
    
    if data == "close_panel":
        await query.message.delete()
        
    elif data == "admin_channels":
        text = "> 📺 **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁**\n\n𝖭𝖺𝗒𝖺 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖺𝖽𝖽 𝗄𝖺𝗋𝗇𝖾 𝗄𝖾 𝗅𝗂𝗒𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗎𝗌𝖾 𝗄𝖺𝗋𝖾𝗂𝗇:\n`/addchannel [Channel ID] [Channel Name]`"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="back_home")]])
        await query.message.edit(text, reply_markup=buttons)
        
    elif data == "admin_settings":
        text = "> ⚙️ **𝗕𝗼𝘁 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀**\n\n𝖥-𝖲𝗎𝖻 𝖺𝗎𝗋 𝖠𝗎𝗍𝗈-𝖣𝖾𝗅𝖾𝗍𝖾 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌:"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ 𝗙-𝗦𝘂𝗯: 𝗢𝗡", callback_data="toggle_fsub")],
            [InlineKeyboardButton("⏱️ 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹𝗲𝘁𝗲: 𝟭𝟬𝗺", callback_data="toggle_autodel")],
            [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="back_home")]
        ])
        await query.message.edit(text, reply_markup=buttons)
        
    elif data == "admin_broadcast":
        await query.answer("Broadcast feature is ready. Just reply to a message with /broadcast", show_alert=True)

@Client.on_callback_query(filters.regex("back_home"))
async def back_home(client, query: CallbackQuery):
    text = (
        "> 👑 **𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗻𝘁𝗿𝗼𝗹 𝗣𝗮𝗻𝗲𝗹**\n\n"
        "**𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗕𝗼𝘀𝘀!** 𝖸𝖺𝗁𝖺𝗇 𝗌𝖾 𝖺𝖺𝗉 𝖻𝗈𝗍 𝗄𝗈 𝖼𝗈𝗇𝗍𝗋𝗈𝗅 𝗄𝖺𝗋 𝗌𝖺𝗄𝗍𝖾 𝗁𝖺𝗂𝗇."
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁", callback_data="admin_broadcast")],
        [InlineKeyboardButton("📺 𝗠𝗮𝗻𝗮𝗴𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀", callback_data="admin_channels")],
        [InlineKeyboardButton("⚙️ 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀", callback_data="admin_settings")],
        [InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲", callback_data="close_panel")]
    ])
    await query.message.edit(text, reply_markup=buttons)

# 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗖𝗼𝗺𝗺𝗮𝗻𝗱
@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMINS) & filters.reply)
async def broadcast_msg(client, message):
    users = await db.get_all_users()
    msg = await message.reply("`Broadcasting Message...`")
    success, failed = 0, 0
    
    for user in users:
        try:
            await message.reply_to_message.copy(user["_id"])
            success += 1
            await asyncio.sleep(0.1) # Flood wait bachne ke liye
        except:
            failed += 1
            
    await msg.edit(f"> 📢 **𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱**\n\n✅ 𝖲𝗎𝖼𝖼𝖾𝗌𝗌: `{success}`\n❌ 𝖥𝖺𝗂𝗅𝖾𝖽: `{failed}`")
    
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database import db
import asyncio

# 𝗔𝗱𝗺𝗶𝗻 𝗣𝗮𝗻𝗲𝗹 𝗠𝗮𝗶𝗻 𝗠𝗲𝗻𝘂 (Screenshot Layout)
@Client.on_message(filters.command("admin") & filters.user(Config.ADMINS))
async def admin_panel(client, message):
    text = (
        "> 👑 **𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗻𝘁𝗿𝗼𝗹 𝗣𝗮𝗻𝗲𝗹**\n\n"
        "**𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗕𝗼𝘀𝘀!** 𝖸𝖺𝗁𝖺𝗇 𝗌𝖾 𝖺𝖺𝗉 𝖻𝗈𝗍 𝗄𝗈 𝖼𝗈𝗇𝗍𝗋𝗈𝗅 𝗄𝖺𝗋 𝗌𝖺𝗄𝗍𝖾 𝗁𝖺𝗂𝗇.\n"
        "𝖪𝗂𝗌𝗂 𝖻𝗁𝗂 𝗈𝗉𝗍𝗂𝗈𝗇 𝗉𝖺𝗋 𝖼𝗅𝗂𝖼𝗄 𝗄𝖺𝗋𝖾𝗂𝗇:"
    )
    # Screenshot jaisa exact layout
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⛩ 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 ⛩", callback_data="open_settings")],
        [InlineKeyboardButton("❓ 𝗛𝗲𝗹𝗽", callback_data="admin_help"),
         InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲", callback_data="close_panel")]
    ])
    await message.reply_text(text, reply_markup=buttons)

# 𝗖𝗮𝗹𝗹𝗯𝗮𝗰𝗸 𝗛𝗮𝗻𝗱𝗹𝗲𝗿 𝗳𝗼𝗿 𝗣𝗮𝗻𝗲𝗹 𝗕𝘂𝘁𝘁𝗼𝗻𝘀
@Client.on_callback_query(filters.regex(r"^(open_settings|admin_help|close_panel|admin_channels|toggle_fsub|toggle_autodel|back_home|admin_broadcast)$"))
async def admin_callbacks(client, query: CallbackQuery):
    data = query.data
    
    # ❌ CLOSE BUTTON
    if data == "close_panel":
        await query.message.delete()
        
    # ⛩ SETTINGS BUTTON (Opens inner controls)
    elif data == "open_settings":
        text = "> ⚙️ **𝗕𝗼𝘁 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 & 𝗖𝗼𝗻𝘁𝗿𝗼𝗹𝘀**\n\n𝖲𝖺𝖻𝗁𝗂 𝖺𝖽𝗆𝗂𝗇 𝖿𝖾𝖺𝗍𝗎𝗋𝖾𝗌 𝗒𝖺𝗁𝖺𝗇 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗁𝖺𝗂𝗇:"
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁", callback_data="admin_broadcast")],
            [InlineKeyboardButton("📺 𝗠𝗮𝗻𝗮𝗴𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀", callback_data="admin_channels")],
            [InlineKeyboardButton("✅ 𝗙-𝗦𝘂𝗯: 𝗢𝗡", callback_data="toggle_fsub"),
             InlineKeyboardButton("⏱️ 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹𝗲𝘁𝗲: 𝟭𝟬𝗺", callback_data="toggle_autodel")],
            [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="back_home")]
        ])
        await query.message.edit(text, reply_markup=buttons)

    # ❓ HELP BUTTON
    elif data == "admin_help":
        text = (
            "> ❓ **𝗔𝗱𝗺𝗶𝗻 𝗛𝗲𝗹𝗽 𝗠𝗲𝗻𝘂**\n\n"
            "**𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗟𝗶𝘀𝘁:**\n"
            "🔸 `/addchannel [ID] [Name]` - 𝖭𝖺𝗒𝖺 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖺𝖽𝖽 𝗄𝖺𝗋𝖾𝗂𝗇\n"
            "🔸 `/delchannel [ID]` - 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝗋𝖾𝗆𝗈𝗏𝖾 𝗄𝖺𝗋𝖾𝗂𝗇\n"
            "🔸 `/broadcast` - 𝖪𝗂𝗌𝗂 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗄𝗈 𝗋𝖾𝗉𝗅𝗒 𝗄𝖺𝗋𝗄𝖾 𝗌𝖺𝖻𝗄𝗈 𝖻𝗁𝖾𝗃𝖾𝗂𝗇\n\n"
            "**𝗛𝗼𝘄 𝗧𝗼 𝗣𝗼𝘀𝘁:**\n"
            "𝖡𝗈𝗍 𝗄𝗈 𝗏𝗂𝖽𝖾𝗈 𝖻𝗁𝖾𝗃𝖾𝗂𝗇 𝖺𝗎𝗋 𝖼𝖺𝗉𝗍𝗂𝗈𝗇 𝗆𝖾 '𝖤𝗉𝗂𝗌𝗈𝖽𝖾 1' 𝗒𝖺 '𝖤𝖯01' 𝗅𝗂𝗄𝗁𝖾𝗂𝗇, "
            "𝖻𝗈𝗍 𝖺𝗎𝗍𝗈𝗆𝖺𝗍𝗂𝖼𝖺𝗅𝗅𝗒 𝖻𝗎𝗍𝗍𝗈𝗇𝗌 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝗄𝖺𝗋 𝖽𝖾𝗀𝖺."
        )
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="back_home")]])
        await query.message.edit(text, reply_markup=buttons)

    # 📺 MANAGE CHANNELS BUTTON
    elif data == "admin_channels":
        text = "> 📺 **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁**\n\n𝖭𝖺𝗒𝖺 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖺𝖽𝖽 𝗄𝖺𝗋𝗇𝖾 𝗄𝖾 𝗅𝗂𝗒𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗎𝗌𝖾 𝗄𝖺𝗋𝖾𝗂𝗇:\n`/addchannel [Channel ID] [Channel Name]`"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="open_settings")]]) # Back to settings
        await query.message.edit(text, reply_markup=buttons)
        
    # 📢 BROADCAST ALERT
    elif data == "admin_broadcast":
        await query.answer("Broadcast ready! Just reply to any message with /broadcast", show_alert=True)

    # 🔙 BACK TO HOME (Screenshot Layout)
    elif data == "back_home":
        text = (
            "> 👑 **𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗻𝘁𝗿𝗼𝗹 𝗣𝗮𝗻𝗲𝗹**\n\n"
            "**𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗕𝗼𝘀𝘀!** 𝖸𝖺𝗁𝖺𝗇 𝗌𝖾 𝖺𝖺𝗉 𝖻𝗈𝗍 𝗄𝗈 𝖼𝗈𝗇𝗍𝗋𝗈𝗅 𝗄𝖺𝗋 𝗌𝖺𝗄𝗍𝖾 𝗁𝖺𝗂𝗇.\n"
            "𝖪𝗂𝗌𝗂 𝖻𝗁𝗂 𝗈𝗉𝗍𝗂𝗈𝗇 𝗉𝖺𝗋 𝖼𝗅𝗂𝖼𝗄 𝗄𝖺𝗋𝖾𝗂𝗇:"
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⛩ 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 ⛩", callback_data="open_settings")],
            [InlineKeyboardButton("❓ 𝗛𝗲𝗹𝗽", callback_data="admin_help"),
             InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲", callback_data="close_panel")]
        ])
        await query.message.edit(text, reply_markup=buttons)

# 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 (No changes here, perfectly fine)
@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMINS) & filters.reply)
async def broadcast_msg(client, message):
    users = await db.get_all_users()
    msg = await message.reply("`Broadcasting Message...`")
    success, failed = 0, 0
    
    for user in users:
        try:
            await message.reply_to_message.copy(user["_id"])
            success += 1
            await asyncio.sleep(0.1) 
        except:
            failed += 1
            
    await msg.edit(f"> 📢 **𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱**\n\n✅ 𝖲𝗎𝖼𝖼𝖾𝗌𝗌: `{success}`\n❌ 𝖥𝖺𝗂𝗅𝖾𝖽: `{failed}`")

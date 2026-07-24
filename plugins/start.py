from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
from config import Config
from database import db
import asyncio
import pyromod # Pucha gaya naya message lene ke liye

# ==================== 1. START / WELCOME COMMAND ====================
@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    if hasattr(db, "add_user"):
        await db.add_user(message.from_user.id)

    user_name = message.from_user.first_name
    text = (
        f"> 👋 **Hey {user_name}! Welcome to the Bot**\n\n"
        "𝖬𝖺𝗂𝗇 𝖺𝖺𝗉𝗄𝗂 𝖺𝗇𝗂𝗆𝖾 𝗏𝗂𝖽𝖾𝗈𝗌 𝖺𝗎𝗋 𝗅𝗂𝗇𝗄𝗌 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝗄𝖺𝗋𝗇𝖾 𝗆𝖾 𝗆𝖺𝖽𝖺𝖽 𝗄𝖺𝗋𝗎𝗇𝗀𝖺.\n"
        "𝖭𝗂𝖼𝗁𝖾 𝖽𝗂𝗒𝖾 𝗀𝖺𝗒𝖾 𝖻𝗎𝗍𝗍𝗈𝗇𝗌 𝗄𝖺 𝗎𝗌𝖾 𝗄𝖺𝗋𝗄𝖾 𝖾𝗑𝗉𝗅𝗈𝗋𝖾 𝗄𝖺𝗋𝖾𝗂𝗇:"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⛩️ 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 ⛩️", callback_data="open_settings")],
        [InlineKeyboardButton("❓ 𝗛𝗲𝗹𝗽", callback_data="user_help"),
         InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲", callback_data="close_panel")]
    ])
    await message.reply_text(text, reply_markup=buttons)


# ==================== 2. DIRECT ADMIN COMMAND ====================
@Client.on_message(filters.command("admin") & filters.user(Config.ADMINS))
async def admin_cmd(client, message):
    await send_admin_panel(message, is_edit=False)


# Helper function: Admin Panel Interface
async def send_admin_panel(message_or_query, is_edit=True):
    text = (
        "> 👑 **𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗻𝘁𝗿𝗼𝗹 𝗣𝗮𝗻𝗲𝗹**\n\n"
        "**𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗕𝗼𝘀𝘀!** 𝖸𝖺𝗁𝖺𝗇 𝗌𝖾 𝖺𝖺𝗉 𝖻𝗈𝗍 𝗄𝗂 𝗌𝖺𝖺𝗋𝗂 𝗌𝖾𝗍𝗍𝗂𝗇𝗀𝗌 𝖺𝗎𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌 𝖼𝗈𝗇𝗍𝗋𝗈𝗅 𝗄𝖺𝗋 𝗌𝖺𝗄𝗍𝖾 𝗁𝖺𝗂𝗇:"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘀", callback_data="admin_stats"),
         InlineKeyboardButton("📢 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁", callback_data="admin_broadcast")],
        [InlineKeyboardButton("📺 𝗠𝗮𝗻𝗮𝗴𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀", callback_data="admin_channels"),
         InlineKeyboardButton("⚙️ 𝗙-𝗦𝘂𝗯 / 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹", callback_data="admin_toggles")],
        [InlineKeyboardButton("📝 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗠𝘀𝗴", callback_data="admin_welcome"),
         InlineKeyboardButton("🔗 𝗣𝗼𝘀𝘁 𝗕𝘂𝘁𝘁𝗼𝗻𝘀", callback_data="admin_post_btns")], # 👇 NEW BUTTON ADDED HERE
        [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸 𝘁𝗼 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀", callback_data="open_settings")]
    ])

    if is_edit:
        await message_or_query.edit_text(text, reply_markup=buttons)
    else:
        await message_or_query.reply_text(text, reply_markup=buttons)


# Helper function: Toggles Menu (Dynamic Buttons)
async def render_toggles_menu(query):
    settings = await db.get_settings()
    fsub_on = settings.get("fsub", False)
    autodel = settings.get("auto_delete", 600)

    # Dynamic Texts Based on DB State
    fsub_text = "✅ 𝗙-𝗦𝘂𝗯: 𝗢𝗡" if fsub_on else "❌ 𝗙-𝗦𝘂𝗯: 𝗢𝗙𝗙"
    
    if autodel == 600: del_text = "⏱️ 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹: 𝟭𝟬𝗺"
    elif autodel == 3600: del_text = "⏱️ 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹: 𝟭𝗵"
    elif autodel == 86400: del_text = "⏱️ 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹: 𝟭𝗱"
    elif autodel == 0: del_text = "⏱️ 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹: 𝗢𝗙𝗙"
    else: del_text = f"⏱️ 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹: {autodel}s"

    text = "> ⚙️ **𝗕𝗼𝘁 𝗖𝗼𝗻𝘁𝗿𝗼𝗹 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀**\n\nYahan se aap Force-Sub aur Auto-Delete settings toggle kar sakte hain:"
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(fsub_text, callback_data="toggle_fsub"),
         InlineKeyboardButton(del_text, callback_data="toggle_autodel")],
        [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="admin_main_panel")]
    ])
    
    try:
        await query.message.edit_text(text, reply_markup=buttons)
    except MessageNotModified:
        pass


# ==================== 3. ALL CALLBACK HANDLERS ====================
@Client.on_callback_query()
async def main_callback_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    is_admin = user_id in Config.ADMINS

    try:
        # ❌ CLOSE BUTTON
        if data == "close_panel":
            await query.message.delete()

        # ⛩️ SETTINGS BUTTON
        elif data == "open_settings":
            text = (
                "> ⚙️ **𝗕𝗼𝘁 𝗜𝗻𝗳𝗼 & 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀**\n\n"
                "🤖 **ᴍʏ ɴᴀᴍᴇ:** Anime Shanu #1 • Hell's Paradise Season 2\n"
                "» **ᴄʀᴇᴀᴛᴏʀ:** Mɪᴋᴏʏᴏ\n"
                "» **ᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴛʏ:** Aᴇʀᴏ ʙᴏᴛs\n"
                "» **ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ:** sʜᴀɴᴜ ᴀɴɪᴍᴇ\n"
                "» **Sʜᴀɴᴜ Aɴɪᴍᴇ:** Sʜᴀɴᴜ Aɴɪᴍᴇ Cʜᴀᴛᴛɪɴ𝗀\n"
                "» **Sʜᴀɴᴜ Aɴɪᴍᴇ Nᴇᴡs:** Sʜᴀɴᴜ Aɴɪᴍᴇ Nᴇᴡs\n"
                "» **ᴅᴇᴠᴇʟᴏᴘᴇʀ:** Mɪᴋᴏʏᴏ"
            )
            btn_list = [
                [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="back_start"),
                 InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲", callback_data="close_panel")]
            ]
            if is_admin:
                btn_list.append([InlineKeyboardButton("👑 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗻𝘁𝗿𝗼𝗹𝘀", callback_data="admin_main_panel")])
            await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(btn_list))

        # 🔙 BACK TO START MENU
        elif data == "back_start":
            await start_cmd(client, query.message)

        # ❓ HELP BUTTON
        elif data == "user_help":
            text = (
                "> ❓ **𝗛𝗲𝗹𝗽 & 𝗜𝗻𝘀𝘁𝗿𝘂𝗰𝘁𝗶𝗼𝗻𝘀**\n\n"
                "• **𝖥𝗂𝗅𝖾𝗌 / 𝖠𝗇𝗂𝗆𝖾 𝖪𝖺𝗂𝗌𝖾 𝖣𝗁𝗎𝗇𝖽𝗁𝖾𝗂𝗇?**\n"
                "  Channel me diye gaye episode button par click karein aur bot me `/start` dabayein.\n\n"
                "• **𝖥𝗈𝗋𝖼𝖾 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇:**\n"
                "  Files download karne se pehle official channel join karna zaroori hai."
            )
            if is_admin:
                text += (
                    "\n\n👑 **𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:**\n"
                    "🔸 `/addchannel [ID]` - Channel add karein\n"
                    "🔸 `/delchannel [ID]` - Channel remove karein\n"
                    "🔸 `/broadcast` - Reply to message to broadcast"
                )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="back_start")]])
            await query.message.edit_text(text, reply_markup=buttons)

        # 👑 ADMIN PANEL ACCESS
        elif data == "admin_main_panel":
            if not is_admin: return await query.answer("❌ Aap Admin Nahi Hain!", show_alert=True)
            await send_admin_panel(query.message, is_edit=True)

        # 📺 MANAGE CHANNELS
        elif data == "admin_channels":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            text = (
                "> 📺 **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁**\n\n"
                "Naya channel add karne ke liye command:\n"
                "`/addchannel`\n\n"
                "Channel delete karne ke liye:\n"
                "`/delchannel [Channel ID]`\n\n"
                "💡 *Tip:* Agar PeerId error aaye toh channel se koi bhi message bot ko forward kar do."
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="admin_main_panel")]])
            await query.message.edit_text(text, reply_markup=buttons)

        # 📢 BROADCAST
        elif data == "admin_broadcast":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            await query.answer("📢 Broadcast ready! Kisi bhi message ko reply karke /broadcast likhein.", show_alert=True)

        # 📊 BOT STATS
        elif data == "admin_stats":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            users = await db.get_all_users()
            channels = await db.get_channels()
            text = (
                "> 📊 **𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀**\n\n"
                f"👤 **Total Users:** `{len(users)}`\n"
                f"📺 **Connected Channels:** `{len(channels)}`\n"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="admin_main_panel")]])
            await query.message.edit_text(text, reply_markup=buttons)

        # 📝 WELCOME MESSAGE MANAGER
        elif data == "admin_welcome":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            settings = await db.get_settings()
            curr_msg = settings.get("welcome_msg", "default")
            
            text = (
                "> 📝 **𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀**\n\n"
                f"**Current Message:**\n`{curr_msg}`\n\n"
                "Naya message set karne ke liye niche click karein, ya default par reset karein."
            )
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️ 𝗘𝗱𝗶𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲", callback_data="edit_welcome"),
                 InlineKeyboardButton("🔄 𝗥𝗲𝘀𝗲𝘁 𝗗𝗲𝗳𝗮𝘂𝗹𝘁", callback_data="reset_welcome")],
                [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="admin_main_panel")]
            ])
            await query.message.edit_text(text, reply_markup=buttons)

        elif data == "reset_welcome":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            await db.reset_welcome_msg()
            await query.answer("Message Reset to Default!", show_alert=False)
            # Re-render menu
            query.data = "admin_welcome"
            await main_callback_handler(client, query)

        elif data == "edit_welcome":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            # Asking new message dynamically
            ask_msg = await query.message.chat.ask("📝 **Send the new Welcome Message.**\n\n(Send `/cancel` to abort)", timeout=120)
            if ask_msg.text.lower() == "/cancel":
                return await ask_msg.reply("🚫 **Cancelled.**")
                
            await db.update_welcome_msg(ask_msg.text)
            await ask_msg.reply("✅ **New Welcome Message Set Successfully!**\nUse /admin to check again.")

        # 🔗 POST BUTTONS MANAGER (NEWLY ADDED)
        elif data == "admin_post_btns":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            settings = await db.get_settings()
            bot_username = (await client.get_me()).username
            
            u_link = settings.get("updates_link") or Config.FSUB_INVITE_LINK
            h_link = settings.get("help_link") or f"https://t.me/{bot_username}"
            
            text = (
                "> 🔗 **𝗠𝗮𝗻𝗮𝗴𝗲 𝗣𝗼𝘀𝘁 𝗕𝘂𝘁𝘁𝗼𝗻𝘀**\n\n"
                "Channel posts ke niche 'Updates' aur 'Help' buttons manage karein:\n"
                "💡 *Tip: Kisi button ko remove karne ke liye `OFF` bhein.*\n\n"
                f"**🔔 Updates Link:** `{u_link}`\n"
                f"**💬 Help Link:** `{h_link}`"
            )
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️ 𝗘𝗱𝗶𝘁 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗟𝗶𝗻𝗸", callback_data="edit_ulink")],
                [InlineKeyboardButton("✏️ 𝗘𝗱𝗶𝘁 𝗛𝗲𝗹𝗽 𝗟𝗶𝗻𝗸", callback_data="edit_hlink")],
                [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="admin_main_panel")]
            ])
            await query.message.edit_text(text, reply_markup=buttons, disable_web_page_preview=True)

        elif data == "edit_ulink":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            ask = await query.message.chat.ask("🔗 **Naya Updates Link bhejein:**\n\n(Button hatane ke liye `OFF` bhejein ya `/cancel` likhein)", timeout=120)
            if ask.text.lower() == "/cancel":
                return await ask.reply("🚫 **Cancelled.**")
            
            await db.update_setting("updates_link", ask.text.strip())
            await ask.reply("✅ **Updates Link Updated Successfully!**\nUse /admin to check again.")

        elif data == "edit_hlink":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            ask = await query.message.chat.ask("🔗 **Naya Help Link bhejein:**\n\n(Button hatane ke liye `OFF` bhejein ya `/cancel` likhein)", timeout=120)
            if ask.text.lower() == "/cancel":
                return await ask.reply("🚫 **Cancelled.**")
            
            await db.update_setting("help_link", ask.text.strip())
            await ask.reply("✅ **Help Link Updated Successfully!**\nUse /admin to check again.")


        # ⚙️ ADMIN TOGGLES MENU
        elif data == "admin_toggles":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            await render_toggles_menu(query)

        # 🔄 DYNAMIC TOGGLE LOGICS
        elif data == "toggle_fsub":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            await db.toggle_fsub()
            await query.answer("F-Sub Setting Toggled!", show_alert=False)
            await render_toggles_menu(query)

        elif data == "toggle_autodel":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            settings = await db.get_settings()
            curr = settings.get("auto_delete", 600)
            
            # Smart Cycle logic for Auto-Delete timers
            if curr == 600: new_val = 3600       # 10m -> 1h
            elif curr == 3600: new_val = 86400   # 1h -> 1d
            elif curr == 86400: new_val = 0      # 1d -> OFF
            else: new_val = 600                  # OFF -> 10m
            
            await db.set_auto_delete(new_val)
            await query.answer("Auto-Delete Timer Updated!", show_alert=False)
            await render_toggles_menu(query)

    except MessageNotModified:
        await query.answer()
    except Exception as e:
        print(f"Callback Error: {e}")


# ==================== 4. BROADCAST COMMAND ====================
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

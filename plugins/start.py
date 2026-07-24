from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
from config import Config
from database import db
import asyncio
import pyromod # Pucha gaya naya message lene ke liye

# ==================== HELPER FUNCTIONS ====================
# Start Menu Generate karne ke liye
def get_start_menu(user_name):
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
    return text, buttons

# Settings / Admin Menu Generate karne ke liye
async def get_settings_menu(client, is_admin):
    bot_info = await client.get_me()
    bot_name = bot_info.first_name
    
    # YAHAN APNE CHANNELS KE LINKS DAALEIN 👇
    text = (
        "> ⚙️ **𝗕𝗼𝘁 𝗜𝗻𝗳𝗼 & 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀**\n\n"
        f"🤖 **ᴍʏ ɴᴀᴍᴇ:** {bot_name} • Hell's Paradise Season 2\n"
        "» **ᴄʀᴇᴀᴛᴏʀ:** [Mɪᴋᴏʏᴏ](https://t.me/YourUsername)\n"
        "» **ᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴛʏ:** [Aᴇʀᴏ ʙᴏᴛs](https://t.me/YourCommunityLink)\n"
        "» **ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ:** [sʜᴀɴᴜ ᴀɴɪᴍᴇ](https://t.me/YourAnimeChannel)\n"
        "» **Sʜᴀɴᴜ Aɴɪᴍᴇ:** [Sʜᴀɴᴜ Aɴɪᴍᴇ Cʜᴀᴛᴛɪɴ𝗀](https://t.me/YourChatLink)\n"
        "» **Sʜᴀɴᴜ Aɴɪᴍᴇ Nᴇᴡs:** [Sʜᴀɴᴜ Aɴɪᴍᴇ Nᴇᴡs](https://t.me/YourNewsLink)\n"
        "» **ᴅᴇᴠᴇʟᴏᴘᴇʀ:** [Mɪᴋᴏʏᴏ](https://t.me/YourUsername)"
    )
    
    if is_admin:
        # Admin ko ye saare buttons dikhenge Settings me
        btn_list = [
            [InlineKeyboardButton("📊 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘀", callback_data="admin_stats"),
             InlineKeyboardButton("📢 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁", callback_data="admin_broadcast")],
            [InlineKeyboardButton("📺 𝗠𝗮𝗻𝗮𝗴𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀", callback_data="admin_channels"),
             InlineKeyboardButton("⚙️ 𝗙-𝗦𝘂𝗯 / 𝗔𝘂𝘁𝗼-𝗗𝗲𝗹", callback_data="admin_toggles")],
            [InlineKeyboardButton("📝 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗠𝘀𝗴", callback_data="admin_welcome"),
             InlineKeyboardButton("🔗 𝗣𝗼𝘀𝘁 𝗕𝘂𝘁𝘁𝗼𝗻𝘀", callback_data="admin_post_btns")],
            [InlineKeyboardButton("👥 𝗠𝗮𝗻𝗮𝗴𝗲 𝗔𝗱𝗺𝗶𝗻𝘀", callback_data="admin_manage")],
            [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="back_start"),
             InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲", callback_data="close_panel")]
        ]
    else:
        # Normal user ko sirf Back aur Close dikhega
        btn_list = [
            [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="back_start"),
             InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲", callback_data="close_panel")]
        ]
    return text, InlineKeyboardMarkup(btn_list)


# ==================== 1. START / WELCOME COMMAND ====================
@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    if hasattr(db, "add_user"):
        await db.add_user(message.from_user.id)

    # DEEP LINKING LOGIC
    if len(message.command) > 1:
        file_hash = message.command[1]
        file_data = await db.get_file(file_hash)
        
        if file_data:
            try:
                msg = await client.send_document(
                    chat_id=message.chat.id,
                    document=file_data["file_id"],
                    caption=file_data.get("caption", "Here is your file!")
                )
            except:
                msg = await client.send_video(
                    chat_id=message.chat.id,
                    video=file_data["file_id"],
                    caption=file_data.get("caption", "Here is your video!")
                )
            return
        else:
            await message.reply_text("❌ **File not found or expired!**")
            return

    # NORMAL START MENU
    text, buttons = get_start_menu(message.from_user.first_name)
    await message.reply_text(text, reply_markup=buttons)


# ==================== 2. ADMIN COMMANDS ====================
@Client.on_message(filters.command("admin") & filters.user(Config.ADMINS))
async def admin_cmd(client, message):
    # Ab /admin par bhi seedha settings menu khulega jisme saare buttons honge
    text, buttons = await get_settings_menu(client, is_admin=True)
    await message.reply_text(text, reply_markup=buttons, disable_web_page_preview=True)

@Client.on_message(filters.command("addadmin") & filters.user(Config.ADMINS))
async def add_admin_cmd(client, message):
    try:
        new_admin_id = int(message.command[1])
        Config.ADMINS = list(Config.ADMINS)
        if new_admin_id not in Config.ADMINS:
            Config.ADMINS.append(new_admin_id)
            await message.reply_text(f"> ✅ **𝗦𝘂𝗰𝗰𝗲𝘀𝘀:** 𝖴𝗌𝖾𝗋 `{new_admin_id}` 𝗄𝗈 𝖠𝖽𝗆𝗂𝗇 𝖻𝖺𝗇𝖺 𝖽𝗂𝗒𝖺 𝗀𝖺𝗒𝖺 𝗁𝖺𝗂!")
        else:
            await message.reply_text("⚠️ **𝖸𝖾 𝖴𝗌𝖾𝗋 𝗉𝖾𝗁𝗅𝖾 𝗌𝖾 𝗁𝗂 𝖠𝖽𝗆𝗂𝗇 𝗁𝖺𝗂!**")
    except IndexError:
        await message.reply_text("❌ **Format Galat Hai!**\nUse: `/addadmin UserID`")
    except ValueError:
        await message.reply_text("❌ **Invalid ID!** Sirf numbers enter karein.")

@Client.on_message(filters.command("deladmin") & filters.user(Config.ADMINS))
async def del_admin_cmd(client, message):
    try:
        del_admin_id = int(message.command[1])
        Config.ADMINS = list(Config.ADMINS)
        if del_admin_id in Config.ADMINS:
            Config.ADMINS.remove(del_admin_id)
            await message.reply_text(f"> 🗑️ **𝗦𝘂𝗰𝗰𝗲𝘀𝘀:** 𝖴𝗌𝖾𝗋 `{del_admin_id}` 𝗄𝗈 𝖠𝖽𝗆𝗂𝗇𝗌 𝗌𝖾 𝗁𝖺𝗍𝖺 𝖽𝗂𝗒𝖺 𝗀𝖺𝗒𝖺 𝗁𝖺𝗂.")
        else:
            await message.reply_text("⚠️ **𝖸𝖾 𝖴𝗌𝖾𝗋 𝖠𝖽𝗆𝗂𝗇 𝗅𝗂𝗌𝗍 𝗆𝖾 𝗇𝖺𝗁𝗂 𝗁𝖺𝗂!**")
    except IndexError:
        await message.reply_text("❌ **Format Galat Hai!**\nUse: `/deladmin UserID`")
    except ValueError:
        await message.reply_text("❌ **Invalid ID!** Sirf numbers enter karein.")


# Helper function: Toggles Menu (Dynamic Buttons)
async def render_toggles_menu(query):
    settings = await db.get_settings()
    fsub_on = settings.get("fsub", False)
    autodel = settings.get("auto_delete", 600)

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
        [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="open_settings")] # Updated to back to settings
    ])
    
    try:
        await query.message.edit_text(text, reply_markup=buttons)
    except MessageNotModified:
        pass


# ==================== 3. ALL CALLBACK HANDLERS ====================
@Client.on_callback_query(filters.regex(r"^(close_panel|open_settings|user_help|back_start|admin_|edit_|reset_|toggle_|add_admin|del_admin)"))
async def main_callback_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    is_admin = user_id in Config.ADMINS

    try:
        if data == "close_panel":
            await query.message.delete()

        elif data == "open_settings":
            text, buttons = await get_settings_menu(client, is_admin)
            
            # Agar purana message video/photo hai (jaise help video), toh delete karke naya bhejo
            if query.message.video or query.message.photo or query.message.document:
                await query.message.delete()
                await client.send_message(query.message.chat.id, text, reply_markup=buttons, disable_web_page_preview=True)
            else:
                await query.message.edit_text(text, reply_markup=buttons, disable_web_page_preview=True)

        elif data == "back_start":
            text, buttons = get_start_menu(query.from_user.first_name)
            
            # Agar current message media hai toh usko delete karke wapas start bhejo
            if query.message.video or query.message.photo or query.message.document:
                await query.message.delete()
                await client.send_message(query.message.chat.id, text, reply_markup=buttons)
            else:
                await query.message.edit_text(text, reply_markup=buttons)

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
                    "🔸 `/addadmin [ID]` - Naya admin add karein\n"
                    "🔸 `/deladmin [ID]` - Admin remove karein\n"
                    "🔸 `/broadcast` - Reply to msg to broadcast"
                )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="back_start")]])
            
            # 👇 YAHAN APNI TUTORIAL VIDEO KA LINK YA FILE_ID DAALEIN
            help_video = getattr(Config, "HELP_VIDEO", "https://t.me/telegram/183") # Example dummy video
            
            try:
                # Video bhejne ke liye current text message delete karte hain
                await query.message.delete()
                await client.send_video(
                    chat_id=query.message.chat.id,
                    video=help_video,
                    caption=text,
                    reply_markup=buttons
                )
            except:
                # Agar video nahi send ho paayi toh text format me help bhejega
                await client.send_message(query.message.chat.id, text, reply_markup=buttons)

        # ====== ADMIN SUB-MENUS (Ab inka Back button 'open_settings' par jayega) ======
        elif data == "admin_manage":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            text = (
                "> 👥 **𝗔𝗱𝗺𝗶𝗻 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁**\n\n"
                f"**Current Admins Count:** `{len(Config.ADMINS)}`\n\n"
                "Naya admin add ya remove karne ke liye buttons ka use karein ya seedha `/addadmin ID` command use karein."
            )
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ 𝗔𝗱𝗱 𝗔𝗱𝗺𝗶𝗻", callback_data="add_admin"),
                 InlineKeyboardButton("➖ 𝗥𝗲𝗺𝗼𝘃𝗲 𝗔𝗱𝗺𝗶𝗻", callback_data="del_admin")],
                [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="open_settings")]
            ])
            await query.message.edit_text(text, reply_markup=buttons)

        elif data == "add_admin":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            ask = await query.message.chat.ask("➕ **Naye Admin ka User ID bhejein:**\n\n(Cancel karne ke liye `/cancel` likhein)", timeout=120)
            if ask.text.lower() == "/cancel": return await ask.reply("🚫 **Cancelled.**")
            
            try:
                new_id = int(ask.text.strip())
                Config.ADMINS = list(Config.ADMINS)
                if new_id not in Config.ADMINS:
                    Config.ADMINS.append(new_id)
                    await ask.reply(f"✅ **User `{new_id}` ko Admin bana diya gaya hai!**\nUse /admin to verify.")
                else:
                    await ask.reply("⚠️ **Ye user pehle se admin hai!**")
            except ValueError:
                await ask.reply("❌ **Invalid ID! Sirf numbers allow hain.**")

        elif data == "del_admin":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            ask = await query.message.chat.ask("➖ **Jise Admin se hatana hai uska User ID bhejein:**\n\n(Cancel karne ke liye `/cancel` likhein)", timeout=120)
            if ask.text.lower() == "/cancel": return await ask.reply("🚫 **Cancelled.**")
            
            try:
                del_id = int(ask.text.strip())
                Config.ADMINS = list(Config.ADMINS)
                if del_id in Config.ADMINS:
                    Config.ADMINS.remove(del_id)
                    await ask.reply(f"🗑️ **User `{del_id}` ko Admins se hata diya gaya hai!**")
                else:
                    await ask.reply("⚠️ **Ye user Admin list me nahi hai!**")
            except ValueError:
                await ask.reply("❌ **Invalid ID! Sirf numbers allow hain.**")


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
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="open_settings")]])
            await query.message.edit_text(text, reply_markup=buttons)

        elif data == "admin_broadcast":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            await query.answer("📢 Broadcast ready! Kisi bhi message ko reply karke /broadcast likhein.", show_alert=True)

        elif data == "admin_stats":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            users = await db.get_all_users()
            channels = await db.get_channels()
            text = (
                "> 📊 **𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀**\n\n"
                f"👤 **Total Users:** `{len(users)}`\n"
                f"📺 **Connected Channels:** `{len(channels)}`\n"
                f"👥 **Total Admins:** `{len(Config.ADMINS)}`"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="open_settings")]])
            await query.message.edit_text(text, reply_markup=buttons)

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
                [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="open_settings")]
            ])
            await query.message.edit_text(text, reply_markup=buttons)

        elif data == "reset_welcome":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            await db.reset_welcome_msg()
            await query.answer("Message Reset to Default!", show_alert=False)
            query.data = "admin_welcome"
            await main_callback_handler(client, query)

        elif data == "edit_welcome":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            ask_msg = await query.message.chat.ask("📝 **Send the new Welcome Message.**\n\n(Send `/cancel` to abort)", timeout=120)
            if ask_msg.text.lower() == "/cancel":
                return await ask_msg.reply("🚫 **Cancelled.**")
                
            await db.update_welcome_msg(ask_msg.text)
            await ask_msg.reply("✅ **New Welcome Message Set Successfully!**\nUse /admin to check again.")

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
                [InlineKeyboardButton("🔙 𝗕𝗮𝗰𝗸", callback_data="open_settings")]
            ])
            await query.message.edit_text(text, reply_markup=buttons, disable_web_page_preview=True)

        elif data == "edit_ulink":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            ask = await query.message.chat.ask("🔗 **Naya Updates Link bhejein:**\n\n(Button hatane ke liye `OFF` bhejein ya `/cancel` likhein)", timeout=120)
            if ask.text.lower() == "/cancel":
                return await ask.reply("🚫 **Cancelled.**")
            
            await db.update_setting("updates_link", ask.text.strip())
            await ask.reply("✅ **Updates Link Updated Successfully!**")

        elif data == "edit_hlink":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            ask = await query.message.chat.ask("🔗 **Naya Help Link bhejein:**\n\n(Button hatane ke liye `OFF` bhejein ya `/cancel` likhein)", timeout=120)
            if ask.text.lower() == "/cancel":
                return await ask.reply("🚫 **Cancelled.**")
            
            await db.update_setting("help_link", ask.text.strip())
            await ask.reply("✅ **Help Link Updated Successfully!**")

        elif data == "admin_toggles":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            await render_toggles_menu(query)

        elif data == "toggle_fsub":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            await db.toggle_fsub()
            await query.answer("F-Sub Setting Toggled!", show_alert=False)
            await render_toggles_menu(query)

        elif data == "toggle_autodel":
            if not is_admin: return await query.answer("❌ Only Admins!", show_alert=True)
            settings = await db.get_settings()
            curr = settings.get("auto_delete", 600)
            
            if curr == 600: new_val = 3600
            elif curr == 3600: new_val = 86400
            elif curr == 86400: new_val = 0
            else: new_val = 600
            
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

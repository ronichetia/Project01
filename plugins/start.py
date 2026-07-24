from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
from config import Config
from database import db
import asyncio
import pyromod # Used for asking user input dynamically

# ==================== HELPER FUNCTIONS ====================
# Start Menu Generator
def get_start_menu(user_name, is_admin):
    text = (
        f"> 👋 **ʜᴇʏ {user_name}! ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙᴏᴛ**\n\n"
        "ɪ ᴡɪʟʟ ʜᴇʟᴘ ʏᴏᴜ ᴘʀᴏᴠɪᴅᴇ ᴀɴɪᴍᴇ ᴠɪᴅᴇᴏs ᴀɴᴅ ʟɪɴᴋs.\n"
        "ᴇxᴘʟᴏʀᴇ ᴜsɪɴɢ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ:"
    )
    
    buttons = []
    # Admin button sirf admins ko dikhega
    if is_admin:
        buttons.append([InlineKeyboardButton("👮 ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ 👮", callback_data="open_admin")])
        
    buttons.append([
        InlineKeyboardButton("❓ ʜᴇʟᴘ", callback_data="user_help"),
        InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="user_about")
    ])
    
    return text, InlineKeyboardMarkup(buttons)

# About Menu Generator
async def get_about_menu(client):
    bot_info = await client.get_me()
    bot_name = bot_info.first_name
    
    text = (
        "> ℹ️ **ʙᴏᴛ ɪɴꜰᴏ & ᴀʙᴏᴜᴛ**\n\n"
        f"🤖 **ᴍʏ ɴᴀᴍᴇ:** {bot_name} • ʜᴇʟʟ's ᴘᴀʀᴀᴅɪsᴇ sᴇᴀsᴏɴ 2\n"
        "» **ᴄʀᴇᴀᴛᴏʀ:** [ᴍɪᴋᴏʏᴏ](https://t.me/YourUsername)\n"
        "» **ᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴛʏ:** [ᴀᴇʀᴏ ʙᴏᴛs](https://t.me/YourCommunityLink)\n"
        "» **ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ:** [sʜᴀɴᴜ ᴀɴɪᴍᴇ](https://t.me/YourAnimeChannel)\n"
        "» **sʜᴀɴᴜ ᴀɴɪᴍᴇ:** [sʜᴀɴᴜ ᴀɴɪᴍᴇ ᴄʜᴀᴛᴛɪɴɢ](https://t.me/YourChatLink)\n"
        "» **sʜᴀɴᴜ ᴀɴɪᴍᴇ ɴᴇᴡs:** [sʜᴀɴᴜ ᴀɴɪᴍᴇ ɴᴇᴡs](https://t.me/YourNewsLink)\n"
        "» **ᴅᴇᴠᴇʟᴏᴘᴇʀ:** [ᴍɪᴋᴏʏᴏ](https://t.me/YourUsername)"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_start"),
         InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close_panel")]
    ])
    return text, buttons

# Admin Menu Generator
async def get_admin_menu():
    text = "> 👮 **ᴀᴅᴍɪɴ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ**\n\nʏᴀʜᴀɴ sᴇ ᴀᴀᴘ ʙᴏᴛ ᴋɪ sᴀᴀʀɪ sᴇᴛᴛɪɴɢs ᴍᴀɴᴀɢᴇ ᴋᴀʀ sᴀᴋᴛᴇ ʜᴀɪɴ."
    
    btn_list = [
        [InlineKeyboardButton("📊 ʙᴏᴛ sᴛᴀᴛs", callback_data="admin_stats"),
         InlineKeyboardButton("📢 ʙʀᴏᴀᴅᴄᴀsᴛ", callback_data="admin_broadcast")],
        [InlineKeyboardButton("📺 ᴍᴀɴᴀɢᴇ ᴄʜᴀɴɴᴇʟs", callback_data="admin_channels"),
         InlineKeyboardButton("⚙️ ꜰ-sᴜʙ / ᴀᴜᴛᴏ-ᴅᴇʟ", callback_data="admin_toggles")],
        [InlineKeyboardButton("📝 ᴡᴇʟᴄᴏᴍᴇ ᴍsɢ", callback_data="admin_welcome"),
         InlineKeyboardButton("🔗 ᴘᴏsᴛ ʙᴜᴛᴛᴏɴs", callback_data="admin_post_btns")],
        [InlineKeyboardButton("👥 ᴍᴀɴᴀɢᴇ ᴀᴅᴍɪɴs", callback_data="admin_manage"),
         InlineKeyboardButton("🎥 ʜᴇʟᴘ ᴠɪᴅᴇᴏ", callback_data="edit_help_video")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_start"),
         InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close_panel")]
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
                    caption=file_data.get("caption", "ʜᴇʀᴇ ɪs ʏᴏᴜʀ ꜰɪʟᴇ!")
                )
            except:
                msg = await client.send_video(
                    chat_id=message.chat.id,
                    video=file_data["file_id"],
                    caption=file_data.get("caption", "ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴠɪᴅᴇᴏ!")
                )
            return
        else:
            await message.reply_text("❌ **ꜰɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ!**")
            return

    # NORMAL START MENU
    is_admin = message.from_user.id in Config.ADMINS
    text, buttons = get_start_menu(message.from_user.first_name, is_admin)
    await message.reply_text(text, reply_markup=buttons)


# ==================== 2. ADMIN COMMANDS ====================
@Client.on_message(filters.command("admin") & filters.user(Config.ADMINS))
async def admin_cmd(client, message):
    text, buttons = await get_admin_menu()
    await message.reply_text(text, reply_markup=buttons, disable_web_page_preview=True)

@Client.on_message(filters.command("addadmin") & filters.user(Config.ADMINS))
async def add_admin_cmd(client, message):
    try:
        new_admin_id = int(message.command[1])
        Config.ADMINS = list(Config.ADMINS)
        if new_admin_id not in Config.ADMINS:
            Config.ADMINS.append(new_admin_id)
            await message.reply_text(f"> ✅ **sᴜᴄᴄᴇss:** ᴜsᴇʀ `{new_admin_id}` ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴀs ᴀᴅᴍɪɴ!")
        else:
            await message.reply_text("⚠️ **ᴛʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ!**")
    except IndexError:
        await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ!**\nᴜsᴇ: `/addadmin UserID`")
    except ValueError:
        await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ɪᴅ!** ᴏɴʟʏ ɴᴜᴍʙᴇʀs ᴀʟʟᴏᴡᴇᴅ.")

@Client.on_message(filters.command("deladmin") & filters.user(Config.ADMINS))
async def del_admin_cmd(client, message):
    try:
        del_admin_id = int(message.command[1])
        Config.ADMINS = list(Config.ADMINS)
        if del_admin_id in Config.ADMINS:
            Config.ADMINS.remove(del_admin_id)
            await message.reply_text(f"> 🗑️ **sᴜᴄᴄᴇss:** ᴜsᴇʀ `{del_admin_id}` ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴀᴅᴍɪɴs.")
        else:
            await message.reply_text("⚠️ **ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴀᴅᴍɪɴ ʟɪsᴛ!**")
    except IndexError:
        await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ!**\nᴜsᴇ: `/deladmin UserID`")
    except ValueError:
        await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ɪᴅ!** ᴏɴʟʏ ɴᴜᴍʙᴇʀs ᴀʟʟᴏᴡᴇᴅ.")


# Helper function: Toggles Menu (Dynamic Buttons)
async def render_toggles_menu(query):
    settings = await db.get_settings()
    fsub_on = settings.get("fsub", False)
    autodel = settings.get("auto_delete", 600)

    fsub_text = "✅ ꜰ-sᴜʙ: ᴏɴ" if fsub_on else "❌ ꜰ-sᴜʙ: ᴏꜰꜰ"
    
    if autodel == 600: del_text = "⏱️ ᴀᴜᴛᴏ-ᴅᴇʟ: 10ᴍ"
    elif autodel == 3600: del_text = "⏱️ ᴀᴜᴛᴏ-ᴅᴇʟ: 1ʜ"
    elif autodel == 86400: del_text = "⏱️ ᴀᴜᴛᴏ-ᴅᴇʟ: 1ᴅ"
    elif autodel == 0: del_text = "⏱️ ᴀᴜᴛᴏ-ᴅᴇʟ: ᴏꜰꜰ"
    else: del_text = f"⏱️ ᴀᴜᴛᴏ-ᴅᴇʟ: {autodel}s"

    text = "> ⚙️ **ʙᴏᴛ ᴄᴏɴᴛʀᴏʟ sᴇᴛᴛɪɴɢs**\n\nᴛᴏɢɢʟᴇ ꜰᴏʀᴄᴇ-sᴜʙ ᴀɴᴅ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ sᴇᴛᴛɪɴɢs ꜰʀᴏᴍ ʜᴇʀᴇ:"
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(fsub_text, callback_data="toggle_fsub"),
         InlineKeyboardButton(del_text, callback_data="toggle_autodel")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="open_admin")] 
    ])
    
    try:
        await query.message.edit_text(text, reply_markup=buttons)
    except MessageNotModified:
        pass


# ==================== 3. ALL CALLBACK HANDLERS ====================
@Client.on_callback_query(filters.regex(r"^(close_panel|open_admin|user_about|user_help|back_start|admin_|edit_|reset_|toggle_|add_|del_|clear_)"))
async def main_callback_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    is_admin = user_id in Config.ADMINS

    try:
        if data == "close_panel":
            await query.message.delete()

        elif data == "open_admin":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            text, buttons = await get_admin_menu()
            if query.message.video or query.message.photo or query.message.document:
                await query.message.delete()
                await client.send_message(query.message.chat.id, text, reply_markup=buttons, disable_web_page_preview=True)
            else:
                await query.message.edit_text(text, reply_markup=buttons, disable_web_page_preview=True)
                
        elif data == "user_about":
            text, buttons = await get_about_menu(client)
            if query.message.video or query.message.photo or query.message.document:
                await query.message.delete()
                await client.send_message(query.message.chat.id, text, reply_markup=buttons, disable_web_page_preview=True)
            else:
                await query.message.edit_text(text, reply_markup=buttons, disable_web_page_preview=True)

        elif data == "back_start":
            text, buttons = get_start_menu(query.from_user.first_name, is_admin)
            
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
            
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_start")]])
            
            # DB se help video fetch karega
            settings = await db.get_settings()
            help_video = settings.get("help_video", None)
            
            if help_video:
                try:
                    await query.message.delete()
                    await client.send_video(
                        chat_id=query.message.chat.id,
                        video=help_video,
                        caption=text,
                        reply_markup=buttons
                    )
                except:
                    # Agar video link ya ID invalid ho toh text bhej dega
                    await client.send_message(query.message.chat.id, text, reply_markup=buttons)
            else:
                if query.message.video or query.message.photo or query.message.document:
                    await query.message.delete()
                    await client.send_message(query.message.chat.id, text, reply_markup=buttons)
                else:
                    await query.message.edit_text(text, reply_markup=buttons)

        # ====== ADMIN SUB-MENUS ======
        elif data == "edit_help_video":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            ask = await query.message.chat.ask("🎥 **ɴᴀʏᴀ ʜᴇʟᴘ ᴠɪᴅᴇᴏ ʙʜᴇᴊᴇɪɴ (ꜰɪʟᴇ ɪᴅ ʏᴀ ʟɪɴᴋ):**\n\n(ʀᴇᴍᴏᴠᴇ ᴋᴀʀɴᴇ ᴋᴇ ʟɪʏᴇ `OFF` ʙʜᴇᴊᴇɪɴ ʏᴀ `/cancel` ʟɪᴋʜᴇɪɴ)", timeout=120)
            
            if ask.text and ask.text.lower() == "/cancel": 
                return await ask.reply("🚫 **ᴄᴀɴᴄᴇʟʟᴇᴅ.**")
            
            video_val = None
            if ask.video:
                video_val = ask.video.file_id
            elif ask.text:
                if ask.text.strip().lower() == "off":
                    video_val = None
                else:
                    video_val = ask.text.strip()
            else:
                return await ask.reply("❌ **ɪɴᴠᴀʟɪᴅ ɪɴᴘᴜᴛ! sɪʀꜰ ᴠɪᴅᴇᴏ ʏᴀ ʟɪɴᴋ ʙʜᴇᴊᴇɪɴ.**")
            
            await db.update_setting("help_video", video_val)
            if video_val:
                await ask.reply("✅ **ʜᴇʟᴘ ᴠɪᴅᴇᴏ ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ!**")
            else:
                await ask.reply("🗑️ **ʜᴇʟᴘ ᴠɪᴅᴇᴏ ʀᴇᴍᴏᴠᴇᴅ!**")

        elif data == "admin_manage":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            text = (
                "> 👥 **ᴀᴅᴍɪɴ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**\n\n"
                f"**ᴄᴜʀʀᴇɴᴛ ᴀᴅᴍɪɴs ᴄᴏᴜɴᴛ:** `{len(Config.ADMINS)}`\n\n"
                "ᴜsᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴀᴅᴅ ᴏʀ ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴs ᴏʀ ᴜsᴇ ᴄᴏᴍᴍᴀɴᴅ `/addadmin ID`."
            )
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ ᴀᴅᴅ ᴀᴅᴍɪɴ", callback_data="add_admin"),
                 InlineKeyboardButton("➖ ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ", callback_data="del_admin")],
                [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="open_admin")]
            ])
            await query.message.edit_text(text, reply_markup=buttons)

        elif data == "add_admin":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            ask = await query.message.chat.ask("➕ **sᴇɴᴅ ᴛʜᴇ ᴜsᴇʀ ɪᴅ ᴏꜰ ᴛʜᴇ ɴᴇᴡ ᴀᴅᴍɪɴ:**\n\n(sᴇɴᴅ `/cancel` ᴛᴏ ᴀʙᴏʀᴛ)", timeout=120)
            if ask.text.lower() == "/cancel": return await ask.reply("🚫 **ᴄᴀɴᴄᴇʟʟᴇᴅ.**")
            
            try:
                new_id = int(ask.text.strip())
                Config.ADMINS = list(Config.ADMINS)
                if new_id not in Config.ADMINS:
                    Config.ADMINS.append(new_id)
                    await ask.reply(f"✅ **ᴜsᴇʀ `{new_id}` ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴀs ᴀᴅᴍɪɴ!**\nᴜsᴇ /admin ᴛᴏ ᴠᴇʀɪꜰʏ.")
                else:
                    await ask.reply("⚠️ **ᴛʜɪs ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ!**")
            except ValueError:
                await ask.reply("❌ **ɪɴᴠᴀʟɪᴅ ɪᴅ! ᴏɴʟʏ ɴᴜᴍʙᴇʀs ᴀʟʟᴏᴡᴇᴅ.**")

        elif data == "del_admin":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            ask = await query.message.chat.ask("➖ **sᴇɴᴅ ᴛʜᴇ ᴜsᴇʀ ɪᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ ꜰʀᴏᴍ ᴀᴅᴍɪɴs:**\n\n(sᴇɴᴅ `/cancel` ᴛᴏ ᴀʙᴏʀᴛ)", timeout=120)
            if ask.text.lower() == "/cancel": return await ask.reply("🚫 **ᴄᴀɴᴄᴇʟʟᴇᴅ.**")
            
            try:
                del_id = int(ask.text.strip())
                Config.ADMINS = list(Config.ADMINS)
                if del_id in Config.ADMINS:
                    Config.ADMINS.remove(del_id)
                    await ask.reply(f"🗑️ **ᴜsᴇʀ `{del_id}` ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴀᴅᴍɪɴs!**")
                else:
                    await ask.reply("⚠️ **ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴀᴅᴍɪɴ ʟɪsᴛ!**")
            except ValueError:
                await ask.reply("❌ **ɪɴᴠᴀʟɪᴅ ɪᴅ! ᴏɴʟʏ ɴᴜᴍʙᴇʀs ᴀʟʟᴏᴡᴇᴅ.**")


        elif data == "admin_channels":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            text = (
                "> 📺 **ᴄʜᴀɴɴᴇʟ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**\n\n"
                "ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴀᴅᴅ ᴀ ɴᴇᴡ ᴄʜᴀɴɴᴇʟ:\n"
                "`/addchannel`\n\n"
                "ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀ ᴄʜᴀɴɴᴇʟ:\n"
                "`/delchannel [Channel ID]`\n\n"
                "💡 *ᴛɪᴘ:* ɪꜰ ʏᴏᴜ ɢᴇᴛ ᴀ ᴘᴇᴇʀɪᴅ ᴇʀʀᴏʀ, ꜰᴏʀᴡᴀʀᴅ ᴀɴʏ ᴍᴇssᴀɢᴇ ꜰʀᴏᴍ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛʜᴇ ʙᴏᴛ."
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="open_admin")]])
            await query.message.edit_text(text, reply_markup=buttons)

        elif data == "admin_broadcast":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            await query.answer("📢 ʙʀᴏᴀᴅᴄᴀsᴛ ʀᴇᴀᴅʏ! ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ /broadcast.", show_alert=True)

        elif data == "admin_stats":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            users = await db.get_all_users()
            channels = await db.get_channels()
            text = (
                "> 📊 **ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs**\n\n"
                f"👤 **ᴛᴏᴛᴀʟ ᴜsᴇʀs:** `{len(users)}`\n"
                f"📺 **ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴄʜᴀɴɴᴇʟs:** `{len(channels)}`\n"
                f"👥 **ᴛᴏᴛᴀʟ ᴀᴅᴍɪɴs:** `{len(Config.ADMINS)}`"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="open_admin")]])
            await query.message.edit_text(text, reply_markup=buttons)

        elif data == "admin_welcome":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            settings = await db.get_settings()
            curr_msg = settings.get("welcome_msg", "default")
            
            text = (
                "> 📝 **ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ sᴇᴛᴛɪɴɢs**\n\n"
                f"**ᴄᴜʀʀᴇɴᴛ ᴍᴇssᴀɢᴇ:**\n`{curr_msg}`\n\n"
                "ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ sᴇᴛ ᴀ ɴᴇᴡ ᴍᴇssᴀɢᴇ, ᴏʀ ʀᴇsᴇᴛ ᴛᴏ ᴅᴇꜰᴀᴜʟᴛ."
            )
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️ ᴇᴅɪᴛ ᴍᴇssᴀɢᴇ", callback_data="edit_welcome"),
                 InlineKeyboardButton("🔄 ʀᴇsᴇᴛ ᴅᴇꜰᴀᴜʟᴛ", callback_data="reset_welcome")],
                [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="open_admin")]
            ])
            await query.message.edit_text(text, reply_markup=buttons)

        elif data == "reset_welcome":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            await db.reset_welcome_msg()
            await query.answer("ᴍᴇssᴀɢᴇ ʀᴇsᴇᴛ ᴛᴏ ᴅᴇꜰᴀᴜʟᴛ!", show_alert=False)
            query.data = "admin_welcome"
            await main_callback_handler(client, query)

        elif data == "edit_welcome":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            ask_msg = await query.message.chat.ask("📝 **sᴇɴᴅ ᴛʜᴇ ɴᴇᴡ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ:**\n\n(sᴇɴᴅ `/cancel` ᴛᴏ ᴀʙᴏʀᴛ)", timeout=120)
            if ask_msg.text.lower() == "/cancel":
                return await ask_msg.reply("🚫 **ᴄᴀɴᴄᴇʟʟᴇᴅ.**")
                
            await db.update_welcome_msg(ask_msg.text)
            await ask_msg.reply("✅ **ɴᴇᴡ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ sᴇᴛ sᴜᴄᴄᴇssꜰᴜʟʟʏ!**\nᴜsᴇ /admin ᴛᴏ ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ.")

        # ================= NEW DYNAMIC BUTTONS LOGIC =================
        elif data == "admin_post_btns":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            settings = await db.get_settings()
            
            post_buttons = settings.get("post_buttons", [])
            
            text = "> 🔗 **ᴍᴀɴᴀɢᴇ ᴘᴏsᴛ ʙᴜᴛᴛᴏɴs**\n\nᴍᴀɴᴀɢᴇ ᴄᴜsᴛᴏᴍ ʙᴜᴛᴛᴏɴs ꜰᴏʀ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛs:\n\n"
            
            if not post_buttons:
                text += "🚫 **ɴᴏ ʙᴜᴛᴛᴏɴs ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ.**"
            else:
                for i, btn in enumerate(post_buttons, 1):
                    text += f"**{i}. {btn['name']}** - `{btn['url']}`\n"
            
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ ᴀᴅᴅ ʙᴜᴛᴛᴏɴ", callback_data="add_post_btn"),
                 InlineKeyboardButton("➖ ʀᴇᴍᴏᴠᴇ ʙᴜᴛᴛᴏɴ", callback_data="del_post_btn")],
                [InlineKeyboardButton("🗑️ ᴄʟᴇᴀʀ ᴀʟʟ ʙᴜᴛᴛᴏɴs", callback_data="clear_post_btns")],
                [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="open_admin")]
            ])
            await query.message.edit_text(text, reply_markup=buttons, disable_web_page_preview=True)

        elif data == "add_post_btn":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            
            ask_name = await query.message.chat.ask("🏷️ **sᴇɴᴅ ᴛʜᴇ ɴᴀᴍᴇ ꜰᴏʀ ᴛʜᴇ ɴᴇᴡ ʙᴜᴛᴛᴏɴ:**\n\n(sᴇɴᴅ `/cancel` ᴛᴏ ᴀʙᴏʀᴛ)", timeout=120)
            if ask_name.text.lower() == "/cancel": 
                return await ask_name.reply("🚫 **ᴄᴀɴᴄᴇʟʟᴇᴅ.**")
            btn_name = ask_name.text.strip()
            
            ask_url = await query.message.chat.ask("🔗 **sᴇɴᴅ ᴛʜᴇ ᴜʀʟ/ʟɪɴᴋ ꜰᴏʀ ᴛʜɪs ʙᴜᴛᴛᴏɴ:**\n\n(sᴇɴᴅ `/cancel` ᴛᴏ ᴀʙᴏʀᴛ)", timeout=120)
            if ask_url.text.lower() == "/cancel": 
                return await ask_url.reply("🚫 **ᴄᴀɴᴄᴇʟʟᴇᴅ.**")
            btn_url = ask_url.text.strip()
            
            settings = await db.get_settings()
            post_buttons = settings.get("post_buttons", [])
            post_buttons.append({"name": btn_name, "url": btn_url})
            await db.update_setting("post_buttons", post_buttons)
            
            await ask_url.reply("✅ **ɴᴇᴡ ʙᴜᴛᴛᴏɴ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ!**")

        elif data == "del_post_btn":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            settings = await db.get_settings()
            post_buttons = settings.get("post_buttons", [])
            
            if not post_buttons:
                return await query.answer("🚫 ɴᴏ ʙᴜᴛᴛᴏɴs ᴛᴏ ʀᴇᴍᴏᴠᴇ!", show_alert=True)
                
            ask_idx = await query.message.chat.ask("🔢 **sᴇɴᴅ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ɴᴜᴍʙᴇʀ ᴛᴏ ʀᴇᴍᴏᴠᴇ (1, 2, 3...):**\n\n(sᴇɴᴅ `/cancel` ᴛᴏ ᴀʙᴏʀᴛ)", timeout=120)
            if ask_idx.text.lower() == "/cancel": 
                return await ask_idx.reply("🚫 **ᴄᴀɴᴄᴇʟʟᴇᴅ.**")
            
            try:
                idx = int(ask_idx.text.strip()) - 1
                if 0 <= idx < len(post_buttons):
                    removed = post_buttons.pop(idx)
                    await db.update_setting("post_buttons", post_buttons)
                    await ask_idx.reply(f"🗑️ **ʙᴜᴛᴛᴏɴ '{removed['name']}' ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ!**")
                else:
                    await ask_idx.reply("❌ **ɪɴᴠᴀʟɪᴅ ʙᴜᴛᴛᴏɴ ɴᴜᴍʙᴇʀ!**")
            except ValueError:
                await ask_idx.reply("❌ **ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ!**")

        elif data == "clear_post_btns":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            await db.update_setting("post_buttons", [])
            await query.answer("🗑️ ᴀʟʟ ᴘᴏsᴛ ʙᴜᴛᴛᴏɴs ᴄʟᴇᴀʀᴇᴅ!", show_alert=True)
            query.data = "admin_post_btns"
            await main_callback_handler(client, query)

        # =============================================================

        elif data == "admin_toggles":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            await render_toggles_menu(query)

        elif data == "toggle_fsub":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            await db.toggle_fsub()
            await query.answer("ꜰ-sᴜʙ sᴇᴛᴛɪɴɢ ᴛᴏɢɢʟᴇᴅ!", show_alert=False)
            await render_toggles_menu(query)

        elif data == "toggle_autodel":
            if not is_admin: return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs!", show_alert=True)
            settings = await db.get_settings()
            curr = settings.get("auto_delete", 600)
            
            if curr == 600: new_val = 3600
            elif curr == 3600: new_val = 86400
            elif curr == 86400: new_val = 0
            else: new_val = 600
            
            await db.set_auto_delete(new_val)
            await query.answer("ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ ᴜᴘᴅᴀᴛᴇᴅ!", show_alert=False)
            await render_toggles_menu(query)

    except MessageNotModified:
        await query.answer()
    except Exception as e:
        print(f"Callback Error: {e}")


# ==================== 4. BROADCAST COMMAND ====================
@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMINS) & filters.reply)
async def broadcast_msg(client, message):
    users = await db.get_all_users()
    msg = await message.reply("`ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴇssᴀɢᴇ...`")
    success, failed = 0, 0
    
    for user in users:
        try:
            await message.reply_to_message.copy(user["_id"])
            success += 1
            await asyncio.sleep(0.1) 
        except:
            failed += 1
            
    await msg.edit(f"> 📢 **ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ**\n\n✅ sᴜᴄᴄᴇss: `{success}`\n❌ ꜰᴀɪʟᴇᴅ: `{failed}`")

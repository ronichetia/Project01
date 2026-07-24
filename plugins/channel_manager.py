from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import CallbackQuery
from database import db
from config import Config

# 🧠 Ek temporary memory (dictionary) track karne ke liye ki admin abhi kya kar raha hai
admin_states = {}

@Client.on_message(filters.command("addchannel") & filters.user(Config.ADMINS))
async def add_channel_start(client, message):
    user_id = message.from_user.id
    
    # 𝗔𝗴𝗮𝗿 𝘂𝘀𝗲𝗿 𝗱𝗶𝗿𝗲𝗰𝘁 𝗜𝗗 𝗮𝘂𝗿 𝗡𝗮𝗺𝗲 𝗱𝗮𝗮𝗹 𝗿𝗮𝗵𝗮 𝗵𝗮𝗶 (/𝗮𝗱𝗱𝗰𝗵𝗮𝗻𝗻𝗲𝗹 -𝟭𝟬𝟬... 𝗡𝗮𝗺𝗲)
    parts = message.text.split(" ", 2)
    if len(parts) == 3:
        try:
            ch_id = int(parts[1])
            ch_name = parts[2]
            wait_msg = await message.reply_text("🔄 **Checking Bot Access...**")
            
            try:
                await client.get_chat(ch_id)
            except Exception:
                await wait_msg.delete()
                return await message.reply_text(
                    "❌ **𝗣𝗲𝗲𝗿 𝗜𝗗 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 / 𝗡𝗼𝘁 𝗙𝗼𝘂𝗻𝗱!**\n\n"
                    "Kripya sirf `/addchannel` likh kar send karein aur bot ke instructions follow karein."
                )
            
            await db.add_channel(ch_id, ch_name)
            return await wait_msg.edit_text(f"> ✅ **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗔𝗱𝗱𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!**\n\n**𝗜𝗗:** `{ch_id}`\n**𝗡𝗮𝗺𝗲:** {ch_name}")
        except ValueError:
            return await message.reply_text("❌ **𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗼𝗿𝗺𝗮𝘁!**")

    # 𝗦𝗧𝗘𝗣 𝟭: 𝗔𝗴𝗮𝗿 𝘂𝘀𝗲𝗿 𝘀𝗶𝗿𝗳 /𝗮𝗱𝗱𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝘁𝘆𝗽𝗲 𝗸𝗮𝗿𝘁𝗮 𝗵𝗮𝗶
    admin_states[user_id] = "adding_channel"
    await message.reply_text(
        "> ➕ **𝗔𝗱𝗱 𝗡𝗲𝘄 𝗖𝗵𝗮𝗻𝗻𝗲𝗹**\n\n"
        "Apne channel ko bot me add karne ke liye, **us channel se koi bhi ek message yahan FORWARD karein.**\n\n"
        "*(Note: Bot us channel me Admin hona zaroori hai)*\n\n"
        "❌ Cancel karne ke liye `/cancel` bhejein."
    )

# 𝗦𝗧𝗘𝗣 𝟮: 𝗖𝗮𝘁𝗰𝗵 𝗙𝗼𝗿𝘄𝗮𝗿𝗱𝗲𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 
@Client.on_message(filters.forwarded & filters.user(Config.ADMINS) & filters.private)
async def process_forwarded_channel(client, message):
    user_id = message.from_user.id
    
    # Sirf tabhi catch karega jab admin sach me channel add karne ke mode me ho
    if admin_states.get(user_id) == "adding_channel":
        if message.forward_from_chat and message.forward_from_chat.type == ChatType.CHANNEL:
            ch_id = message.forward_from_chat.id
            ch_name = message.forward_from_chat.title
            
            # Database me direct save karo (Ab /addchannel ki bhi zaroorat nahi)
            await db.add_channel(ch_id, ch_name)
            
            # State clear karo taaki next time normal chat ho sake
            del admin_states[user_id]
            
            await message.reply_text(
                f"> ✅ **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗔𝗱𝗱𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!**\n\n"
                f"**𝗜𝗗:** `{ch_id}`\n"
                f"**𝗡𝗮𝗺𝗲:** {ch_name}\n\n"
                f"🎉 Bot ne ab is channel ko automatically yaad kar liya aur save kar liya hai!"
            )
        else:
            await message.reply_text("❌ **Error:** Ye message kisi Channel se forward nahi hua hai. Kripya channel ka message forward karein ya `/cancel` bhejein.")

# ❌ 𝗖𝗮𝗻𝗰𝗲𝗹 𝗣𝗿𝗼𝗰𝗲𝘀𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱
@Client.on_message(filters.command("cancel") & filters.user(Config.ADMINS))
async def cancel_action(client, message):
    user_id = message.from_user.id
    if user_id in admin_states:
        del admin_states[user_id]
        await message.reply_text("✅ **Add Channel Process Cancelled.**")
    else:
        pass # Ignore if not in any process

# 🗑️ 𝗗𝗲𝗹𝗲𝘁𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹
@Client.on_message(filters.command("delchannel") & filters.user(Config.ADMINS))
async def del_channel(client, message):
    try:
        ch_id = int(message.text.split(" ")[1])
        await db.remove_channel(ch_id)
        await message.reply_text(f"> 🗑️ **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗥𝗲𝗺𝗼𝘃𝗲𝗱:** `{ch_id}`")
    except:
        await message.reply_text("❌ **𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗼𝗿𝗺𝗮𝘁!**\n𝖴𝗌𝖾: `/delchannel -100123456789`")

# 🔘 𝗔𝗱𝗺𝗶𝗻 𝗣𝗮𝗻𝗲𝗹 𝗕𝘂𝘁𝘁𝗼𝗻 𝗧𝗿𝗶𝗴𝗴𝗲𝗿 (𝗕𝗼𝗻𝘂𝘀 𝗙𝗲𝗮𝘁𝘂𝗿𝗲)
@Client.on_callback_query(filters.regex("^add_new_channel$") & filters.user(Config.ADMINS))
async def add_channel_callback(client, query: CallbackQuery):
    user_id = query.from_user.id
    admin_states[user_id] = "adding_channel"
    await query.message.edit_text(
        "> ➕ **𝗔𝗱𝗱 𝗡𝗲𝘄 𝗖𝗵𝗮𝗻𝗻𝗲𝗹**\n\n"
        "Apne channel ko bot me add karne ke liye, **us channel se koi bhi ek message yahan FORWARD karein.**\n\n"
        "*(Note: Bot us channel me Admin hona zaroori hai)*\n\n"
        "❌ Cancel karne ke liye `/cancel` bhejein."
    )

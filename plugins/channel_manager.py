from pyrogram import Client, filters
from database import db
from config import Config

@Client.on_message(filters.command("addchannel") & filters.user(Config.ADMINS))
async def add_channel(client, message):
    try:
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            raise ValueError
            
        ch_id = int(parts[1])
        ch_name = parts[2]
        
        wait_msg = await message.reply_text("🔄 **Checking Bot Access...**")
        
        # 🔍 Verification & Caching Logic
        try:
            # Pehle sidha access check karte hai
            await client.get_chat(ch_id)
        except Exception:
            # Agar peer cache me nahi hai toh bot force sync karega
            try:
                async for _ in client.get_dialogs():
                    pass
                await client.get_chat(ch_id) # Ek baar wapas try
            except Exception:
                await wait_msg.delete()
                return await message.reply_text(
                    "❌ **𝗣𝗲𝗲𝗿 𝗜𝗗 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 / 𝗡𝗼𝘁 𝗙𝗼𝘂𝗻𝗱!**\n\n"
                    "Bot is channel ko cache nahi kar pa raha hai.\n\n"
                    "🛠 **𝗦𝗼𝗹𝘂𝘁𝗶𝗼𝗻 (𝟭𝟬𝟬% 𝗪𝗼𝗿𝗸𝗶𝗻𝗴):**\n"
                    "Apne channel se koi bhi ek message is bot ko **FORWARD** karo, uske baad bot usko scan karke khud add kar lega."
                )
        
        # 💾 Save to Database if verification passed
        await db.add_channel(ch_id, ch_name)
        await wait_msg.edit_text(f"> ✅ **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗔𝗱𝗱𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!**\n\n**𝗜𝗗:** `{ch_id}`\n**𝗡𝗮𝗺𝗲:** {ch_name}")
        
    except ValueError:
        await message.reply_text("❌ **𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗼𝗿𝗺𝗮𝘁!**\n𝖴𝗌𝖾: `/addchannel -100123456789 Channel_Name`")

@Client.on_message(filters.command("delchannel") & filters.user(Config.ADMINS))
async def del_channel(client, message):
    try:
        ch_id = int(message.text.split(" ")[1])
        await db.remove_channel(ch_id)
        await message.reply_text(f"> 🗑️ **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗥𝗲𝗺𝗼𝘃𝗲𝗱:** `{ch_id}`")
    except:
        await message.reply_text("❌ **𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗼𝗿𝗺𝗮𝘁!**\n𝖴𝗌𝖾: `/delchannel -100123456789`")

# 🛠 HACK TO CACHE PEER ID (New Feature)
@Client.on_message(filters.forwarded & filters.user(Config.ADMINS) & filters.private)
async def cache_peer(client, message):
    if message.forward_from_chat:
        ch_id = message.forward_from_chat.id
        ch_name = message.forward_from_chat.title
        await message.reply_text(
            f"> ✅ **𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗗𝗮𝘁𝗮 𝗖𝗮𝗰𝗵𝗲𝗱!**\n\n"
            f"Bot ne ab is channel ka access hash yaad kar liya hai.\n"
            f"👇 Ab is command ko niche se copy karke bas send kar do:\n\n"
            f"`/addchannel {ch_id} {ch_name}`"
        )
    else:
        await message.reply_text("❌ Ye message kisi channel se forward nahi kiya gaya hai. Kripya channel se message forward karein.")

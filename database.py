from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_URI)
        self.db = self.client["PremiumBotDB"]
        self.users = self.db["users"]
        self.files = self.db["files"]
        self.channels = self.db["channels"]
        self.settings = self.db["settings"]

    # 𝗨𝘀𝗲𝗿 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁
    async def add_user(self, user_id):
        if not await self.users.find_one({"_id": user_id}):
            await self.users.insert_one({"_id": user_id})

    async def get_all_users(self):
        return await self.users.find({}).to_list(length=None)

    # 𝗙𝗶𝗹𝗲 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁 (𝗟𝗶𝗻𝗸𝘀)
    async def save_file(self, file_id, file_hash, caption):
        await self.files.insert_one({
            "_id": file_hash,
            "file_id": file_id,
            "caption": caption
        })

    async def get_file(self, file_hash):
        return await self.files.find_one({"_id": file_hash})

    # 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁
    async def add_channel(self, channel_id, channel_name):
        await self.channels.update_one(
            {"_id": channel_id},
            {"$set": {"name": channel_name}},
            upsert=True
        )

    async def get_channels(self):
        return await self.channels.find({}).to_list(length=None)

    async def remove_channel(self, channel_id):
        await self.channels.delete_one({"_id": channel_id})

    # ⚙️ 𝗕𝗼𝘁 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁 (𝗡𝗲𝘄𝗹𝘆 𝗔𝗱𝗱𝗲𝗱)
    async def get_settings(self):
        # Ek default document return karega agar pehle se nahi hai
        settings = await self.settings.find_one({"_id": "bot_settings"})
        if not settings:
            default_settings = {
                "_id": "bot_settings",
                "welcome_msg": "default", 
                "fsub": False,
                "auto_delete": 600 # Default 10 Minutes in seconds
            }
            await self.settings.insert_one(default_settings)
            return default_settings
        return settings

    async def update_welcome_msg(self, msg_text):
        await self.settings.update_one(
            {"_id": "bot_settings"},
            {"$set": {"welcome_msg": msg_text}},
            upsert=True
        )

    async def reset_welcome_msg(self):
        await self.settings.update_one(
            {"_id": "bot_settings"},
            {"$set": {"welcome_msg": "default"}},
            upsert=True
        )

    async def toggle_fsub(self):
        # Current status check karke usko reverse (toggle) kar dega
        settings = await self.get_settings()
        new_status = not settings.get("fsub", False)
        await self.settings.update_one(
            {"_id": "bot_settings"},
            {"$set": {"fsub": new_status}},
            upsert=True
        )
        return new_status

    async def set_auto_delete(self, timer_seconds):
        await self.settings.update_one(
            {"_id": "bot_settings"},
            {"$set": {"auto_delete": timer_seconds}},
            upsert=True
        )

db = Database()

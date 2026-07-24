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

db = Database()

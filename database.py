import os
import base64
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
    async def add_channel(self, channel_id, channel_data):
        await self.channels.update_one(
            {"_id": channel_id},
            {"$set": channel_data},
            upsert=True
        )

    async def get_channels(self):
        return await self.channels.find({}).to_list(length=None)

    async def remove_channel(self, channel_id):
        await self.channels.delete_one({"_id": channel_id})

    # ⚙️ 𝗕𝗼𝘁 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁
    async def get_settings(self):
        settings = await self.settings.find_one({"_id": "bot_settings"})
        if not settings:
            default_settings = {
                "_id": "bot_settings",
                "welcome_msg": "default", 
                "fsub": False,
                "auto_delete": 600, # Default 10 Minutes in seconds
                "updates_link": None,
                "help_link": None,
                # 👇 NEW: Default admins ko config se utha kar pehli baar DB me save karega
                "admins": Config.ADMINS 
            }
            await self.settings.insert_one(default_settings)
            return default_settings
        return settings

    async def update_setting(self, key, value):
        """Generic function to update any setting dynamically"""
        await self.settings.update_one(
            {"_id": "bot_settings"},
            {"$set": {key: value}},
            upsert=True
        )

    async def update_welcome_msg(self, msg_text):
        await self.update_setting("welcome_msg", msg_text)

    async def reset_welcome_msg(self):
        await self.update_setting("welcome_msg", "default")

    async def toggle_fsub(self):
        settings = await self.get_settings()
        new_status = not settings.get("fsub", False)
        await self.update_setting("fsub", new_status)
        return new_status

    async def set_auto_delete(self, timer_seconds):
        await self.update_setting("auto_delete", timer_seconds)

    # ==========================================
    # 👇 NEW: 𝗔𝗗𝗠𝗜𝗡 𝗠𝗔𝗡𝗔𝗚𝗘𝗠𝗘𝗡𝗧 (For Database)
    # ==========================================
    
    async def get_admins(self):
        settings = await self.get_settings()
        return settings.get("admins", Config.ADMINS)

    async def add_admin_db(self, admin_id):
        # $addToSet se duplicate ID save nahi hogi
        await self.settings.update_one(
            {"_id": "bot_settings"},
            {"$addToSet": {"admins": admin_id}}, 
            upsert=True
        )

    async def remove_admin_db(self, admin_id):
        # $pull specific ID ko array me se delete kar deta hai
        await self.settings.update_one(
            {"_id": "bot_settings"},
            {"$pull": {"admins": admin_id}}
        )

    # ==========================================
    # 👇 NEW: 𝗦𝗘𝗦𝗦𝗜𝗢𝗡 𝗙𝗜𝗟𝗘 𝗕𝗔𝗖𝗞𝗨𝗣 & 𝗥𝗘𝗦𝗧𝗢𝗥𝗘
    # ==========================================
    async def load_session(self, session_name="PremiumAutoPoster.session"):
        """Bot start hone se pehle DB se session file wapas layega"""
        try:
            session_data = await self.settings.find_one({"_id": "session_file"})
            if session_data and "file_b64" in session_data:
                with open(session_name, "wb") as f:
                    f.write(base64.b64decode(session_data["file_b64"]))
                print("✅ 𝗦𝗲𝘀𝘀𝗶𝗼𝗻 𝗳𝗶𝗹𝗲 𝗿𝗲𝘀𝘁𝗼𝗿𝗲𝗱 𝗳𝗿𝗼𝗺 𝗠𝗼𝗻𝗴𝗼𝗗𝗕!")
        except Exception as e:
            print(f"⚠️ Error loading session: {e}")

    async def save_session(self, session_name="PremiumAutoPoster.session"):
        """Naye channels add hone par session file ko DB me backup karega"""
        try:
            if os.path.exists(session_name):
                with open(session_name, "rb") as f:
                    file_b64 = base64.b64encode(f.read()).decode("utf-8")
                    await self.settings.update_one(
                        {"_id": "session_file"},
                        {"$set": {"file_b64": file_b64}},
                        upsert=True
                    )
                print("✅ 𝗦𝗲𝘀𝘀𝗶𝗼𝗻 𝗳𝗶𝗹𝗲 𝗯𝗮𝗰𝗸𝗲𝗱 𝘂𝗽 𝘁𝗼 𝗠𝗼𝗻𝗴𝗼𝗗𝗕!")
        except Exception as e:
            print(f"⚠️ Error saving session: {e}")

db = Database()

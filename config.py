import os

class Config:
    # 𝗔𝗣𝗜 𝗞𝗲𝘆𝘀
    API_ID = int(os.environ.get("API_ID", "28733143")) # Apna API ID daalo
    API_HASH = os.environ.get("API_HASH", "f7bbd29cf8ba336237046dbecfeab519")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8670021313:AAFn9UGLdcF24Z9wtarwvw3f8W1Y3Ppv07U")
    
    # 𝗗𝗮𝘁𝗮𝗯𝗮𝘀𝗲 (𝗠𝗼𝗻𝗴𝗼𝗗𝗕)
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://neonman242:neonman242@game0.sqfzcd4.mongodb.net/?appName=game0")
    
    # 𝗔𝗱𝗺𝗶𝗻 & 𝗙-𝗦𝘂𝗯
    ADMINS = [int(admin) for admin in os.environ.get("ADMINS", "123456789").split()] # Apna User ID
    FSUB_CHANNEL = int(os.environ.get("FSUB_CHANNEL", "-1004295637905")) # Channel ID
    FSUB_INVITE_LINK = os.environ.get("FSUB_INVITE_LINK", "https://t.me/tetsbdbeb36")
    
    # 𝗕𝗼𝘁 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 (Default)
    AUTO_DELETE_TIME = 600 # 10 Minutes in seconds (Bot chat auto delete)
    
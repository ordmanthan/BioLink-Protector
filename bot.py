from pyrogram import Client, filters
from pymongo import MongoClient
import os

API_ID = int(os.environ.get("22602867"))
API_HASH = os.environ.get("7e2042dde2f4a8278cbe9d3bebae8ac5")
BOT_TOKEN = os.environ.get("8137321769:AAHAeHKLxh0T5-QDwYXQXUgCJAne4u02Kh8")
MONGO_URI = os.environ.get("mongodb+srv://dark:12345@cluster0.i65p4do.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# MongoDB connection
client_mongo = MongoClient(mongodb+srv://dark:12345@cluster0.i65p4do.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0)
db = client_mongo["bio_link_detector"]
users_collection = db["users"]

# Pyrogram bot client
app = Client("BioLinkBot", api_id=22602867, api_hash=7e2042dde2f4a8278cbe9d3bebae8ac5, bot_token=8137321769:AAHAeHKLxh0T5-QDwYXQXUgCJAne4u02Kh8)

# /start command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    welcome_text = """
✨ Welcome to BioLink Protector Bot! ✨

🛡️ I help protect your groups from users with links in their bio.

🔹 Key Features:
   • Automatic URL detection in user bios
   • Customizable warning limit
   • Auto-mute or ban when limit is reached
   • Whitelist management for trusted users

Use /help to see all available commands.
"""
    await message.reply_text(welcome_text)

# New member join event
@app.on_message(filters.new_chat_members)
async def new_member(client, message):
    for member in message.new_chat_members:
        bio = member.bio if hasattr(member, 'bio') else ""
        if "http" in bio:
            await message.reply_text(f"{member.mention} your bio contains a link! ⚠️")
            users_collection.update_one({"user_id": member.id}, {"$set": {"has_link": True}}, upsert=True)

# Run the bot
app.run()

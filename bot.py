from pyrogram import Client
from pyrogram.raw import functions
import time
import os

API_ID = int(os.environ.get("22602867"))
API_HASH = os.environ.get("7e2042dde2f4a8278cbe9d3bebae8ac5")
BOT_TOKEN = os.environ.get("8137321769:AAHAeHKLxh0T5-QDwYXQXUgCJAne4u02Kh8")
from pymongo import MongoClient

MONGO_URI = os.environ.get("mongodb+srv://dark:12345@cluster0.i65p4do.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client_mongo = MongoClient(mongodb+srv://dark:12345@cluster0.i65p4do.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0)
db = client_mongo["biolink_db"]


app = Client("my_bot", api_id=22602867, api_hash=7e2042dde2f4a8278cbe9d3bebae8ac5, bot_token=8137321769:AAHAeHKLxh0T5-QDwYXQXUgCJAne4u02Kh8)

# Time sync fix
with app:
    app.send(functions.Ping(ping_id=int(time.time())))

app.run()
from pyrogram.raw import functions

# bot start से पहले
await app.send(functions.Ping(ping_id=int(time.time())))


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

@app.on_message(filters.new_chat_members)
async def new_member(client, message):
    for member in message.new_chat_members:
        bio = member.bio if hasattr(member, 'bio') else ""
        if "http" in bio:
            await message.reply_text(f"{member.mention} your bio contains a link! ⚠️")
            users_collection.update_one({"user_id": member.id}, {"$set": {"has_link": True}}, upsert=True)

app.run()


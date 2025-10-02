from pyrogram import Client, filters
from pymongo import MongoClient
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

client_mongo = MongoClient(MONGO_URI)
db = client_mongo["bio_link_detector"]
users_collection = db["users"]

app = Client("BioLinkBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("Hello! I'm BioLink Detector Bot.")

@app.on_message(filters.new_chat_members)
async def new_member(client, message):
    for member in message.new_chat_members:
        bio = member.bio if hasattr(member, 'bio') else ""
        if "http" in bio:
            await message.reply_text(f"{member.mention} your bio contains a link! ⚠️")
            users_collection.update_one({"user_id": member.id}, {"$set": {"has_link": True}}, upsert=True)

app.run()

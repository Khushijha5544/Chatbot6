import asyncio
import aiohttp

from pyrogram import filters
from pyrogram.types import Message

from config import app


async def fetch_response(query):
    url = f"https://codesearchdevapi.vercel.app/chat?query={query}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data")
        except (aiohttp.ClientError, asyncio.TimeoutError):
            print(f"Failed to fetch response for query: {query}")
            return None

async def text_filter(_, __, m: Message):
    return (
        bool(m.text)
        and len(m.text) <= 69
        and not m.text.startswith(("!", "/"))
        and (not m.reply_to_message or m.reply_to_message.from_user.id == m._client.me.id)
    )

chatbot_filter = filters.create(text_filter)

@app.on_message(chatbot_filter)
async def chatbot(_, message: Message):
    reply = await fetch_response(message.text)
    await message.reply_text(reply or "ChatBot Error: Something went wrong. Contact @AsuraaSupports.")

# ⭐ 𝐂𝐫𝐞𝐝𝐢𝐭𝐬: @CodeSearchDev ✦ @AshokShau
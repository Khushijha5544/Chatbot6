import logging
from os import getenv

import httpx
import pyrogram
import uvloop
from pyrogram import Client, filters, idle, errors
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.filters import create
from pyrogram.types import Message

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


class Telegram(Client):
    def __init__(self) -> None:
        super().__init__(
            name="bot",
            api_id=6,
            api_hash='eb06d4abfb49dc3eeb1aeb98ae0f581e',
            bot_token=getenv("TOKEN"),
            in_memory=False,
            parse_mode=ParseMode.DEFAULT,
            workers=10,
        )
        self.me = None
        self.http = httpx.AsyncClient(timeout=10)

    async def start(self, *args, **kwargs) -> None:
        await super().start(*args, **kwargs)
        self.me = await self.get_me()
        LOGGER.info(f"[•] Bot started as {self.me.first_name} (@{self.me.username})")
        LOGGER.info(f"Pyrogram v{pyrogram.__version__}")

    async def stop(self, *args, **kwargs) -> None:
        await self.http.aclose()
        await super().stop(*args, **kwargs)
        LOGGER.info("[•] Bot stopped.")


async def start_cmd(_, message: Message) -> None:
    await message.reply_text(f"Hello, {message.from_user.mention}")


async def text_filter(_, __, m: Message):
    return (
            bool(m.text)
            and len(m.text) <= 69
            and not m.text.startswith(("!", "/"))
            and (not m.reply_to_message or m.reply_to_message.from_user.id == m._client.me.id)
    )


chatbot_filter = create(text_filter)


async def chatbot(client: Telegram, message: Message):
    """Handles chatbot responses efficiently."""
    url = f"https://codesearchdevapi.vercel.app/chat?query={message.text}"

    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    except errors.RPCError:
        pass

    try:
        response = await client.http.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if reply := data.get("data"):
                return await message.reply_text(reply)

    except httpx.HTTPError:
        pass

    # return await message.reply_text("ChatBot Error: Something went wrong. Contact @FallenProjects.")


async def main():
    bot = Telegram()

    bot.add_handler(pyrogram.handlers.MessageHandler(start_cmd, filters.command("start")))
    bot.add_handler(pyrogram.handlers.MessageHandler(chatbot, chatbot_filter & ~filters.me))

    try:
        await bot.start()
        LOGGER.info("[•] Bot is now running...")
        await idle()
    except Exception as e:
        LOGGER.error(f"[!] Bot failed to start: {e}", exc_info=True)
    finally:
        await bot.stop()
        LOGGER.info("[•] Bot stopped.")


if __name__ == "__main__":
    uvloop.run(main())


# ⭐ 𝐂𝐫𝐞𝐝𝐢𝐭𝐬: @CodeSearchDev ✦ @AshokShau
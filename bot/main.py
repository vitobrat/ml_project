from aiogram import Bot, Dispatcher
import asyncio
from bot.compliments.send_compliment import run_send_compliment

from aiogram.client.default import DefaultBotProperties

from bot import admin
from bot.handler import handler_commands, handler_messages
from aiosqlitedatabase.database import create_table
from bot.keyboards import commands
from config.config import TOKEN
import logging

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_routers(admin.router, handler_commands.router, handler_messages.router)
    await bot.set_my_commands(commands)

    await create_table()

    asyncio.create_task(run_send_compliment(bot, 30))
    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

import logging
from aiogram.types import BotCommand
from aiohttp import web
from bot.bot_depend import dp, bot
from bot.app import app_handl
import asyncio
from bot.config import settings
from bot.handlers import (
    start_router,
    catalog_router,
    favorites_router,
    view_statistics_router,
    help_router,
    admin_panel_router,
)


def register_routers():
    dp.include_router(start_router)
    dp.include_router(catalog_router)
    dp.include_router(favorites_router)
    dp.include_router(view_statistics_router)
    dp.include_router(help_router)
    dp.include_router(admin_panel_router)


async def set_commands():
    commands = [BotCommand(command="/start", description="Начать работу с ботом")]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(level=logging.INFO)
    register_routers()
    await set_commands()
    # app = app_handl()

    # web.run_app(app, port=settings.PORT, host=settings.HOST)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    # main()

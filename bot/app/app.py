import logging
from aiohttp import web
from aiogram.types import Update
from bot.bot_depend import bot, dp
from bot.config import settings


async def on_startup(app):
    logging.info("Bot started, start webhook")
    url: str = f"{settings.NGROK_URL}{settings.WEBHOOK_PATH}"
    await bot.set_webhook(url=url)


async def on_shutdown(app):
    logging.info("Bot shutdown")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    logging.error("Бот остановлен")


async def handle_webhook(request: web.Request):
    try:
        update = Update(**await request.json())
        await dp.feed_update(bot, update)
        return web.Response(status=200)
    except Exception as e:
        logging.error(e)
        return web.Response(status=500)


def app():
    app = web.Application()

    app.router.add_post(path=f"{settings.WEBHOOK_PATH}", handler=handle_webhook)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from bot.core.models import UserDao
from bot.keyboards import start_keyb
from bot.schemas import TelegramID, UserUpdate

router = Router()


@router.message(CommandStart())
async def get_start_message(message: Message):
    await message.delete()
    telegram_id = message.from_user.id
    user = await UserDao.get_product_by_id(TelegramID(telegram_id=message.from_user.id))

    if not user:
        await UserDao.add_table_by_filters(
            UserUpdate(
                telegram_id=telegram_id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
            )
        )

        await message.answer(
            text="Добрый день, спасибо что впервые запустили нашего бота,\nприятного времяпрепровождения!",
            reply_markup=start_keyb(telegram_id),
        )
    else:
        await message.answer(
            text=f"Приветствуем {message.from_user.first_name}",
            reply_markup=start_keyb(telegram_id),
        )


@router.callback_query(F.data.in_(("menu", "menu_photo")))
async def menu(call: CallbackQuery):
    await call.answer(text="Вы вернулись в меню")

    if call.data == "menu_photo":
        await call.message.delete()
        await call.message.answer(
            text=f"Приветствуем {call.from_user.first_name}",
            reply_markup=start_keyb(telegram_id=call.from_user.id),
        )

    else:
        await call.message.edit_text(
            text=f"Приветствуем {call.from_user.first_name}",
            reply_markup=start_keyb(telegram_id=call.from_user.id),
        )


@router.callback_query(F.data == "delete_message")
async def delete_message(call: CallbackQuery):
    await call.message.delete()

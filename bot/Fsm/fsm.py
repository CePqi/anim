from aiogram.fsm.state import StatesGroup, State


class FsmGroup(StatesGroup):
    year = State()
    rating = State()
    animes = State()
    del_animes = State()
    total_row = State()
    min_row = State()

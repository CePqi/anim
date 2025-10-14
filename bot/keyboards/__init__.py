__all__ = (
    "start_keyb",
    "catalog_keyb",
    "view_stats_keyb",
    "help_keyb",
    "favorite_keyb",
    "hide_the_message",
    "view_menu_keyb",
    "admin_keyb",
    "choose_year_keyb",
    "choose_rating_keyb",
    "next_keyb",
)

from bot.keyboards.start_keyb import start_keyb
from bot.keyboards.catalog_keyb import (
    catalog_keyb,
    hide_the_message,
    choose_year_keyb,
    choose_rating_keyb,
    next_keyb,
)
from bot.keyboards.favorites_keyb import favorite_keyb, hide_and_delete
from bot.keyboards.view_stats_keyb import view_stats_keyb, view_menu_keyb
from bot.keyboards.help_keyb import help_keyb
from bot.keyboards.admin_keyb import admin_keyb

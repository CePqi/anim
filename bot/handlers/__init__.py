__all__ = (
    "start_router",
    "catalog_router",
    "favorites_router",
    "view_statistics_router",
    "help_router",
    "admin_panel_router",
)

from bot.handlers.start import router as start_router
from bot.handlers.catalog_of_filmes import router as catalog_router
from bot.handlers.favorites_of_filmes import router as favorites_router
from bot.handlers.view_statistics import router as view_statistics_router
from bot.handlers.help import router as help_router
from bot.handlers.admin_panel import router as admin_panel_router

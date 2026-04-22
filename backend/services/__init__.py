"""
服务包
"""

from .game_engine import GameEngine, get_current_game, reset_game
from .event_system import EventSystem, GameEvent
from .save_system import SaveSystem, get_save_system

__all__ = [
    "GameEngine",
    "get_current_game",
    "reset_game",
    "EventSystem",
    "GameEvent",
    "SaveSystem",
    "get_save_system",
]

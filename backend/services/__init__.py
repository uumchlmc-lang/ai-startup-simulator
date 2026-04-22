"""
服务包
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.game_engine import GameEngine, get_current_game, reset_game
from services.event_system import EventSystem, GameEvent
from services.save_system import SaveSystem, get_save_system

__all__ = [
    "GameEngine",
    "get_current_game",
    "reset_game",
    "EventSystem",
    "GameEvent",
    "SaveSystem",
    "get_save_system",
]

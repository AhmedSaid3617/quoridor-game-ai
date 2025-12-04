from typing import List
from src.rules.game_rules import GameRules
from src.state.game_state import GameState


class Path:
    def __init__(self, start: GameState.Position, path: List[GameRules.PawnMove]):
        self.start = start
        self.path = path
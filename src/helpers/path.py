from typing import List
from src.rules.game_rules import GameRules
from src.state.game_state import GameState


class Path:
    def __init__(self, start: GameState.Position, path: List[GameRules.PawnMove]):
        self.start = start
        self.path = path
        self.end = self.calculate_end_position()


    def calculate_end_position(self) -> GameState.Position:
        current_position = self.start
        rules = GameRules(None)  # Assuming GameRules can be initialized without a game state for this calculation
        for move in self.path:
            current_position = rules.apply_pawn_move(current_position, move)
        return current_position
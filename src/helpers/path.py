from typing import List
from src.controller.state_controller import StateController
from src.rules.game_rules import GameRules
from src.state.game_state import GameState


class Path:
    def __init__(self, start: GameState.Position, path: List[GameRules.PawnMove]):
        self.start = start
        self.path = path
        self.end = self.calculate_end_position()


    def calculate_end_position(self) -> GameState.Position:
        current_position = self.start
        for move in self.path:
            t = current_position + GameRules.movement_to_delta(move.movement)
            current_position = GameState.Position(t[0], t[1])
        return current_position
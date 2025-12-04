from src.rules.game_rules import GameRules
from src.state.game_state import GameState


class GameController:
    def __init__(self, rules: GameRules, state: GameState, starting_player: GameState.Player):
        self.rules = rules
        self.state = state
        self.current_player = starting_player

    def apply_move(self, move: GameRules.Move) -> bool:
        # somewhere here state.place_player or place_wall based on move type
        raise NotImplementedError("Move application not implemented yet")
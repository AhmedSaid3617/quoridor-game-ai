from src.rules.game_rules import GameRules
from src.state.game_state import GameState


class StateController:
    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def apply_pawn_move(self, player: GameState.Player, move: GameRules.PawnMove):
        if move.system == GameRules.PawnMove.SystemType.ABSOLUTE:
            self.game_state.place_player(player, move.position)
        else:
            position  = self.game_state.player_one if self.game_state.active_player == GameState.Player.PLAYER_ONE else self.game_state.player_two
            self.game_state.place_player(player, position + GameRules.movement_to_delta(move.movement))

    def apply_wall_move(self, player: GameState.Player, move: GameRules.WallMove):
        if player == GameState.Player.PLAYER_ONE:
            self.game_state.player_one_remaining_walls -= 1
        else:
            self.game_state.player_two_remaining_walls -= 1

        self.game_state.place_wall(move.wall, move.position)

    def get_player_position(self, player: GameState.Player) -> GameState.Position:
        if player == GameState.Player.PLAYER_ONE:
            return self.game_state.player_one
        else:
            return self.game_state.player_two
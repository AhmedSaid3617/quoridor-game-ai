from copy import copy
from src.controller.state_controller import StateController
from src.rules.game_rules import GameRules
from src.state.game_state import GameState, GameStateBiased


class GameController:
    def __init__(self, game_state: GameState):
        
        self.game_state = game_state
        self.state_controller = StateController(self.game_state)
        self.rules = GameRules(self.game_state.get_biased_for_player(self.game_state.active_player))
        self.done = [copy(self.game_state)]
        self.undone = []

    def check_winner(self) -> GameState.Player | None:
        if self.game_state.player_one.y == 0:
            return GameState.Player.PLAYER_ONE
        elif self.game_state.player_two.y == 8:
            return GameState.Player.PLAYER_TWO
        else:
            return None
    
    def apply_move(self, move: GameRules.Move) -> bool:
        self.rules = GameRules(self.game_state.get_biased_for_player(self.game_state.active_player))
        
        
        if isinstance(move, GameRules.PawnMove):
            if self.rules.can_apply_pawn_move(move, self.game_state.active_player):     # If this player can move to this position.
                self.state_controller.apply_pawn_move(self.game_state.active_player, move)
                self.undone.clear()
                self.done.append(copy(self.game_state))
                return True
            
        elif isinstance(move, GameRules.WallMove):
            if self.rules.can_apply_wall_move(self.game_state.active_player, move): # If this player can play this wall move.
                self.state_controller.apply_wall_move(self.game_state.active_player, move)
                self.undone.clear()
                self.done.append(copy(self.game_state))
                return True
                
        else:
            raise ValueError("Unknown move type")
        
    def undo(self):
        if len(self.done) > 1:
            self.undone.append(self.done.pop())
            self._transfer_state(self.done[-1], self.game_state)
        else:
            raise IndexError("No more moves to undo.")


    def redo(self):
        if len(self.undone) > 0:
            self.done.append(self.undone.pop())
            self._transfer_state(self.done[-1], self.game_state)
        else:
            raise IndexError("No more moves to redo.")


    def _transfer_state(self, from_state: GameState, to_state: GameState):
        to_state.player_one = from_state.player_one.__copy__()
        to_state.player_two = from_state.player_two.__copy__()
        to_state.player_one_remaining_walls = from_state.player_one_remaining_walls
        to_state.player_two_remaining_walls = from_state.player_two_remaining_walls
        to_state.active_player = from_state.active_player
        to_state.vertical_edges = [row[:] for row in from_state.vertical_edges]
        to_state.horizontal_edges = [row[:] for row in from_state.horizontal_edges]

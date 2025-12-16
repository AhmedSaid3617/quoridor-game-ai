from src.controller.state_controller import StateController
from src.rules.game_rules import GameRules
from src.state.game_state import GameState, GameStateBiased


class GameController:
    def __init__(self, game_state: GameState, starting_player: GameState.Player):
        
        self.game_state = game_state
        self.state_controller = StateController(self.game_state)
        self.current_player = starting_player
        self.rules = GameRules(self.game_state.get_biased_for_player(GameState.Player.PLAYER_TWO if self.current_player == GameState.Player.PLAYER_ONE else GameState.Player.PLAYER_ONE))

    def check_winner(self) -> GameState.Player | None:
        if self.game_state.player_one.y == 0:
            return GameState.Player.PLAYER_ONE
        elif self.game_state.player_two.y == 8:
            return GameState.Player.PLAYER_TWO
        else:
            return None
    
    def apply_move(self, move: GameRules.Move) -> bool:
        self.rules = GameRules(self.game_state.get_biased_for_player(GameState.Player.PLAYER_TWO if self.current_player == GameState.Player.PLAYER_ONE else GameState.Player.PLAYER_ONE))
        
        if isinstance(move, GameRules.PawnMove):
            if self.rules.can_apply_pawn_move(move, self.game_state.active_player):     # If this player can move to this position.
                self.state_controller.apply_pawn_move(self.game_state.active_player, move)
                #self._flip_active_player()
                return True
            
        elif isinstance(move, GameRules.WallMove):
            if self.rules.can_apply_wall_move(self.game_state.active_player, move): # If this player can play this wall move.
                self.state_controller.apply_wall_move(self.game_state.active_player, move)
                #self._flip_active_player()
                return True
                
        else:
            raise ValueError("Unknown move type")
        

    def _flip_active_player(self):
        if self.current_player == GameState.Player.PLAYER_ONE:
            self.current_player = GameState.Player.PLAYER_TWO
            
        elif self.current_player == GameState.Player.PLAYER_TWO:
            self.current_player = GameState.Player.PLAYER_ONE

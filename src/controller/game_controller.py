from src.rules.game_rules import GameRules
from src.state.game_state import GameState


class GameController:
    def __init__(self, game_state: GameState, starting_player: GameState.Player):
        
        self.game_state = game_state
        self.current_player = starting_player
        self.rules = GameRules()

    def check_winner(self) -> GameState.Player | None:
        if self.game_state.player_one.y == 0:
            return GameState.Player.PLAYER_ONE
        elif self.game_state.player_two.y == 8:
            return GameState.Player.PLAYER_TWO
        else:
            return None
    
    def apply_move(self, move: GameRules.Move) -> bool:

        if isinstance(move, GameRules.PawnMove):
            if self.rules.can_apply_pawn_placement(move, self.game_state.active_player):     # If this player can move to this position.
                self.game_state.place_player(self.game_state.active_player, move.position)  # Then move him.
                return True
            
        elif isinstance(move, GameRules.WallMove):
            if self.rules.can_apply_wall_move(self.game_state.active_player, move): # If this player can play this wall move.
                self.game_state.place_wall(move.wall, move.position) # Then place a wall at this postion.
                return True
                
        else:
            raise ValueError("Unknown move type")
        

        
        return False
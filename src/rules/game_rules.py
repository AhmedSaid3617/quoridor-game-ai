from abc import abstractmethod
from enum import Enum
from src.state import GameState

class GameRules:
    class Move:
        @abstractmethod
        def __str__(self):
            raise NotImplementedError

    """
    Incremental movement of a pawn in one of the four cardinal directions.
    """
    class PawnMove(Move):
        class MovementType(Enum):
            UP = "UP"
            RIGHT = "RIGHT"
            DOWN = "DOWN"
            LEFT = "LEFT"
            NE = "NE"
            SE = "SE"
            SW = "SW"
            NW = "NW"
            
        def __init__(self, movement: MovementType):
            self.movement = movement

        def __str__(self):
            return f"Move {str.lower(self.movement.value)}"


    """
    Placement of a wall (vertical or horizontal).
    """
    class WallMove(Move):
            
        def __init__(self, wall: GameState.Wall, position: GameState.Position):
            self.wall = wall
            self.position = position

        def __str__(self):
            return f"Place {str.lower(self.wall.value)} wall at {self.position}"               


    def __init__(self, game_state: GameState = GameState()):
        self.game_state = game_state


    def _get_players_info(self):
        """
        Returns a tuple:
        (player_one_enum, player_one_position, player_two_enum, player_two_position)
        """
        return (
            self.game_state.Player.PLAYER_ONE,
            self.game_state.player_one,
            self.game_state.Player.PLAYER_TWO,
            self.game_state.player_two
        )

    def _get_current_and_opponent_positions(self, position: GameState.Position):
        """
        Returns (current_player_position, opponent_player_position) based on the input position.
        If the position does not match either player, current_player is the input position, opponent is None.
        """
        _, player_one_pos, _, player_two_pos = self._get_players_info()
        if position == player_one_pos:
            return player_one_pos, player_two_pos
        elif position == player_two_pos:
            return player_two_pos, player_one_pos
        else:
            return position, None

    # TODO: implement special cases, hitting a player
###################################### Regular moves ######################################
    def _can_move_up(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)
        if current_player.y == 0:
            return False
        if self.game_state.horizontal_edges[current_player.y - 1][current_player.x]:
            return False
        if opponent_player is not None:
            if (current_player.x == opponent_player.x) and (current_player.y == opponent_player.y + 1):
                return False
        return True
    
    def _can_move_right(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)
        if current_player.x == 8:
            return False
        if self.game_state.vertical_edges[current_player.y][current_player.x]:
            return False
        if opponent_player is not None:
            if (current_player.y == opponent_player.y) and (current_player.x == opponent_player.x - 1):
                return False
        return True

    def _can_move_down(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)

        if current_player.y == 8:
            return False
        if self.game_state.horizontal_edges[current_player.y][current_player.x]:
            return False
        if opponent_player is not None:
            if (current_player.x == opponent_player.x) and (current_player.y == opponent_player.y - 1):
                return False
        return True
    
    def _can_move_left(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)
        if current_player.x == 0:
            return False
        if self.game_state.vertical_edges[current_player.y][current_player.x - 1]:
            return False
        if opponent_player is not None:
            if (current_player.y == opponent_player.y) and (current_player.x == opponent_player.x + 1):
                return False
        return True

###################################### special jumps ######################################
    def _can_jump_up(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)

        if (opponent_player.y == current_player.y - 1) and (self._can_move_up(self,opponent_player)):  
            return True
        else:
            return False
        
    def _can_jump_down(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)

        if(opponent_player.y == current_player.y + 1) and (self._can_move_down(self,opponent_player)):  
            return True
        else:
            return False
    
    def _can_jump_right(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)

        if (opponent_player.x == current_player.x + 1) and (self._can_move_right(self,opponent_player)):  
            return True
        else:
            return False
    
    def _can_jump_left(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)

        if (opponent_player.x == current_player.x - 1) and (self._can_move_left(self,opponent_player)):  
            return True
        else:
            return False

################################## special diagonal moves #################################
    def _can_move_ne(self, position: GameState.Position) -> bool:
        raise NotImplementedError("Diagonal movement not implemented yet")
    
    def _can_move_nw(self, position: GameState.Position) -> bool:
        raise NotImplementedError("Diagonal movement not implemented yet")
    
    def _can_move_se(self, position: GameState.Position) -> bool:
        raise NotImplementedError("Diagonal movement not implemented yet")
    
    def _can_move_sw(self, position: GameState.Position) -> bool:
        raise NotImplementedError("Diagonal movement not implemented yet")
    
    
    def can_apply_pawn_move(self, position: GameState.Position, pawn_move: PawnMove) -> bool:
        movement = pawn_move.movement
        if movement == GameRules.PawnMove.MovementType.UP:
            return self._can_move_up(position)
        elif movement == GameRules.PawnMove.MovementType.RIGHT:
            return self._can_move_right(position)
        elif movement == GameRules.PawnMove.MovementType.DOWN:
            return self._can_move_down(position)
        elif movement == GameRules.PawnMove.MovementType.LEFT:
            return self._can_move_left(position)
        elif movement == GameRules.PawnMove.MovementType.NE:
            return self._can_move_ne(position)
        elif movement == GameRules.PawnMove.MovementType.SE:
            return self._can_move_se(position)
        elif movement == GameRules.PawnMove.MovementType.SW:
            return self._can_move_sw(position)
        elif movement == GameRules.PawnMove.MovementType.NW:
            return self._can_move_nw(position)
        else:
            raise ValueError("Invalid pawn move")

    def can_apply_wall_move(self, player: GameState.Player, wall_move: WallMove) -> bool:
        # Check if player has remaining walls
        # TODO:
        wall, position = wall_move.wall, wall_move.position
        try:
            self.game_state.place_wall(wall, position)
            return True
        except ValueError:
            return False
        
        # BFS or DFS to check if both players have a path to their goal
        # Use helper function
        raise NotImplementedError("Pathfinding check not implemented yet")


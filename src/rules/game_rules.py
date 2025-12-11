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

    # TODO: implement special cases, hitting a player
    def _can_move_up(self, position: GameState.Position) -> bool:
        if position.y == 0:
            return False
        if self.game_state.horizontal_edges[position.y - 1][position.x]:
            return False
        return True
    
    def _can_move_right(self, position: GameState.Position) -> bool:
        if position.x == 8:
            return False
        if self.game_state.vertical_edges[position.y][position.x]:
            return False
        return True

    def _can_move_down(self, position: GameState.Position) -> bool:
        if position.y == 8:
            return False
        if self.game_state.horizontal_edges[position.y][position.x]:
            return False
        return True
    
    def _can_move_left(self, position: GameState.Position) -> bool:
        if position.x == 0:
            return False
        if self.game_state.vertical_edges[position.y][position.x - 1]:
            return False
        return True
    
    def _can_move_se(self, position: GameState.Position) -> bool:
        raise NotImplementedError("Diagonal movement not implemented yet")
    
    def _can_move_sw(self, position: GameState.Position) -> bool:
        raise NotImplementedError("Diagonal movement not implemented yet")
    
    def _can_move_ne(self, position: GameState.Position) -> bool:
        raise NotImplementedError("Diagonal movement not implemented yet")
    
    def _can_move_nw(self, position: GameState.Position) -> bool:
        raise NotImplementedError("Diagonal movement not implemented yet")
    
    def can_apply_pawn_placement(self, position: GameState.Position, player:GameState.Player) -> bool:
        return True
        # TODO: implement this.
    
    def can_apply_pawn_move(self, pawn_move:PawnMove, player:GameState.Player) -> bool:
        # TODO: implement this.
        return True
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
        # TODO: implement this
        return True
        wall, position = wall_move.wall, wall_move.position
        try:
            self.game_state.place_wall(wall, position)
            return True
        except ValueError:
            return False
        
        # BFS or DFS to check if both players have a path to their goal
        # Use helper function
        raise NotImplementedError("Pathfinding check not implemented yet")
    
    
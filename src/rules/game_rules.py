from abc import abstractmethod
from enum import Enum
from typing import Tuple
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
            JUMP_UP = "JUMP_UP"
            RIGHT = "RIGHT"
            DOWN = "DOWN"
            JUMP_DOWN = "JUMP_DOWN"
            LEFT = "LEFT"
            NE = "NE"
            SE = "SE"
            SW = "SW"
            NW = "NW"

        class SystemType(Enum):
            RELATIVE = "RELATIVE"
            ABSOLUTE = "ABSOLUTE"
            
        def __init__(self, system: SystemType, movement: MovementType = None, position: GameState.Position = None):
            self.system = system
            if system == self.SystemType.RELATIVE:
                self.movement = movement
            else:
                self.position = position

        def __str__(self):
            if self.system == self.SystemType.ABSOLUTE:
                return f"Move to {self.position}"
            else:
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
    
    
    def can_apply_pawn_move(self, pawn_move:PawnMove, player:GameState.Player) -> bool:
        if pawn_move.system == GameRules.PawnMove.SystemType.ABSOLUTE: # change to relative
            movement = None # should not be ABSOLUTE
            if (player == GameState.Player.PLAYER_ONE):
                delta = self.game_state.player_one - pawn_move.position
            elif (player  == GameState.Player.PLAYER_TWO):
                delta = self.game_state.player_two - pawn_move.position

            movement = self._delta_to_movement(delta)

            if not movement:
                return False # Not in any possible move
        else:
            movement = pawn_move.movement # Relative

        position = self.game_state.player_one if player == GameState.Player.PLAYER_ONE else self.game_state.player_two

        return self._can_handler(movement, position)

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
    
    
    @staticmethod
    def _movement_to_delta_dict() -> Tuple:
        return {
            GameRules.PawnMove.MovementType.UP:    (0, 1),
            GameRules.PawnMove.MovementType.DOWN:  (0, -1),
            GameRules.PawnMove.MovementType.LEFT:  (-1, 0),
            GameRules.PawnMove.MovementType.RIGHT: (1, 0),
            GameRules.PawnMove.MovementType.NE:    (1, 1),
            GameRules.PawnMove.MovementType.SE:    (1, -1),
            GameRules.PawnMove.MovementType.SW:    (-1, -1),
            GameRules.PawnMove.MovementType.NW:    (-1, 1),
        }


    @staticmethod
    def _delta_to_movement(delta) -> GameRules.PawnMove.MovementType | None:
        # reverse the dictionary
        lookup = {v: k for k, v in GameRules._movement_to_delta_dict().items()}

        if delta in lookup:
            return lookup[delta]
        
        return None
    
    @staticmethod
    def movement_to_delta(delta) -> Tuple:
        lookup = GameRules._movement_to_delta_dict()

        if delta in lookup:
            return lookup[delta]
        
        return None
    
    def _can_handler(self, movement, position):
        handlers = {
            GameRules.PawnMove.MovementType.UP:    self._can_move_up,
            GameRules.PawnMove.MovementType.RIGHT: self._can_move_right,
            GameRules.PawnMove.MovementType.DOWN:  self._can_move_down,
            GameRules.PawnMove.MovementType.LEFT:  self._can_move_left,
            GameRules.PawnMove.MovementType.NE:    self._can_move_ne,
            GameRules.PawnMove.MovementType.SE:    self._can_move_se,
            GameRules.PawnMove.MovementType.SW:    self._can_move_sw,
            GameRules.PawnMove.MovementType.NW:    self._can_move_nw,
            # TODO: others
        }

        if movement in handlers:
            return handlers[movement](position)
        
        raise ValueError(f"Invalid pawn movement: {movement}")
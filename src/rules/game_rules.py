from abc import abstractmethod
from enum import Enum
from typing import Set, Tuple
from src.state import GameState
from src.state.game_state import GameStateBiased

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
            
        def __eq__(self, other):
            return self.system == other.system and (self.movement == other.movement or self.position == other.position)
        
        def __hash__(self):
            return hash((self.system, self.movement)) if self.system == self.SystemType.RELATIVE  else hash((self.system, self.position))
    
    """
    Placement of a wall (vertical or horizontal).
    """
    class WallMove(Move):
            
        def __init__(self, wall: GameState.Wall, position: GameState.Position):
            self.wall = wall
            self.position = position

        def __str__(self):
            return f"Place {str.lower(self.wall.value)} wall at {self.position}"               


    def __init__(self, game_state: GameStateBiased):
        if not isinstance(game_state, GameStateBiased):
            raise ValueError("Need a biased game state to know the position of opponent")
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
        return position, self.game_state.opponent

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

        if (opponent_player.x == current_player.x)and(opponent_player.y == current_player.y - 1) and (self._can_move_up(opponent_player)):  
            return True
        else:
            return False
        
    def _can_jump_down(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)

        if(opponent_player.x == current_player.x) and (opponent_player.y == current_player.y + 1) and (self._can_move_down(opponent_player)):  
            return True
        else:
            return False
    
    def _can_jump_right(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)

        if (opponent_player.y == current_player.y) and(opponent_player.x == current_player.x + 1) and (self._can_move_right(opponent_player)):  
            return True
        else:
            return False
    
    def _can_jump_left(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)

        if (opponent_player.y == current_player.y) and(opponent_player.x == current_player.x - 1) and (self._can_move_left(opponent_player)):  
            return True
        else:
            return False

################################## special diagonal moves #################################
    def _can_move_ne(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)
        same_x = (opponent_player.x == current_player.x)
        same_y = (opponent_player.y == current_player.y)

        oppnentIsAbove = (opponent_player.y == current_player.y - 1) and same_x
        opponentIsRight = (opponent_player.x == current_player.x + 1) and same_y

        jump_up_blocked    = not self._can_jump_up(current_player)
        jump_right_blocked = not self._can_jump_right(current_player)

        oppnent_can_move_right = self._can_move_right(opponent_player)
        oppnent_can_move_up    = self._can_move_up(opponent_player)

        if same_x and oppnentIsAbove and jump_up_blocked: 
            if oppnent_can_move_right: 
                return True
            else:
                return False
        elif same_y and opponentIsRight and jump_right_blocked:
            if oppnent_can_move_up:
                return True
            else: 
                return False
        else:
            return False
        
    def _can_move_nw(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)
        same_x = (opponent_player.x == current_player.x)
        same_y = (opponent_player.y == current_player.y)

        oppnentIsAbove  = (opponent_player.y == current_player.y - 1)
        opponentIsLeft = (opponent_player.x == current_player.x - 1) and same_y

        jump_up_blocked    = not self._can_jump_up(current_player)
        jump_left_blocked  = not self._can_jump_left(current_player)

        oppnent_can_move_left = self._can_move_left(opponent_player)
        oppnent_can_move_down = self._can_move_down(opponent_player)

        if same_x and oppnentIsAbove and jump_up_blocked:
            
            if oppnent_can_move_left: 
                return True
            else:
                return False
        elif same_y and opponentIsLeft and jump_left_blocked:
            if oppnent_can_move_down:
                return True
            else:
                return False
        else:
            return False
    
    def _can_move_se(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)
        same_x = (opponent_player.x == current_player.x)
        same_y = (opponent_player.y == current_player.y)

        oppnentIsBelow  = (opponent_player.y == current_player.y + 1)
        opponentIsRight = (opponent_player.x == current_player.x + 1) and same_y

        jump_down_blocked    = not self._can_jump_down(current_player)
        jump_right_blocked   = not self._can_jump_right(current_player)

        oppnent_can_move_down = self._can_move_down(opponent_player)
        oppnent_can_move_right = self._can_move_right(opponent_player)

        if same_x and oppnentIsBelow and jump_down_blocked:
            
            if oppnent_can_move_right: 
                return True
            else:
                return False
        elif same_y and opponentIsRight and jump_right_blocked:
            if oppnent_can_move_down:
                return True
            else:
                return False
        else:
            return False
    
    
    def _can_move_sw(self, position: GameState.Position) -> bool:
        current_player, opponent_player = self._get_current_and_opponent_positions(position)
        same_x = (opponent_player.x == current_player.x)
        same_y = (opponent_player.y == current_player.y)

        oppnentIsBelow  = (opponent_player.y == current_player.y + 1)
        opponentIsLeft = (opponent_player.x == current_player.x - 1) and same_y

        jump_down_blocked    = not self._can_jump_down(current_player)
        jump_left_blocked   = not self._can_jump_left(current_player)

        oppnent_can_move_down = self._can_move_down(opponent_player)
        oppnent_can_move_left = self._can_move_left(opponent_player)

        if same_x and oppnentIsBelow and jump_down_blocked:
            
            if oppnent_can_move_left: 
                return True
            else:
                return False
        elif same_y and opponentIsLeft and jump_left_blocked:
            if oppnent_can_move_down:
                return True
            else:
                return False
        else:
            return False
    
    
    
    
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
            GameRules.PawnMove.MovementType.UP:         (0, -1),
            GameRules.PawnMove.MovementType.JUMP_UP:    (0, -2),
            GameRules.PawnMove.MovementType.DOWN:       (0, 1),
            GameRules.PawnMove.MovementType.JUMP_DOWN:  (0, 2),
            GameRules.PawnMove.MovementType.LEFT:       (-1, 0),
            GameRules.PawnMove.MovementType.RIGHT:      (1, 0),
            GameRules.PawnMove.MovementType.NE:         (1, -1),
            GameRules.PawnMove.MovementType.SE:         (1, 1),
            GameRules.PawnMove.MovementType.SW:         (-1, 1),
            GameRules.PawnMove.MovementType.NW:         (-1, -1),
        }


    @staticmethod
    def _delta_to_movement(delta) -> PawnMove.MovementType | None:
        # reverse the dictionary
        lookup = {v: k for k, v in GameRules._movement_to_delta_dict().items()}

        if delta in lookup:
            return lookup[delta]
        
        return None
    
    @staticmethod
    def movement_to_delta(movement) -> Tuple:
        lookup = GameRules._movement_to_delta_dict()

        if movement in lookup:
            return lookup[movement]
        
        return None
    
    def _movement_to_handler_dict(self):
        return {
            GameRules.PawnMove.MovementType.UP:         self._can_move_up,
            GameRules.PawnMove.MovementType.JUMP_UP:    self._can_jump_up,
            GameRules.PawnMove.MovementType.RIGHT:      self._can_move_right,
            GameRules.PawnMove.MovementType.DOWN:       self._can_move_down,
            GameRules.PawnMove.MovementType.JUMP_DOWN:  self._can_jump_down,
            GameRules.PawnMove.MovementType.LEFT:       self._can_move_left,
            GameRules.PawnMove.MovementType.NE:         self._can_move_ne,
            GameRules.PawnMove.MovementType.SE:         self._can_move_se,
            GameRules.PawnMove.MovementType.SW:         self._can_move_sw,
            GameRules.PawnMove.MovementType.NW:         self._can_move_nw,
        }

    def _can_handler(self, movement, position):
        handlers = self._movement_to_handler_dict()

        if movement in handlers:
            return handlers[movement](position)
        
        raise ValueError(f"Invalid pawn movement: {movement}")
    
    def all_pawn_moves_relative(self, player: GameState.Player) -> Set[PawnMove]:
        position = self.game_state.player_one if player == GameState.Player.PLAYER_ONE else self.game_state.player_two
        valid_moves = set()

        for move_type, handler in self._movement_to_handler_dict().items():
            if handler(position):
                new_move = GameRules.PawnMove(system=GameRules.PawnMove.SystemType.RELATIVE, movement=move_type)
                valid_moves.add(new_move)

        return valid_moves
    
    def all_pawn_moves_absolute(self, player: GameState.Player) -> Set[PawnMove]:
        position = self.game_state.player_one if player == GameState.Player.PLAYER_ONE else self.game_state.player_two
        valid_moves = set()

        for move_type, handler in self._movement_to_handler_dict().items():
            if handler(position):
                new_move = GameRules.PawnMove(system=GameRules.PawnMove.SystemType.ABSOLUTE, position=(position + self.movement_to_delta(move_type)))
                valid_moves.add(new_move)

        return valid_moves
    #get all pawn movies absolute using the player and current position as input
    def all_pown_moves_absolute_using_position(self,player: GameState.Player,c_position : GameState.Position) -> Set[PawnMove]:
        position = c_position
        valid_moves = set()

        for move_type, handler in self._movement_to_handler_dict().items():
            if handler(position):
                new_move = GameRules.PawnMove(system=GameRules.PawnMove.SystemType.RELATIVE, movement=move_type)
                valid_moves.add(new_move)

        return valid_moves
        
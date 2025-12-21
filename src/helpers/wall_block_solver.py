from typing import List
from src.helpers.path import Path
from src.helpers.path_solver import PathSolver
from src.rules.game_rules import GameRules
from src.state.game_state import GameState


class WallBlockSolver:
    def __init__(self, state: GameState, player: GameState.Player):
        self.game_state = state
        self.player = player

    """
    @returns a WallMove that blocks the given PawnMove at the given Position,
    True if the move is already blocked,
    or False if blocking is not possible.
    """
    def solve(self, position: GameState.Position, move: GameRules.PawnMove) -> List[GameRules.WallMove] | bool:
        wall_moves = set()

        if move.system == GameRules.PawnMove.SystemType.ABSOLUTE:
            raise ValueError("Need a relative move not absolute move")
        
        rules  = GameRules(self.game_state.get_biased_for_player(self.player))
        if move.movement == GameRules.PawnMove.MovementType.UP:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x, position.y - 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y - 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
  
        elif move.movement == GameRules.PawnMove.MovementType.JUMP_UP:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x, position.y - 2))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y - 2))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
        elif move.movement == GameRules.PawnMove.MovementType.RIGHT:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x, position.y))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x, position.y - 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
        elif move.movement == GameRules.PawnMove.MovementType.JUMP_RIGHT:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x + 1, position.y))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x + 1, position.y - 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
        elif move.movement == GameRules.PawnMove.MovementType.DOWN:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x, position.y))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x - 1, position.y))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
                
        elif move.movement == GameRules.PawnMove.MovementType.JUMP_DOWN:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x, position.y + 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x - 1, position.y + 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
                        
        elif move.movement == GameRules.PawnMove.MovementType.LEFT:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y - 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
        elif move.movement == GameRules.PawnMove.MovementType.JUMP_LEFT:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 2, position.y))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 2, position.y - 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
        elif move.movement == GameRules.PawnMove.MovementType.NE:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x, position.y - 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
        elif move.movement == GameRules.PawnMove.MovementType.SE:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x, position.y + 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
        elif move.movement == GameRules.PawnMove.MovementType.SW:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y + 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
        elif move.movement == GameRules.PawnMove.MovementType.NW:
            if not rules.can_handler(move.movement, position):
                return True # No wall blocking needed, already blocked
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y - 1))
            if rules.can_apply_wall_move(self.player, wall_move):
                wall_moves.add(wall_move)
            
        else:
            raise ValueError("Invalid pawn move: " + str(move))    

        return list(wall_moves)
    
    def solve_optimum_on_path(self, path: Path) -> GameRules.WallMove | bool:
        raise NotImplementedError("Wall blocking check not implemented yet")
    
    def get_wall_moves_on_opt_paths(self) -> List[GameRules.WallMove]:
        wall_moves = set()

        if self.player == GameState.Player.PLAYER_ONE:
            paths = PathSolver.solve_all_optimum(GameState.Player.PLAYER_ONE, 0, self.game_state)
        else:
            paths = PathSolver.solve_all_optimum(GameState.Player.PLAYER_TWO, 8, self.game_state)
        
        for path in paths:
            current_position = path.start
            for move in path.path: # path is relative

                solution = self.solve(current_position, move)
                if isinstance(solution, list):
                    for m in solution:
                        wall_moves.add(m)
                
                t = current_position + GameRules.movement_to_delta(move.movement)
                current_position = GameState.Position(t[0], t[1])


        return list(wall_moves)
        
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
    def solve(self, position: GameState.Position, move: GameRules.PawnMove) -> GameRules.WallMove | bool:
        rules  = GameRules(self.game_state)
        if move == GameRules.PawnMove.MovementType.UP:
            if not rules._can_move_up(position):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x, position.y - 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y - 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
        if move == GameRules.PawnMove.MovementType.JUMP_UP:
            if not rules._can_jump_up(position):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x, position.y - 2))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y - 2))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
        elif move == GameRules.PawnMove.MovementType.RIGHT:
            if not rules.can_apply_pawn_move(position, move):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x, position.y))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x, position.y - 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
        elif move == GameRules.PawnMove.MovementType.JUMP_RIGHT:
            if not rules.can_apply_pawn_move(position, move):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x + 1, position.y))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x + 1, position.y - 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
        elif move == GameRules.PawnMove.MovementType.DOWN:
            if not rules.can_apply_pawn_move(position, move):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x, position.y))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x - 1, position.y))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
                
        elif move == GameRules.PawnMove.MovementType.JUMP_DOWN:
            if not rules.can_apply_pawn_move(position, move):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x, position.y + 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
            wall_move = GameRules.WallMove(GameState.Wall.HORIZONTAL, GameState.Position(position.x - 1, position.y + 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
                        
        elif move == GameRules.PawnMove.MovementType.LEFT:
            if not rules.can_apply_pawn_move(position, move):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y - 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
        elif move == GameRules.PawnMove.MovementType.LEFT:
            if not rules.can_apply_pawn_move(position, move):
                return True # No wall blocking needed, already blocked

            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 2, position.y))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 2, position.y - 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
        elif move == GameRules.PawnMove.MovementType.NE:
            if not rules.can_apply_pawn_move(position, move):
                return True # No wall blocking needed, already blocked
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x, position.y - 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
        elif move == GameRules.PawnMove.MovementType.SE:
            if not rules.can_apply_pawn_move(position, move):
                return True # No wall blocking needed, already blocked
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x, position.y + 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
        elif move == GameRules.PawnMove.MovementType.SW:
            if not rules.can_apply_pawn_move(position, move):
                return True # No wall blocking needed, already blocked
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y + 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
        elif move == GameRules.PawnMove.MovementType.NW:
            if not rules.can_apply_pawn_move(position, move):
                return True # No wall blocking needed, already blocked
            
            wall_move = GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(position.x - 1, position.y - 1))
            if rules.can_place_wall(self.player, wall_move):
                return wall_move
            
        else:
            raise ValueError("Invalid pawn move")    

        return False # No wall blocking possible
    
    def solve_optimum_on_path(self, path: Path) -> GameRules.WallMove | bool:
        raise NotImplementedError("Wall blocking check not implemented yet")
    
    def get_wall_moves_on_opponent_opt_paths(self) -> List[GameRules.WallMove]:
        wall_moves = set()

        if self.player == GameState.Player.PLAYER_ONE:
            paths = PathSolver.solve_all_optimum(GameState.Player.PLAYER_TWO, 8, self.game_state)
        else:
            paths = PathSolver.solve_all_optimum(GameState.Player.PLAYER_ONE, 0, self.game_state)

        for path in paths:
            current_position = path.start
            for move in path.path: # path is relative
                t = current_position + GameRules.movement_to_delta(move.movement)
                current_position = GameState.Position(t[0], t[1])

                result = self.solve(current_position, move)
                if isinstance(result, GameRules.WallMove):
                    wall_moves.add(result)


        return list(wall_moves)
        
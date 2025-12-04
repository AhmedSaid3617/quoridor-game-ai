from typing import List
from src.rules.game_rules import GameRules
from src.state.game_state import GameState


class WallBlockSolver:
    def solve(position: GameState.Position, move: GameRules.PawnMove) -> GameRules.WallMove | None:
        raise NotImplementedError("Wall blocking check not implemented yet")
    
    def solve_optimum_on_path() -> GameRules.WallMove | None:
        raise NotImplementedError("Wall blocking check not implemented yet")
from typing import List
from src.helpers.path import Path
from src.state.game_state import GameState


class PathSolver:
    def solve_any(start: GameState.Position, goal_y: int, game_state: GameState) -> Path:
        raise NotImplementedError("BFS pathfinding not implemented yet")
    
    def solve_optimum(start: GameState.Position, goal_y: int, game_state: GameState) -> Path:
        raise NotImplementedError("BFS pathfinding not implemented yet")
    
    def solve_all_optimum(start: GameState.Position, goal_y: int, game_state: GameState) -> List[Path]:
        raise NotImplementedError("BFS pathfinding not implemented yet")
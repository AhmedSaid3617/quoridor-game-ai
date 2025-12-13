from typing import List
from src.helpers.path import Path
from src.state.game_state import GameState
from src.rules.game_rules import *
from src.controller.state_controller import StateController
from src.state.game_state import *


class PathSolver:
    def solve_any(start: GameState.Position, goal_y: int, game_state: GameState) -> Path:
        return PathSolver.solve_optimum(start, goal_y, game_state)
    
    def solve_optimum(player: GameState.Player, goal_y: int, game_state: GameState) -> Path:
        my_state = game_state.__copy__()
        #9*9 matrix for visited positions
        visited = [[False for _ in range(9)] for _ in range(9)]
        #bfs queue of pathes
        bfs_queue: List[Path] = []
        rules = GameRules(game_state)
        state_controller = StateController(my_state)
        initial_postion = state_controller.get_player_position(player, my_state)
        initial_path = Path(start=initial_postion, path=[])
        bfs_queue.append(initial_path)
        while bfs_queue:
            current_path = bfs_queue.pop(0)
            current_position = current_path.end
            
            if current_position.y == goal_y:
                return current_path
                        
                
            available_moves = rules.all_pown_moves_absolute_using_position(player,current_position)
            for move in available_moves:
                dx,dy=rules.movement_to_delta(move)
                new_position = Position(x=current_position.x+dx, y=current_position.y+dy)
                if not visited[new_position.y][new_position.x]:
                    new_path = Path(start=current_path.start, path=current_path.path + [move])
                    bfs_queue.append(new_path)
                    visited[new_position.y][new_position.x] = True
           
        return None
    #private function that takes the visited matrix and move to mark this move positions as visited


    def solve_all_optimum(player: GameState.Player, goal_y: int, game_state: GameState) -> List[Path]:
    # 1. Use Distance Matrix (Integers), not Boolean
        min_dist = [[999 for _ in range(9)] for _ in range(9)]

        bfs_queue = []
        paths = []

        rules = GameRules(game_state)
        state_controller = StateController(game_state)

        initial_pos = state_controller.get_player_position(player, game_state)
        bfs_queue.append(Path(start=initial_pos, path=[]))

        min_dist[initial_pos.y][initial_pos.x] = 0

        shortest_len = None

        while bfs_queue:
            current_path = bfs_queue.pop(0)
            current_pos = current_path.end
            current_len = current_path.length() # or len(current_path.path)

            # Optimization: Stop if we are exceeding the best length found
            if shortest_len is not None and current_len > shortest_len:
                break

            # Goal Check
            if current_pos.y == goal_y:
                if shortest_len is None:
                    shortest_len = current_len

                if current_len == shortest_len:
                    paths.append(current_path)
                continue

            # Expansion
            # Don't expand if we are already worse than the best solution
            if shortest_len is not None and current_len >= shortest_len:
                continue

            available_moves = rules.all_pown_moves_absolute_using_position(player, current_pos)

            for move in available_moves:
                dx, dy = rules.movement_to_delta(move)
                nx, ny = current_pos.x + dx, current_pos.y + dy

                new_len = current_len + 1

                # THE FIX: Allow merge if new path is <= existing best path
                if new_len <= min_dist[ny][nx]:
                    min_dist[ny][nx] = new_len
                    new_path = Path(start=current_path.start, path=current_path.path + [move])
                    bfs_queue.append(new_path)

        return paths
from src.state import GameState

class GameRules:
    def __init__(self, game_state: GameState = GameState()):
        self.game_state = game_state

    def can_move_up(self, position: GameState.Position) -> bool:
        if position.y == 0:
            return False
        if self.game_state.horizontal_edges[position.y - 1][position.x]:
            return False
        return True
    
    def can_move_right(self, position: GameState.Position) -> bool:
        if position.x == 8:
            return False
        if self.game_state.vertical_edges[position.y][position.x]:
            return False
        return True

    def can_move_down(self, position: GameState.Position) -> bool:
        if position.y == 8:
            return False
        if self.game_state.horizontal_edges[position.y][position.x]:
            return False
        return True
    
    def can_move_left(self, position: GameState.Position) -> bool:
        if position.x == 0:
            return False
        if self.game_state.vertical_edges[position.y][position.x - 1]:
            return False
        return True
    
    def can_place_wall(self, wall: GameState.Wall, position: GameState.Position) -> bool: # pragma: no cover
        try:
            self.game_state.place_wall(wall, position)
            return True
        except ValueError:
            return False
        
        # BFS or DFS to check if both players have a path to their goal
        raise NotImplementedError("Pathfinding check not implemented yet")
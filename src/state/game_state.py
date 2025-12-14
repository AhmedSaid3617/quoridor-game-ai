from enum import Enum

class GameState:


    class Position:
        def __init__(self, x: int = 0, y: int = 0):
            self.x = x
            self.y = y

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y
        
        def __copy__(self):
            return GameState.Position(self.x, self.y)

        def __str__(self):
            return f"({self.x}, {self.y})"

        def __sub__(self, other):
            return (self.x - other.x, self.y - other.y)
        
        def __add__(self, other):
            if isinstance(other, tuple):
                return (self.x + other[0], self.y + other[1])
            
            return (self.x + other.x, self.y + other.y)


    class Player(Enum):
        PLAYER_ONE = 1
        PLAYER_TWO = 2


    class Wall(Enum):
        VERTICAL = "VERTICAL"
        HORIZONTAL = "HORIZONTAL"


    def __init__(self):
        self.player_one = self.Position(4,8)
        self.player_two = self.Position(4,0)
        self.player_one_remaining_walls = 10
        self.player_two_remaining_walls = 10
        self.active_player = self.Player.PLAYER_ONE

        # vertical_edges[x][y] indicates if there is a vertical wall to the right of (x, y)
        self.vertical_edges = [[False] * 8 for _ in range(9)]

        # horizontal_edges[x][y] indicates if there is a horizontal wall below (x, y)
        self.horizontal_edges = [[False] * 9 for _ in range(8)]

    def place_player(self, player: Player, position: Position):

        if position.x < 0 or position.x >= 9 or position.y < 0 or position.y >= 9:
            raise ValueError("Invalid position: out of bounds")

        if player == self.Player.PLAYER_ONE:
            if self.player_two == position:
                raise ValueError("Invalid position: occupied by Player Two")
            
            # TODO: move this.
            self.player_one = position
            self.active_player = self.Player.PLAYER_TWO

        elif player == self.Player.PLAYER_TWO:
            if self.player_one == position:
                raise ValueError("Invalid position: occupied by Player One")
            
            # TODO: move this
            self.player_two = position
            self.active_player = self.Player.PLAYER_ONE

    # TODO: who decrements the walls?
    def place_wall(self, wall: Wall, position: Position):
        if wall == self.Wall.VERTICAL:
            if position.x < 0 or position.x > 7 or position.y < 0 or position.y > 7:
                raise ValueError("Invalid position for vertical wall")
            
            if self.vertical_edges[position.y][position.x] or self.vertical_edges[position.y + 1][position.x]:
                raise ValueError("Invalid position: a vertical wall blocks placing here")
            
            self.vertical_edges[position.y][position.x] = True
            self.vertical_edges[position.y + 1][position.x] = True

        elif wall == self.Wall.HORIZONTAL:
            if position.x < 0 or position.x > 7 or position.y < 0 or position.y > 7:
                raise ValueError("Invalid position for horizontal wall")
            
            if self.horizontal_edges[position.y][position.x] or self.horizontal_edges[position.y][position.x + 1]:
                raise ValueError("Invalid position: a horizontal wall blocks placing here")
            
            self.horizontal_edges[position.y][position.x] = True
            self.horizontal_edges[position.y][position.x + 1] = True

    def __copy__(self):
        new_state = GameState()
        new_state.player_one = self.player_one.__copy__()
        new_state.player_two = self.player_two.__copy__()
        new_state.vertical_edges = [row[:] for row in self.vertical_edges]
        new_state.horizontal_edges = [row[:] for row in self.horizontal_edges]
        return new_state
    
    def get_biased_for_player(self, opponent: GameState.Player):
        new_state = GameStateBiased(self.player_one if opponent == GameState.Player.PLAYER_TWO else self.player_two)
        new_state.player_one = self.player_one
        new_state.player_two = self.player_two.__copy__()
        new_state.vertical_edges = [row[:] for row in self.vertical_edges]
        new_state.horizontal_edges = [row[:] for row in self.horizontal_edges]
        return new_state

    

class GameStateBiased(GameState):
    def __init__(self, opponent: GameState.Position):
        super().__init__()
        self.opponent = opponent
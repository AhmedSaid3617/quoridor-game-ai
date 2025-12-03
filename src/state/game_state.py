from enum import Enum

class GameState:


    class Position:
        def __init__(self, x: int = 0, y: int = 0):
            self.x = x
            self.y = y

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y


    class Player(Enum):
        PLAYER_ONE = 1
        PLAYER_TWO = 2


    class Wall(Enum):
        VERTICAL = 1
        HORIZONTAL = 2


    def __init__(self):
        self.player_one = self.Position(4,8)
        self.player_two = self.Position(4,0)

        # vertical_edges[x][y] indicates if there is a vertical wall to the right of (x, y)
        self.vertical_edges = [9 * [[False] * 8]]

        # horizontal_edges[x][y] indicates if there is a horizontal wall below (x, y)
        self.horizontal_edges = [8 * [[False] * 9]]

    def place(self, player: Player, position: Position):
        if position.x < 0 or position.x > 9 or position.y < 0 or position.y > 9:
            raise ValueError("Invalid position: out of bounds")

        if player == self.Player.PLAYER_ONE:
            if self.player_two == position:
                raise ValueError("Invalid position: occupied by Player Two")
            
            self.player_one = position

        elif player == self.Player.PLAYER_TWO:
            if self.player_one == position:
                raise ValueError("Invalid position: occupied by Player One")
            
            self.player_two = position

    def place(self, wall: Wall, position: Position):
        if wall == self.Wall.VERTICAL:
            if position.x < 0 or position.x > 8 or position.y <= 0 or position.y > 8:
                raise ValueError("Invalid position for vertical wall")
            
            if self.vertical_edges[position.x][position.y] or self.vertical_edges[position.x][position.y - 1]:
                raise ValueError("Invalid position: a vertical wall blocks placing here")
            
            self.vertical_edges[position.x][position.y] = True
            self.vertical_edges[position.x][position.y - 1] = True

        elif wall == self.Wall.HORIZONTAL:
            if position.x < 0 or position.x >= 8 or position.y < 0 or position.y > 7:
                raise ValueError("Invalid position for horizontal wall")
            
            if self.horizontal_edges[position.x][position.y] or self.horizontal_edges[position.x + 1][position.y]:
                raise ValueError("Invalid position: a horizontal wall blocks placing here")
            
            self.horizontal_edges[position.x][position.y] = True
            self.horizontal_edges[position.x + 1][position.y] = True
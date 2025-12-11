# gui/board_view.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel

from src.controller.game_controller import GameController
from src.rules.game_rules import GameRules
from src.state.game_state import GameState

BOARD_SIZE = 9

class BoardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(BOARD_SIZE * 50, BOARD_SIZE * 50)
        self.pawns = []  # list of dicts: {"row": int, "col": int, "color": QColor}
        self.walls = []  # list of dicts: {"row": int, "col": int, "orientation": "h"/"v"}
        self.message_label = QLabel(self)
        self.message_label.setStyleSheet("""
            background-color: rgba(255,0,0,180); 
            color: white; 
            font-weight: bold;
            font-size: 16px;
            border-radius: 5px;
            padding: 5px;
        """)
        self.setMouseTracking(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.hide()
        self.legal_moves = []
        self.hovered_cell = None  # Coord(row, col) or None
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.current_wall_orientation = "H"
        self.game_state = GameState()
        self.controller = None


    def set_game_state(self, game_state: GameState):
        self.game_state = game_state

    def set_controller(self, controller: GameController):
        self.controller = controller
    
    def paint_wall(self, painter, row, col, orientation, cell_size):
        wall_thickness = int(cell_size / 5)
        if orientation == "H":
            # horizontal wall sits below the row 'row'
            x = col * cell_size
            y = (row + 1) * cell_size - wall_thickness // 2
            painter.drawRect(int(x), int(y), int(cell_size * 2), wall_thickness)
        elif orientation == "V":
            # vertical wall sits to the right of column 'col'
            x = (col + 1) * cell_size - wall_thickness // 2
            y = row * cell_size
            painter.drawRect(int(x), int(y), wall_thickness, int(cell_size * 2))


    def paintEvent(self, a0):
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(2)
        painter.setPen(pen)

        # dynamic cell size
        cell_size = min(self.width(), self.height()) / BOARD_SIZE

        # draw grid
        for i in range(BOARD_SIZE + 1):
            coord = int(i * cell_size)
            painter.drawLine(0, coord, int(BOARD_SIZE * cell_size), coord)
            painter.drawLine(coord, 0, coord, int(BOARD_SIZE * cell_size))

        """ painter.setBrush(QColor(255, 0, 0, 20))
        painter.setPen(Qt.PenStyle.NoPen) """
        painter.setBrush(QColor(255, 0, 0, 70))
        painter.setPen(Qt.PenStyle.NoPen)

        # --- Hover
        if self.hovered_cell:
            row, col = self.hovered_cell
            # TODO: draw wall preview
            self.paint_wall(painter, row, col, self.current_wall_orientation, cell_size)

        # --- Legal moves
        """ painter.setBrush(QColor(0, 255, 0, 120))  # green
        painter.setPen(Qt.PenStyle.NoPen)
        for move in self.legal_moves:
            x = move.col * cell_size
            y = move.row * cell_size
            painter.drawEllipse(int(x + cell_size/4), int(y + cell_size/4),
                                int(cell_size/2), int(cell_size/2)) """

        # draw pawns
        if self.game_state:
            # Draw player one (red)
            r = self.game_state.player_one.x
            c = self.game_state.player_one.y
            painter.setBrush(QColor("red"))
            painter.setPen(Qt.GlobalColor.black)
            x = r * cell_size + cell_size / 2
            y = c * cell_size + cell_size / 2
            radius = cell_size / 2 - 5
            painter.drawEllipse(int(x - radius), int(y - radius), int(radius * 2), int(radius * 2))
            
            # Draw player two (blue)
            r = self.game_state.player_two.x
            c = self.game_state.player_two.y
            painter.setBrush(QColor("blue"))
            painter.setPen(Qt.GlobalColor.black)
            x = r * cell_size + cell_size / 2
            y = c * cell_size + cell_size / 2
            radius = cell_size / 2 - 5
            painter.drawEllipse(int(x - radius), int(y - radius), int(radius * 2), int(radius * 2))

        # draw vertical walls
        painter.setBrush(QColor("brown"))
        painter.setPen(Qt.GlobalColor.black)

        for r in range(len(self.game_state.vertical_edges)):
            for c in range(len(self.game_state.vertical_edges[r])):
                if self.game_state.vertical_edges[r][c]:
                    wall_thickness = int(cell_size / 5)
                    x = (c+1) * cell_size - wall_thickness // 2
                    y = r * cell_size
                    painter.drawRect(int(x), int(y), wall_thickness, int(cell_size))

        for r in range(len(self.game_state.horizontal_edges)):
            for c in range(len(self.game_state.horizontal_edges[r])):
                if self.game_state.horizontal_edges[r][c]:
                    wall_thickness = int(cell_size / 5)
                    x = c * cell_size
                    y = (r+1) * cell_size - wall_thickness // 2
                    painter.drawRect(int(x), int(y), int(cell_size), wall_thickness)

        if self.controller and self.controller.check_winner() is not None:
            winner = self.controller.check_winner()
            color = "Red" if winner == GameState.Player.PLAYER_ONE else "Blue"
            self.show_message(f"{color} wins!", 3000)
                    
                    
        """ wall_thickness = int(cell_size / 5)
        for wall in self.walls:
            r, c, orientation = wall["row"], wall["col"], wall["orientation"]
            painter.setBrush(QColor("brown"))
            painter.setPen(Qt.GlobalColor.black)
            if orientation == "H":
                # horizontal wall sits below the row 'r'
                x = c * cell_size
                y = (r + 1) * cell_size - wall_thickness // 2
                painter.drawRect(int(x), int(y), int(cell_size * 2), wall_thickness)
            elif orientation == "V":
                # vertical wall sits to the right of column 'c'
                x = (c + 1) * cell_size - wall_thickness // 2
                y = r * cell_size
                painter.drawRect(int(x), int(y), wall_thickness, int(cell_size * 2)) """

    def mousePressEvent(self, a0):
        pass
        
        if not hasattr(self, "controller") or self.controller is None:
            return
        
        x = a0.position().x()
        y = a0.position().y()

        cell_size = min(self.width(), self.height()) / BOARD_SIZE
        row = int(x // cell_size)
        col = int(y // cell_size)

        if a0.button() == Qt.MouseButton.LeftButton:
            pawn_move = GameRules.PawnMove(GameRules.PawnMove.SystemType.ABSOLUTE, position=GameState.Position(row,col))
            self.controller.apply_move(pawn_move)

        elif a0.button() == Qt.MouseButton.RightButton:
            wall_move = GameRules.WallMove(
                wall=GameState.Wall.HORIZONTAL if self.current_wall_orientation == "H" else GameState.Wall.VERTICAL,
                position=GameState.Position(row, col)
            )
            self.controller.apply_move(wall_move)

        self.update()


    def show_message(self, text, duration=1000):
        """Show temporary overlay message for `duration` ms."""
        self.message_label.setText(text)

        # Resize and center over board
        self.message_label.resize(self.width() // 2, 50)
        self.message_label.move((self.width() - self.message_label.width()) // 2,
                                (self.height() - self.message_label.height()) // 2)
        self.message_label.show()

        # Hide after `duration` ms
        QTimer.singleShot(duration, self.message_label.hide)

    def mouseMoveEvent(self, a0):
        pass
        cell_size = min(self.width(), self.height()) / BOARD_SIZE  # same as paintEvent
        x = a0.position().x()
        y = a0.position().y()
        row = int(y // cell_size)
        col = int(x // cell_size)

        # Only allow hover inside the board
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            self.hovered_cell = (row, col)
        else:
            self.hovered_cell = None

        # Update cursor if hovering over a legal move
        if self.hovered_cell in [(m.row, m.col) for m in self.legal_moves]:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        self.update()
    
    # TODO: I will likely eliminate this.
    def keyPressEvent(self, a0):
        pass
        """ if not hasattr(self, "controller") or self.controller is None:
            return """

        # Change wall orientation
        if a0.key() == Qt.Key.Key_H:
            self.current_wall_orientation = "H"
            self.show_message("Wall orientation: Horizontal", 1000)
        elif a0.key() == Qt.Key.Key_V:
            self.current_wall_orientation = "V"
            self.show_message("Wall orientation: Vertical", 1000)
        """
        # WASD / arrow keys for pawn movement
        player = self.controller.game_state.players[self.controller.game_state.active_player]
        opponent = self.controller.game_state.get_opponent_position(player)
        legal_moves = self.controller.game_state.get_pawn_moves(player.position, opponent)
        move = None

        if event.key() in (Qt.Key.Key_W, Qt.Key.Key_Up):
            move = next((m for m in legal_moves if m.row == player.position.row-1 and m.col == player.position.col), None)
        elif event.key() in (Qt.Key.Key_S, Qt.Key.Key_Down):
            move = next((m for m in legal_moves if m.row == player.position.row+1 and m.col == player.position.col), None)
        elif event.key() in (Qt.Key.Key_A, Qt.Key.Key_Left):
            move = next((m for m in legal_moves if m.row == player.position.row and m.col == player.position.col-1), None)
        elif event.key() in (Qt.Key.Key_D, Qt.Key.Key_Right):
            move = next((m for m in legal_moves if m.row == player.position.row and m.col == player.position.col+1), None)

        if move:
            self.controller.game_state.apply_pawn_move(player, move)
            self.controller.update_gui()
            # Check winner
            winner = self.controller.game_state.check_winner()
            if winner:
                color = "Red" if winner.player_id == 0 else "Blue"
                self.show_message(f"{color} wins!", 3000)
                self.controller = None """
                


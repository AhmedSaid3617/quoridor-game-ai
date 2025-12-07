# controller/game_controller.py
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox
from models.coord import Coord
from models.wall import Wall
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ai.easy import easy_ai_move
from ai.medium import medium_ai_move
from ai.hard import hard_ai_move

class GameController:
    def __init__(self, board_widget, game_state, update_info_callback=None):
        self.board = board_widget
        self.game_state = game_state
        self.update_info_callback = update_info_callback
        self.update_gui()
        self.mode = None         # "Human" or "AI"
        self.ai_player_id = 1         # assume AI is player 1
        self.difficulty = None
        self.undo_stack = []
        self.redo_stack = []


    def ai_move_if_needed(self):
        active_player = self.game_state.active_player
        if self.mode == "AI" and active_player == self.ai_player_id:
            # Choose AI move based on difficulty
            if self.difficulty == "Easy":
                move = easy_ai_move(self.game_state)
            elif self.difficulty == "Medium":
                move = medium_ai_move(self.game_state)
            else:
                move = hard_ai_move(self.game_state)

            # Apply the AI move
            self.game_state.apply_pawn_move(self.game_state.players[self.ai_player_id], move)
            self.update_gui()

            # Check winner after AI move
            winner = self.game_state.check_winner()
            if winner:
                color = "Red" if winner.player_id == 0 else "Blue"
                self.board.show_message(f"{color} wins!", 3000)
                self.board.controller = None

    def update_gui(self):
        pawns = [
            {"row": p.position.row, "col": p.position.col,
            "color": QColor("red") if p.player_id == 0 else QColor("blue")}
            for p in self.game_state.players
        ]

        walls = []
        for r, c in self.game_state.board.horizontal_walls:
            walls.append({"row": r, "col": c, "orientation": "H"})
        for r, c in self.game_state.board.vertical_walls:
            walls.append({"row": r, "col": c, "orientation": "V"})

        self.board.set_pawns(pawns)
        self.board.set_walls(walls)

        if self.update_info_callback:
            self.update_info_callback()
        
        player = self.game_state.players[self.game_state.active_player]
        opponent = self.game_state.get_opponent_position(player)
        legal_moves = self.game_state.get_pawn_moves(player.position, opponent)
        self.board.set_legal_moves(legal_moves)

    def handle_click(self, row, col, button="left"):
        player = self.game_state.players[self.game_state.active_player]

        self.undo_stack.append(self.game_state.copy())
        self.redo_stack.clear()
        if button == "left":  # Pawn move
            dest = Coord(row, col)
            legal_moves = self.game_state.get_pawn_moves(
                player.position,
                self.game_state.get_opponent_position(player)
            )

            if dest not in legal_moves:
                self.board.show_message("Illegal Move!", 1000)
                return

            self.game_state.apply_pawn_move(player, dest)
            self.update_gui()

            # Check winner
            winner = self.game_state.check_winner()
            if winner:
                color = "Red" if winner.player_id == 0 else "Blue"
                self.board.show_message(f"{color} wins!", 3000)
                self.board.controller = None
                return

        elif button == "right":  # wall placement
            # Read the orientation from the BoardWidget
            orientation = self.board.current_wall_orientation  # "h" or "v"

            # Make sure we don't place a horizontal wall at the far-right or vertical at the bottom
            if orientation == "H" and col >= self.game_state.board.size - 1:
                col = self.game_state.board.size - 2
            elif orientation == "V" and row >= self.game_state.board.size - 1:
                row = self.game_state.board.size - 2

            wall = Wall(row, col, orientation)
            try:
                self.game_state.apply_wall_move(player, wall)
                self.update_gui()
            except Exception as e:
                self.board.show_message(str(e), 1000)

        self.ai_move_if_needed()
        
    def undo(self):
        if not self.undo_stack:
            self.board.show_message("Nothing to undo", 1000)
            return
        # Save current state for redo
        self.redo_stack.append(self.game_state.copy())
        # Pop previous state
        self.game_state = self.undo_stack.pop()
        self.update_gui()

    def redo(self):
        if not self.redo_stack:
            self.board.show_message("Nothing to redo", 1000)
            return
        # Save current state for undo
        self.undo_stack.append(self.game_state.copy())
        # Pop from redo stack
        self.game_state = self.redo_stack.pop()
        self.update_gui()

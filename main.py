from PyQt6.QtWidgets import QApplication
from src.gui.game_window import GameWindow
from src.state.game_state import GameState

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    game_board_state = GameState()  # Initialize your GameState here
    window = GameWindow()
    window.show()
    
    if window.board.executor:
        window.board.executor.shutdown()

    sys.exit(app.exec())

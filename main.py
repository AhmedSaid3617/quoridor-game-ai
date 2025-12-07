from PyQt6.QtWidgets import QApplication
from gui.game_window import GameWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())

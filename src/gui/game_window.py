from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QFrame, QSizePolicy
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from src.gui.board_view import BoardWidget
from controller.game_controller import GameController
from src.state.game_state import GameState

# TODO: Remove this function and use actual game initialization in production
def game_state_init_test(game_state):
    """Initialize the game state for testing purposes."""

    game_state.place_wall(GameState.Wall.HORIZONTAL, GameState.Position(0,0))
    game_state.place_wall(GameState.Wall.HORIZONTAL, GameState.Position(2, 3))
    

    game_state.place_wall(GameState.Wall.HORIZONTAL, GameState.Position(5, 5))
   
    game_state.place_wall(GameState.Wall.HORIZONTAL, GameState.Position(3, 5))

    
    """ expected_horizontal_edges = np.array([
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]).astype(bool).tolist() """


    game_state.place_wall(GameState.Wall.VERTICAL, GameState.Position(2, 3))


    game_state.place_wall(GameState.Wall.VERTICAL, GameState.Position(4, 4))


    game_state.place_wall(GameState.Wall.VERTICAL, GameState.Position(2, 0))


    game_state.place_wall(GameState.Wall.VERTICAL, GameState.Position(4, 2))

    """
        expected_vertical_edges = np.array([
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()
    """


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quoridor")
        self.setMinimumSize(800, 600)

        # ---------- Info panel ----------
        self.info_label = QLabel()
        self.info_label.setStyleSheet("font-size: 16px;")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ---------- Board view ----------
        self.board = BoardWidget(parent=None)

        # ---------- Control pane ----------
        self.control_frame = QFrame()
        self.control_frame.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border: 2px solid #888;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QComboBox {
                padding: 5px;
                font-size: 14px;
                margin-top: 10px;
            }
        """)
        control_layout = QVBoxLayout()
        control_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Buttons
        self.reset_button = QPushButton("Play Again / Reset")
        self.reset_button.clicked.connect(self.reset_game)
        self.human_button = QPushButton("Human Mode")
        self.human_button.clicked.connect(self.set_human_mode)
        self.ai_button = QPushButton("AI Mode")
        self.ai_player_id=1
        self.ai_button.clicked.connect(self.set_ai_mode)
        self.undo_button = QPushButton("Undo")
        #self.undo_button.clicked.connect(lambda: self.controller.undo())

        self.redo_button = QPushButton("Redo")
        #self.redo_button.clicked.connect(lambda: self.controller.redo())

        self.ai_difficulty = QComboBox()
        self.ai_difficulty.addItems(["Easy", "Medium", "Hard"])

        control_layout.addWidget(self.reset_button)
        control_layout.addWidget(self.human_button)
        control_layout.addWidget(self.ai_button)
        control_layout.addWidget(self.undo_button)
        control_layout.addWidget(self.redo_button)
        control_layout.addWidget(self.ai_difficulty)
        self.control_frame.setLayout(control_layout)
        self.control_frame.setFixedWidth(180)

        # ---------- Main layout ----------
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.info_label)
        left_layout.addWidget(self.board)
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.control_frame)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # ---------- Game state ----------
        self.game_started = False
        self.mode = None      # "Human" or "AI"
        self.difficulty = None  # Only relevant if AI mode

        self.controller = None

        self.update_info()  # initial info display
        

    def start_game(self):
        """Initialize game with selected mode and difficulty."""
        self.game_state = GameState()

        game_state_init_test(self.game_state)

        """ self.controller = GameController(self.board, self.game_state, self.update_info)
        self.controller.mode = self.mode
        self.controller.ai_player_id=self.ai_player_id
        self.controller.difficulty = self.difficulty
        self.board.controller = self.controller """
        #self.game_started = True

        # Update the board view with the new game state
        self.board.set_game_state(self.game_state)
        
        # TODO: likely need to remove this
        self.board.update()

        self.update_info()


    def update_info(self):
        """Update the info label with turn, walls, mode, and AI difficulty."""
        if self.game_started and self.game_state and self.controller:
            # Game is running
            active_color = "Red" if self.game_state.active_player == 1 else "Blue"
            mode_text = f"Mode: {self.mode}"
            if self.mode == "AI":
                mode_text += f" ({self.difficulty})"

            info_text = (
                f"Turn: {active_color} | "
                f"Red walls: {self.game_state.player_one_remaining_walls} | "
                f"Blue walls: {self.game_state.player_two_remaining_walls} | "
                f"{mode_text}"
            )
        else:
            # Game not started
            info_text = "Game not started | Select Human or AI mode"

        self.info_label.setText(info_text)

    # ---------- Button actions ----------
    def reset_game(self):
        self.game_started = False
        self.mode = None
        self.difficulty = None
        self.game_state = None
        self.controller = None
        #self.board.controller = None
        self.update_info()

    def set_human_mode(self):
        self.mode = "Human"
        self.difficulty = None
        self.start_game()

    def set_ai_mode(self):
        self.mode = "AI"
        self.difficulty = self.ai_difficulty.currentText()
        self.start_game()
    


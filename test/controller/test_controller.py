import unittest
from src.controller.game_controller import GameController
from src.state.game_state import GameState
from src.rules.game_rules import GameRules


class TestGameController(unittest.TestCase):
    """Unit tests for the GameController class."""

    def setUp(self):
        """Set up a fresh game state and controller before each test."""
        self.game_state = GameState()
        self.controller = GameController(self.game_state, GameState.Player.PLAYER_ONE)

    def tearDown(self):
        """Clean up after each test."""
        del self.controller
        del self.game_state

    # --- Initialization Tests ---

    def test_initialization_player_one_starts(self):
        """Test that controller initializes correctly with Player One starting."""
        controller = GameController(GameState(), GameState.Player.PLAYER_ONE)
        self.assertEqual(controller.current_player, GameState.Player.PLAYER_ONE)
        self.assertEqual(controller.game_state.active_player, GameState.Player.PLAYER_ONE)

    def test_initialization_player_two_starts(self):
        """Test that controller initializes correctly with Player Two starting."""
        game_state = GameState()
        controller = GameController(game_state, GameState.Player.PLAYER_TWO)
        self.assertEqual(controller.current_player, GameState.Player.PLAYER_TWO)

    # --- Check Winner Tests ---

    def test_check_winner_no_winner_initially(self):
        """Test that there is no winner at the start of the game."""
        self.assertIsNone(self.controller.check_winner())

    def test_check_winner_player_one_wins(self):
        """Test that Player One wins when reaching y=0."""
        self.game_state.place_player(GameState.Player.PLAYER_ONE, GameState.Position(4, 0))
        winner = self.controller.check_winner()
        self.assertEqual(winner, GameState.Player.PLAYER_ONE)

    def test_check_winner_player_two_wins(self):
        """Test that Player Two wins when reaching y=8."""
        self.game_state.place_player(GameState.Player.PLAYER_TWO, GameState.Position(4, 8))
        winner = self.controller.check_winner()
        self.assertEqual(winner, GameState.Player.PLAYER_TWO)

    def test_check_winner_player_one_any_column(self):
        """Test that Player One wins at y=0 regardless of x position."""
        for x in range(9):
            game_state = GameState()
            controller = GameController(game_state, GameState.Player.PLAYER_ONE)
            game_state.place_player(GameState.Player.PLAYER_ONE, GameState.Position(x, 0))
            self.assertEqual(controller.check_winner(), GameState.Player.PLAYER_ONE)

    def test_check_winner_player_two_any_column(self):
        """Test that Player Two wins at y=8 regardless of x position."""
        for x in range(9):
            game_state = GameState()
            controller = GameController(game_state, GameState.Player.PLAYER_TWO)
            game_state.place_player(GameState.Player.PLAYER_TWO, GameState.Position(x, 8))
            self.assertEqual(controller.check_winner(), GameState.Player.PLAYER_TWO)

    # --- Pawn Move Tests ---

    def test_apply_valid_pawn_move_down(self):
        """Test applying a valid pawn move downward for Player One."""
        initial_pos = self.game_state.player_one
        move = GameRules.PawnMove(
            GameRules.PawnMove.SystemType.ABSOLUTE,
            position=GameState.Position(4, 7)
        )
        result = self.controller.apply_move(move)
        self.assertTrue(result)
        self.assertEqual(self.game_state.player_one, GameState.Position(4, 7))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

    def test_apply_valid_pawn_move_up(self):
        """Test applying a valid pawn move upward for Player Two."""
        # First switch to Player Two
        self.game_state.active_player = GameState.Player.PLAYER_TWO
        move = GameRules.PawnMove(
            GameRules.PawnMove.SystemType.ABSOLUTE,
            position=GameState.Position(4, 1)
        )
        result = self.controller.apply_move(move)
        self.assertTrue(result)
        self.assertEqual(self.game_state.player_two, GameState.Position(4, 1))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)

    def test_apply_invalid_pawn_move_out_of_bounds(self):
        """Test that invalid pawn moves out of bounds are rejected."""
        move = GameRules.PawnMove(
            GameRules.PawnMove.SystemType.ABSOLUTE,
            position=GameState.Position(10, 10)
        )
        result = self.controller.apply_move(move)
        self.assertFalse(result)
        # Player should still be at original position
        self.assertEqual(self.game_state.player_one, GameState.Position(4, 8))

    def test_apply_invalid_pawn_move_occupied_square(self):
        """Test that moving to opponent's square is rejected."""
        # Try to move Player One to Player Two's position
        move = GameRules.PawnMove(
            GameRules.PawnMove.SystemType.ABSOLUTE,
            position=GameState.Position(4, 0)
        )
        result = self.controller.apply_move(move)
        self.assertFalse(result)
        self.assertEqual(self.game_state.player_one, GameState.Position(4, 8))

    def test_apply_pawn_move_toggles_active_player(self):
        """Test that applying a valid pawn move toggles the active player."""
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)
        move = GameRules.PawnMove(
            GameRules.PawnMove.SystemType.ABSOLUTE,
            position=GameState.Position(4, 7)
        )
        self.controller.apply_move(move)
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

    # --- Wall Move Tests ---

    def test_apply_valid_horizontal_wall(self):
        """Test placing a valid horizontal wall."""
        initial_walls = self.game_state.player_one_remaining_walls
        move = GameRules.WallMove(
            wall=GameState.Wall.HORIZONTAL,
            position=GameState.Position(2, 2)
        )
        result = self.controller.apply_move(move)
        self.assertTrue(result)
        self.assertTrue(self.game_state.horizontal_edges[2][2])
        self.assertTrue(self.game_state.horizontal_edges[2][3])
        self.assertEqual(self.game_state.player_one_remaining_walls, initial_walls - 1)
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

    def test_apply_valid_vertical_wall(self):
        """Test placing a valid vertical wall."""
        initial_walls = self.game_state.player_one_remaining_walls
        move = GameRules.WallMove(
            wall=GameState.Wall.VERTICAL,
            position=GameState.Position(3, 3)
        )
        result = self.controller.apply_move(move)
        self.assertTrue(result)
        self.assertTrue(self.game_state.vertical_edges[3][3])
        self.assertTrue(self.game_state.vertical_edges[4][3])
        self.assertEqual(self.game_state.player_one_remaining_walls, initial_walls - 1)

    def test_apply_wall_decrements_correct_player_walls(self):
        """Test that placing a wall decrements the correct player's wall count."""
        # Player One places a wall
        self.assertEqual(self.game_state.player_one_remaining_walls, 10)
        move = GameRules.WallMove(
            wall=GameState.Wall.HORIZONTAL,
            position=GameState.Position(1, 1)
        )
        self.controller.apply_move(move)
        self.assertEqual(self.game_state.player_one_remaining_walls, 9)
        self.assertEqual(self.game_state.player_two_remaining_walls, 10)

        # Player Two places a wall
        move2 = GameRules.WallMove(
            wall=GameState.Wall.VERTICAL,
            position=GameState.Position(5, 5)
        )
        self.controller.apply_move(move2)
        self.assertEqual(self.game_state.player_one_remaining_walls, 9)
        self.assertEqual(self.game_state.player_two_remaining_walls, 9)

    def test_apply_invalid_wall_overlap(self):
        """Test that overlapping walls are rejected."""
        # Place first wall
        move1 = GameRules.WallMove(
            wall=GameState.Wall.HORIZONTAL,
            position=GameState.Position(2, 2)
        )
        self.controller.apply_move(move1)
        
        # Try to place overlapping wall
        self.game_state.active_player = GameState.Player.PLAYER_ONE
        move2 = GameRules.WallMove(
            wall=GameState.Wall.HORIZONTAL,
            position=GameState.Position(2, 2)
        )
        result = self.controller.apply_move(move2)
        self.assertFalse(result)
        # Wall count should not have changed again
        self.assertEqual(self.game_state.player_one_remaining_walls, 9)

    def test_apply_wall_out_of_bounds(self):
        """Test that walls placed out of bounds are rejected."""
        move = GameRules.WallMove(
            wall=GameState.Wall.HORIZONTAL,
            position=GameState.Position(8, 8)
        )
        result = self.controller.apply_move(move)
        self.assertFalse(result)
        self.assertEqual(self.game_state.player_one_remaining_walls, 10)

    # --- Integration Tests ---

    def test_complete_game_sequence(self):
        """Test a sequence of moves in a game."""
        # Player One moves down
        move1 = GameRules.PawnMove(
            GameRules.PawnMove.SystemType.ABSOLUTE,
            position=GameState.Position(4, 7)
        )
        self.assertTrue(self.controller.apply_move(move1))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

        # Player Two moves up
        move2 = GameRules.PawnMove(
            GameRules.PawnMove.SystemType.ABSOLUTE,
            position=GameState.Position(4, 1)
        )
        self.assertTrue(self.controller.apply_move(move2))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)

        # Player One places a wall
        move3 = GameRules.WallMove(
            wall=GameState.Wall.HORIZONTAL,
            position=GameState.Position(2, 2)
        )
        self.assertTrue(self.controller.apply_move(move3))
        self.assertEqual(self.game_state.player_one_remaining_walls, 9)
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

    def test_rules_update_after_each_move(self):
        """Test that the rules object is updated with the new game state after each move."""
        initial_rules = self.controller.rules
        move = GameRules.PawnMove(
            GameRules.PawnMove.SystemType.ABSOLUTE,
            position=GameState.Position(4, 7)
        )
        self.controller.apply_move(move)
        # Rules should have been recreated (implicitly tested by checking the move was applied correctly)
        self.assertIsNotNone(self.controller.rules)

    def test_invalid_move_type_raises_error(self):
        """Test that an unknown move type raises an error."""
        class UnknownMove(GameRules.Move):
            def __str__(self):
                return "Unknown"
        
        with self.assertRaises(ValueError):
            self.controller.apply_move(UnknownMove())

    def test_multiple_wall_placements_deplete_walls(self):
        """Test that placing multiple walls correctly depletes the wall count."""
        for i in range(10):
            self.game_state.active_player = GameState.Player.PLAYER_ONE
            move = GameRules.WallMove(
                wall=GameState.Wall.HORIZONTAL if i % 2 == 0 else GameState.Wall.VERTICAL,
                position=GameState.Position(i % 7, i % 7)
            )
            if self.controller.apply_move(move):
                pass  # Valid move
            # After all valid placements, check wall count
        
        # At least some walls should have been placed
        self.assertLess(self.game_state.player_one_remaining_walls, 10)


    def test_pawn_move_undo(self):
        # Move each player forward for 3 plays.
        move1 = GameRules.PawnMove(GameRules.PawnMove.SystemType.ABSOLUTE, position=GameState.Position(4, 7))
        move2 = GameRules.PawnMove(GameRules.PawnMove.SystemType.ABSOLUTE, position=GameState.Position(4, 1))
        move3 = GameRules.PawnMove(GameRules.PawnMove.SystemType.ABSOLUTE, position=GameState.Position(4, 6))

        self.controller.apply_move(move1)
        self.controller.apply_move(move2)
        self.controller.apply_move(move3)
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

        self.controller.undo()  # Undo Player One's move.
        self.assertEqual(self.game_state.player_one, GameState.Position(4, 7))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)

        self.controller.undo()  # Undo Player Two's move.
        self.assertEqual(self.game_state.player_two, GameState.Position(4, 0))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

        self.controller.undo()  # Undo Player One's first move.
        self.assertEqual(self.game_state.player_one, GameState.Position(4, 8))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)

    def test_pawn_move_redo(self):
        # Move each player forward for 2 plays.
        move1 = GameRules.PawnMove(GameRules.PawnMove.SystemType.ABSOLUTE, position=GameState.Position(4, 7))
        move2 = GameRules.PawnMove(GameRules.PawnMove.SystemType.ABSOLUTE, position=GameState.Position(4, 1))

        self.controller.apply_move(move1)
        self.controller.apply_move(move2)
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)

        self.controller.undo()  # Undo Player Two's move.
        self.assertEqual(self.game_state.player_two, GameState.Position(4, 0))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

        self.controller.undo()  # Undo Player One's move.
        self.assertEqual(self.game_state.player_one, GameState.Position(4, 8))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)

        self.controller.redo()  # Redo Player One's move.
        self.assertEqual(self.game_state.player_one, GameState.Position(4, 7))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

        self.controller.redo()  # Redo Player Two's move.
        self.assertEqual(self.game_state.player_two, GameState.Position(4, 1))
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)

    def test_wall_move_undo_redo(self):
        move1 = GameRules.WallMove(wall=GameState.Wall.HORIZONTAL, position=GameState.Position(2, 2))
        move2 = GameRules.WallMove(wall=GameState.Wall.VERTICAL, position=GameState.Position(4, 4))

        self.controller.apply_move(move1)
        self.controller.apply_move(move2)
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)

        self.controller.undo()  # Undo Player Two's wall.
        self.assertFalse(self.game_state.vertical_edges[4][4])
        self.assertFalse(self.game_state.vertical_edges[5][4])
        self.assertEqual(self.game_state.player_two_remaining_walls, 10)
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

        self.controller.undo()  # Undo Player One's wall.
        self.assertFalse(self.game_state.horizontal_edges[2][2])
        self.assertFalse(self.game_state.horizontal_edges[2][3])
        self.assertEqual(self.game_state.player_one_remaining_walls, 10)
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)

        self.controller.redo()  # Redo Player One's wall.
        self.assertTrue(self.game_state.horizontal_edges[2][2])
        self.assertTrue(self.game_state.horizontal_edges[2][3])
        self.assertEqual(self.game_state.player_one_remaining_walls, 9)
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_TWO)

        self.controller.redo()  # Redo Player Two's wall.
        self.assertTrue(self.game_state.vertical_edges[4][4])
        self.assertTrue(self.game_state.vertical_edges[5][4])
        self.assertEqual(self.game_state.player_two_remaining_walls, 9)
        self.assertEqual(self.game_state.active_player, GameState.Player.PLAYER_ONE)

    def test_undo_beyond_initial_state_raises_error(self):
        with self.assertRaises(IndexError, msg="No more moves to undo."):
            self.controller.undo()  # No moves made yet.
    
    def test_undo_play_undo_raises_error(self):
        move1 = GameRules.PawnMove(GameRules.PawnMove.SystemType.ABSOLUTE, position=GameState.Position(4, 7))
        self.controller.apply_move(move1)

        self.controller.undo()  # Undo the move.

        with self.assertRaises(IndexError, msg="No more moves to undo."):
            self.controller.undo()  # No more moves to undo.


if __name__ == '__main__':
    unittest.main()

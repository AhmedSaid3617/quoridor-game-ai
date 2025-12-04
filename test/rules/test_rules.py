from src.state import GameState
from src.rules import GameRules
import unittest
import numpy as np


class TestRulesOperations(unittest.TestCase):
    # Setup Method (Runs before *every* test method)
    def setUp(self):
        self.rules = GameRules()

    # Teardown Method (Runs after *every* test method)
    def tearDown(self):
        del self.rules

    # --- Test Methods (Must start with 'test_') ---

    def test_initial_position(self):
        self.assertEqual(self.rules.game_state.player_one, GameState.Position(4, 8))
        self.assertEqual(self.rules.game_state.player_two, GameState.Position(4, 0))

    def test_move_blocked_by_wall(self):
        horizontal_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()

        vertical_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()

        self.rules.game_state.vertical_edges = vertical_edges
        self.rules.game_state.horizontal_edges = horizontal_edges
        
        self.assertTrue(self.rules.can_move_up(GameState.Position(4, 4)))
        self.assertTrue(self.rules.can_move_right(GameState.Position(4, 4)))
        self.assertTrue(self.rules.can_move_down(GameState.Position(4, 4)))
        self.assertTrue(self.rules.can_move_left(GameState.Position(4, 4)))

        self.assertFalse(self.rules.can_move_up(GameState.Position(0, 0)))
        self.assertTrue(self.rules.can_move_down(GameState.Position(0, 0)))
        self.assertTrue(self.rules.can_move_right(GameState.Position(0, 0)))
        self.assertFalse(self.rules.can_move_left(GameState.Position(0, 0)))

        self.assertTrue(self.rules.can_move_up(GameState.Position(8, 8)))
        self.assertFalse(self.rules.can_move_down(GameState.Position(8, 8)))
        self.assertFalse(self.rules.can_move_right(GameState.Position(8, 8)))
        self.assertTrue(self.rules.can_move_left(GameState.Position(8, 8)))

        # Place walls around (4,4)

        horizontal_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()

        vertical_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()

        self.rules.game_state.vertical_edges = vertical_edges
        self.rules.game_state.horizontal_edges = horizontal_edges

        self.assertFalse(self.rules.can_move_up(GameState.Position(4, 4)))
        self.assertFalse(self.rules.can_move_right(GameState.Position(4, 4)))
        self.assertTrue(self.rules.can_move_down(GameState.Position(4, 4)))
        self.assertTrue(self.rules.can_move_left(GameState.Position(4, 4)))

        self.assertFalse(self.rules.can_move_up(GameState.Position(3, 4)))
        self.assertTrue(self.rules.can_move_right(GameState.Position(3, 4)))
        self.assertTrue(self.rules.can_move_down(GameState.Position(3, 4)))
        self.assertFalse(self.rules.can_move_left(GameState.Position(3, 4)))

        self.assertTrue(self.rules.can_move_up(GameState.Position(3, 5)))
        self.assertTrue(self.rules.can_move_right(GameState.Position(3, 5)))
        self.assertFalse(self.rules.can_move_down(GameState.Position(3, 5)))
        self.assertFalse(self.rules.can_move_left(GameState.Position(3, 5)))

        self.assertTrue(self.rules.can_move_up(GameState.Position(4, 5)))
        self.assertFalse(self.rules.can_move_right(GameState.Position(4, 5)))
        self.assertFalse(self.rules.can_move_down(GameState.Position(4, 5)))
        self.assertTrue(self.rules.can_move_left(GameState.Position(4, 5)))
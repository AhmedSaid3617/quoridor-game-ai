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
        
        self.assertTrue(self.rules._can_move_up(GameState.Position(4, 4)))
        self.assertTrue(self.rules._can_move_right(GameState.Position(4, 4)))
        self.assertTrue(self.rules._can_move_down(GameState.Position(4, 4)))
        self.assertTrue(self.rules._can_move_left(GameState.Position(4, 4)))

        self.assertFalse(self.rules._can_move_up(GameState.Position(0, 0)))
        self.assertTrue(self.rules._can_move_down(GameState.Position(0, 0)))
        self.assertTrue(self.rules._can_move_right(GameState.Position(0, 0)))
        self.assertFalse(self.rules._can_move_left(GameState.Position(0, 0)))

        self.assertTrue(self.rules._can_move_up(GameState.Position(8, 8)))
        self.assertFalse(self.rules._can_move_down(GameState.Position(8, 8)))
        self.assertFalse(self.rules._can_move_right(GameState.Position(8, 8)))
        self.assertTrue(self.rules._can_move_left(GameState.Position(8, 8)))

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

        self.assertFalse(self.rules._can_move_up(GameState.Position(4, 4)))
        self.assertFalse(self.rules._can_move_right(GameState.Position(4, 4)))
        self.assertTrue(self.rules._can_move_down(GameState.Position(4, 4)))
        self.assertTrue(self.rules._can_move_left(GameState.Position(4, 4)))

        self.assertFalse(self.rules._can_move_up(GameState.Position(3, 4)))
        self.assertTrue(self.rules._can_move_right(GameState.Position(3, 4)))
        self.assertTrue(self.rules._can_move_down(GameState.Position(3, 4)))
        self.assertFalse(self.rules._can_move_left(GameState.Position(3, 4)))

        self.assertTrue(self.rules._can_move_up(GameState.Position(3, 5)))
        self.assertTrue(self.rules._can_move_right(GameState.Position(3, 5)))
        self.assertFalse(self.rules._can_move_down(GameState.Position(3, 5)))
        self.assertFalse(self.rules._can_move_left(GameState.Position(3, 5)))

        self.assertTrue(self.rules._can_move_up(GameState.Position(4, 5)))
        self.assertFalse(self.rules._can_move_right(GameState.Position(4, 5)))
        self.assertFalse(self.rules._can_move_down(GameState.Position(4, 5)))
        self.assertTrue(self.rules._can_move_left(GameState.Position(4, 5)))

    def test_can_move_up_all_cases(self):
        rules = self.rules
        gs = rules.game_state
        # Case 1: y == 0
        self.assertFalse(rules._can_move_up(GameState.Position(4, 0)), "Should not move up from y=0")
        # Case 2: Blocked by horizontal wall
        gs.horizontal_edges[3][4] = True
        self.assertFalse(rules._can_move_up(GameState.Position(4, 4)), "Should not move up if horizontal wall above")
        gs.horizontal_edges[3][4] = False
        # Case 3: Opponent directly above
        gs.player_one = GameState.Position(4, 4)
        gs.player_two = GameState.Position(4, 3)
        self.assertFalse(rules._can_move_up(GameState.Position(4, 4)), "Should not move up if opponent directly above")
        # Case 4: Nothing blocks
        gs.player_one = GameState.Position(4, 4)
        gs.player_two = GameState.Position(0, 0)
        self.assertTrue(rules._can_move_up(GameState.Position(4, 4)), "Should move up if nothing blocks")
        # Case 5: Not a player position
        self.assertTrue(rules._can_move_up(GameState.Position(2, 2)), "Should move up from generic position if nothing blocks")
        # Reset for other tests
        gs.player_one = GameState.Position(4, 8)
        gs.player_two = GameState.Position(4, 0)

    def test_can_move_right_all_cases(self):
        rules = self.rules
        gs = rules.game_state
        # Case 1: x == 8 (edge of board)
        self.assertFalse(rules._can_move_right(GameState.Position(8, 4)), "Should not move right from x=8")
        # Case 2: Blocked by vertical wall
        gs.vertical_edges[4][4] = True
        self.assertFalse(rules._can_move_right(GameState.Position(4, 4)), "Should not move right if vertical wall blocks")
        gs.vertical_edges[4][4] = False
        # Case 3: Opponent directly right
        gs.player_one = GameState.Position(4, 4)
        gs.player_two = GameState.Position(5, 4)
        self.assertFalse(rules._can_move_right(GameState.Position(4, 4)), "Should not move right if opponent directly right")
        # Case 4: Nothing blocks
        gs.player_one = GameState.Position(4, 4)
        gs.player_two = GameState.Position(0, 0)
        self.assertTrue(rules._can_move_right(GameState.Position(4, 4)), "Should move right if nothing blocks")
        # Case 5: Not a player position
        self.assertTrue(rules._can_move_right(GameState.Position(2, 2)), "Should move right from generic position if nothing blocks")
        # Reset for other tests
        gs.player_one = GameState.Position(4, 8)
        gs.player_two = GameState.Position(4, 0)

    def test_can_move_left_all_cases(self):
        rules = self.rules
        gs = rules.game_state
        # Case 1: x == 0 (edge of board)
        self.assertFalse(rules._can_move_left(GameState.Position(0, 4)), "Should not move left from x=0")
        # Case 2: Blocked by vertical wall
        gs.vertical_edges[4][3] = True
        self.assertFalse(rules._can_move_left(GameState.Position(4, 4)), "Should not move left if vertical wall blocks")
        gs.vertical_edges[4][3] = False
        # Case 3: Opponent directly left
        gs.player_one = GameState.Position(4, 4)
        gs.player_two = GameState.Position(3, 4)
        self.assertFalse(rules._can_move_left(GameState.Position(4, 4)), "Should not move left if opponent directly left")
        # Case 4: Nothing blocks
        gs.player_one = GameState.Position(4, 4)
        gs.player_two = GameState.Position(0, 0)
        self.assertTrue(rules._can_move_left(GameState.Position(4, 4)), "Should move left if nothing blocks")
        # Case 5: Not a player position
        self.assertTrue(rules._can_move_left(GameState.Position(2, 2)), "Should move left from generic position if nothing blocks")
        # Reset for other tests
        gs.player_one = GameState.Position(4, 8)
        gs.player_two = GameState.Position(4, 0)

    def test_can_move_down_all_cases(self):
        rules = self.rules
        gs = rules.game_state
        # Case 1: y == 8 (edge of board)
        self.assertFalse(rules._can_move_down(GameState.Position(4, 8)), "Should not move down from y=8")
        # Case 2: Blocked by horizontal wall
        gs.horizontal_edges[4][4] = True
        self.assertFalse(rules._can_move_down(GameState.Position(4, 4)), "Should not move down if horizontal wall blocks")
        gs.horizontal_edges[4][4] = False
        # Case 3: Opponent directly below
        gs.player_one = GameState.Position(4, 4)
        gs.player_two = GameState.Position(4, 5)
        self.assertFalse(rules._can_move_down(GameState.Position(4, 4)), "Should not move down if opponent directly below")
        # Case 4: Nothing blocks
        gs.player_one = GameState.Position(4, 4)
        gs.player_two = GameState.Position(0, 0)
        self.assertTrue(rules._can_move_down(GameState.Position(4, 4)), "Should move down if nothing blocks")
        # Case 5: Not a player position
        self.assertTrue(rules._can_move_down(GameState.Position(2, 2)), "Should move down from generic position if nothing blocks")
        # Reset for other tests
        gs.player_one = GameState.Position(4, 8)
        gs.player_two = GameState.Position(4, 0)
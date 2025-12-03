from src.state import GameState
import unittest
import numpy as np


class TestStateOperations(unittest.TestCase):
    # Setup Method (Runs before *every* test method)
    def setUp(self):
        self.state = GameState()

    # Teardown Method (Runs after *every* test method)
    def tearDown(self):
        del self.state

    # --- Test Methods (Must start with 'test_') ---

    def test_initial_position(self):
        self.assertEqual(self.state.player_one, GameState.Position(4, 8))
        self.assertEqual(self.state.player_two, GameState.Position(4, 0))

    def test_placing_players(self):
        for i in range(9):
            for j in range(9):
                position = GameState.Position(i, j)

                if position == self.state.player_two:
                    self.assertRaises(ValueError, self.state.place_player, GameState.Player.PLAYER_ONE, position)
                    continue

                self.state.place_player(GameState.Player.PLAYER_ONE, position)
                self.assertEqual(self.state.player_one, position)

        for i in range(9):
            for j in range(9):
                position = GameState.Position(i, j)

                if position == self.state.player_one:
                    self.assertRaises(ValueError, self.state.place_player, GameState.Player.PLAYER_TWO, position)
                    continue

                self.state.place_player(GameState.Player.PLAYER_TWO, position)
                self.assertEqual(self.state.player_two, position)

    def test_placing_players_out_of_bounds(self):
        out_of_bounds_positions = [
            GameState.Position(-1, 0),
            GameState.Position(0, -1),
            GameState.Position(10, 0),
            GameState.Position(9, 0),
            GameState.Position(0, 9),
            GameState.Position(0, 10),
        ]

        for position in out_of_bounds_positions:
            self.assertRaises(ValueError, self.state.place_player, GameState.Player.PLAYER_ONE, position)
            self.assertRaises(ValueError, self.state.place_player, GameState.Player.PLAYER_TWO, position)

    def test_placing_vertical_walls(self):
        expected_vertical_edges = np.array([
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
        self.assertEqual(self.state.vertical_edges, expected_vertical_edges)

        self.state.place_wall(GameState.Wall.VERTICAL, GameState.Position(2, 3))
        expected_vertical_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()
        self.assertEqual(self.state.vertical_edges, expected_vertical_edges)

        self.state.place_wall(GameState.Wall.VERTICAL, GameState.Position(4, 4))
        expected_vertical_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()
        self.assertEqual(self.state.vertical_edges, expected_vertical_edges)

        self.state.place_wall(GameState.Wall.VERTICAL, GameState.Position(2, 0))
        expected_vertical_edges = np.array([
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()
        self.assertEqual(self.state.vertical_edges, expected_vertical_edges)

        self.state.place_wall(GameState.Wall.VERTICAL, GameState.Position(4, 2))
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
        self.assertEqual(self.state.vertical_edges, expected_vertical_edges)

        self.assertRaises(ValueError, self.state.place_wall, GameState.Wall.VERTICAL, GameState.Position(2, 2))
        self.assertRaises(ValueError, self.state.place_wall, GameState.Wall.VERTICAL, GameState.Position(2, 3))

    def test_placing_horizontal_walls(self):
        expected_horizontal_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()
        self.assertEqual(self.state.horizontal_edges, expected_horizontal_edges)

        self.state.place_wall(GameState.Wall.HORIZONTAL, GameState.Position(2, 3))
        expected_horizontal_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()
        self.assertEqual(self.state.horizontal_edges, expected_horizontal_edges)

        self.state.place_wall(GameState.Wall.HORIZONTAL, GameState.Position(5, 5))
        expected_horizontal_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()
        self.assertEqual(self.state.horizontal_edges, expected_horizontal_edges)

        self.state.place_wall(GameState.Wall.HORIZONTAL, GameState.Position(3, 5))
        expected_horizontal_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()
        self.assertEqual(self.state.horizontal_edges, expected_horizontal_edges)

        self.assertRaises(ValueError, self.state.place_wall, GameState.Wall.HORIZONTAL, GameState.Position(3, 5))
        self.assertRaises(ValueError, self.state.place_wall, GameState.Wall.HORIZONTAL, GameState.Position(2, 5))

    def test_placing_walls_out_of_bounds(self):
        out_of_bounds_vertical_positions = [
            GameState.Position(-1, 0),
            GameState.Position(0, -1),
            GameState.Position(8, 0),
            GameState.Position(7, 8),
            GameState.Position(0, 8),
            GameState.Position(0, 9),
        ]

        for position in out_of_bounds_vertical_positions:
            self.assertRaises(ValueError, self.state.place_wall, GameState.Wall.VERTICAL, position)

        out_of_bounds_horizontal_positions = [
            GameState.Position(-1, 0),
            GameState.Position(0, -1),
            GameState.Position(8, 0),
            GameState.Position(7, 8),
            GameState.Position(0, 9),
            GameState.Position(0, 8),
        ]

        for position in out_of_bounds_horizontal_positions:
            self.assertRaises(ValueError, self.state.place_wall, GameState.Wall.HORIZONTAL, position)

    def test_str_representation(self):
        self.assertEqual(str(self.state.player_one), "(4, 8)")
        self.assertEqual(str(self.state.player_two), "(4, 0)")

    def test_position_equality(self):
        pos1 = GameState.Position(2, 3)
        pos2 = GameState.Position(2, 3)
        pos3 = GameState.Position(3, 2)

        self.assertEqual(pos1, pos2)
        self.assertNotEqual(pos1, pos3)

    def test_position_copy(self):
        pos1 = GameState.Position(5, 6)
        pos2 = pos1.__copy__()

        self.assertEqual(pos1, pos2)
        self.assertIsNot(pos1, pos2)
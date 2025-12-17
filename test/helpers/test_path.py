from src.helpers.path_solver import PathSolver
from src.state import GameState
import unittest
import numpy as np

class TestPath(unittest.TestCase):
    # Setup Method (Runs before *every* test method)
    def setUp(self):
        self.state = GameState()

    # Teardown Method (Runs after *every* test method)
    def tearDown(self):
        del self.state

    # --- Test Methods (Must start with 'test_') ---
    def test_path_solve_any_simple(self):
        start = GameState.Player.PLAYER_ONE
        state = self.state
        result = PathSolver.solve_any(start, 5, state)
        print (result)

    def test_path_solve_optimum_simple(self):
        start = GameState.Player.PLAYER_ONE
        state = self.state
        result = PathSolver.solve_optimum(start, 5, state)
        print (result)

    def test_path_solve_all_optimum_simple(self):
        start = GameState.Player.PLAYER_ONE
        state = self.state
        state.horizontal_edges = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 0],
        ]
        result = PathSolver.solve_all_optimum(start, 5, state)
        print (result)


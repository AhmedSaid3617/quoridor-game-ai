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

    def test_path_optimum_with_Player_two(self):
        start = GameState.Player.PLAYER_TWO
        state = self.state
        result = PathSolver.solve_optimum(start, 5, state)
        print(result)

    def test_path_optimum_with_Edges(self):
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
            [0, 0, 1, 1, 1, 1, 1, 1, 0],
        ]

        result = PathSolver.solve_optimum(start, 0, state)
        print(result)

        state.vertical_edges = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
        ]
        result = PathSolver.solve_optimum(start, 0, state)
        print(result)

    def test_surrounded_from_three_directions(self):
        start = GameState.Player.PLAYER_ONE
        state = self.state
        state.horizontal_edges = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        state.vertical_edges = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        state.player_one = GameState.Position(4, 6)
        result = PathSolver.solve_optimum(start, 0, state)
        print(result)


    #Error the path finding function ignores the other player

    def test_second_player_in_front_of_the_other(self):
        start = GameState.Player.PLAYER_ONE
        state = self.state
        state.player_two = GameState.Position(4, 5)
        state.player_one = GameState.Position(4, 6)
        result = PathSolver.solve_optimum(start, 0, state)
        print(result)
        start = GameState.Player.PLAYER_TWO
        state = self.state
        state.player_two = GameState.Position(4, 5)
        state.player_one = GameState.Position(4, 6)
        result = PathSolver.solve_optimum(start, 8, state)
        print(result)

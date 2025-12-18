from src.rules.game_rules import GameRules
from src.state import GameState
import unittest
import numpy as np
from src.helpers.wall_block_solver import WallBlockSolver

class TestWallBlockSolver(unittest.TestCase):
    # Setup Method (Runs before *every* test method)
    def setUp(self):
        self.state = GameState()

    # Teardown Method (Runs after *every* test method)
    def tearDown(self):
        del self.state

    # --- Test Methods (Must start with 'test_') ---
    def test_wall_block_solver_init(self):
        solver = WallBlockSolver(self.state, GameState.Player.PLAYER_ONE)
        self.assertIsInstance(solver, WallBlockSolver)

    def test_wall_block(self):
        solver = WallBlockSolver(self.state, GameState.Player.PLAYER_ONE)
        solution = solver.solve(GameState.Position(0,0), GameRules.PawnMove(GameRules.PawnMove.SystemType.RELATIVE, GameRules.PawnMove.MovementType.RIGHT))
        self.assertEqual(solution, [GameRules.WallMove(GameState.Wall.VERTICAL, GameState.Position(0,0))])


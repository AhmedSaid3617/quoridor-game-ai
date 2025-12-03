from src.state import GameState
import unittest

def test_initial_positions():
    state = GameState()
    assert state.player_one.x == 4
    assert state.player_one.y == 8
    assert state.player_two.x == 4
    assert state.player_two.y == 0

class TestStateOperations(unittest.TestCase):
    # Setup Method (Runs before *every* test method)
    def setUp(self):
        self.state = GameState()

    # Teardown Method (Runs after *every* test method)
    def tearDown(self):
        del self.state

    # --- Test Methods (Must start with 'test_') ---

    def test_position(self):
        self.assertEqual(self.state.player_one, GameState.Position(4, 8))
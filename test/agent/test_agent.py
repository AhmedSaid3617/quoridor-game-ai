from src.agent.agent import Agent
from src.agent.agent_leveled import Agent_leveled
from src.helpers.path_solver import PathSolver
from src.rules.game_rules import GameRules
from src.state import GameState
import unittest
import numpy as np

class TestAgent(unittest.TestCase):
    # Setup Method (Runs before *every* test method)
    def setUp(self):
        self.state = GameState()

    # Teardown Method (Runs after *every* test method)
    def tearDown(self):
        del self.state

    # --- Test Methods (Must start with 'test_') ---
    def test_create_instance_and_predicts_a_move(self):
        agent = Agent_leveled(difficulty=Agent.AgentDifficulty.HARD, state=self.state, player=GameState.Player.PLAYER_TWO)
        self.assertIsInstance(agent.decide_move(), GameRules.Move)
from abc import abstractmethod
from enum import Enum

from src.rules.game_rules import GameRules
from src.state.game_state import GameState


class Agent:
    class AgentDifficulty(Enum):
        EASY = "EASY"
        MEDIUM = "MEDIUM"
        HARD = "HARD"

    # player is the MAX agent
    def __init__(self, difficulty: AgentDifficulty, maximize: GameState.Player, state: GameState,player:GameState.Player):
        self.difficulty = difficulty
        self.maximize = maximize
        self.state = state
        self.player=player


    @abstractmethod
    def decide_move(self) -> 'GameRules.Move':
        raise NotImplementedError("Agent move decision not implemented yet")


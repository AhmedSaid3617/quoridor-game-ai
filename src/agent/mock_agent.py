from src.agent.agent import Agent
from src.rules.game_rules import GameRules
from src.state.game_state import GameState

class MockAgent(Agent):
    def decide_move(self) -> 'GameRules.Move':
        # Always return a dummy move (e.g., move pawn forward by one)
        current_position = self.state.player_one if self.maximize == GameState.Player.PLAYER_ONE else self.state.player_two
        new_position = GameState.Position(current_position.x, current_position.y + 1)
        move = GameRules.PawnMove(GameRules.PawnMove.SystemType.ABSOLUTE, position=new_position)
        return move

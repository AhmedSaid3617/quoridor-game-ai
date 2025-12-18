from src.agent.agent import Agent
from src.controller.game_controller import GameController
from src.helpers.path_solver import PathSolver
from src.helpers.wall_block_solver import WallBlockSolver
from src.rules.game_rules import GameRules
from src.state.game_state import GameState

class Agent_leveled(Agent):
    def heuristic(self, state: GameState) -> int:
        min_path_for_agent = PathSolver.solve_optimum(self.player, 8 if self.player == GameState.Player.PLAYER_ONE else 0, state)
        opponent = GameState.Player.PLAYER_ONE if self.player == GameState.Player.PLAYER_TWO else GameState.Player.PLAYER_TWO
        min_path_for_opponent = PathSolver.solve_optimum(opponent, 0 if self.player == GameState.Player.PLAYER_ONE else 8, state)
        len_agent = len(min_path_for_agent.path) if min_path_for_agent else 99
        len_opp = len(min_path_for_opponent.path) if min_path_for_opponent else 99

        return len_opp - len_agent
    def minimax(self, state: GameState, depth: int, alpha: int, beta: int) -> int:
        rules=GameRules(state)

        opponent =GameState.Player.PLAYER_TWO if self.player==GameState.Player.PLAYER_ONE else GameState.Player.PLAYER_ONE
        
        if depth == 0 or rules.check_winner():
            if rules.check_winner() == self.player:
                return 1000
            elif rules.check_winner() == opponent:
                return -1000
            else:
                return self.heuristic(state)
        
        if (not depth%2==0):
            wall_solver=WallBlockSolver(state,self.player)
            available_pawn_moves=rules.all_pawn_moves_absolute(self.player)
            available_walls_on_path= wall_solver.get_wall_moves_on_opponent_opt_paths()
            dfs=available_pawn_moves+available_walls_on_path
            best_value = -1000
            for move in dfs:
                temp_state = state.__copy__()
                game_controller=GameController(temp_state, self.player)
                if not game_controller.apply_move(move):
                    continue
                value = self.minimax(game_controller.game_state, depth - 1, alpha, beta)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else: 
            wall_solver=WallBlockSolver(state,opponent) 
            available_pawn_moves=rules.all_pawn_moves_absolute(opponent)
            available_walls_on_path= wall_solver.get_wall_moves_on_opponent_opt_paths()
            dfs=available_pawn_moves+available_walls_on_path
            worst_value = 10000
            for move in dfs:
                temp_state = state.__copy__()
                game_controller=GameController(temp_state, opponent)
                if not game_controller.apply_move(move):
                    continue
                value = self.minimax(game_controller.game_state, depth - 1, alpha, beta)
                worst_value = min(worst_value, value)
                beta = min(beta, worst_value)
                if beta <= alpha:
                    break
            return best_value

    def decide_move(self,current_level:int =1) -> 'GameRules.Move':
        rules=GameRules(self.state)
        depth = 5 if self.difficulty == Agent.AgentDifficulty.HARD else 3 if self.difficulty == Agent.AgentDifficulty.MEDIUM else 1
        
        alpha=-10000
        beta=10000
        move =None
        wall_solver=WallBlockSolver(self.state,self.player) 
        available_pawn_moves=rules.all_pawn_moves_absolute(self.player)
        available_walls_on_path= wall_solver.get_wall_moves_on_opponent_opt_paths()
        dfs=available_pawn_moves+available_walls_on_path
        best_move=None
        for move in dfs:
          temp_state = self.state.__copy__()
          game_controller = GameController(temp_state, self.player)
          
          if not game_controller.apply_move(move):
              continue
          v = self.minimax(temp_state, depth - 1, alpha, beta)
          if alpha < v:
              alpha = v
              best_move = move
                
        return best_move
    



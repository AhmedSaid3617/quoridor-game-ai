import copy
from src.agent.agent import Agent
from src.controller.game_controller import GameController
from src.helpers.path_solver import PathSolver
from src.helpers.wall_block_solver import WallBlockSolver
from src.rules.game_rules import GameRules
from src.state.game_state import GameState



class Agent_leveled(Agent):

    INFINITY = 1000000
    OPP_BIAS = 6
    PLAYER_BIAS = 8
    WALL_VALUE = 2

    # TODO: wall moves must be added to heuristic
    def heuristic(self, state: GameState) -> int:
        min_path_for_agent = PathSolver.solve_optimum(self.player, 0 if self.player == GameState.Player.PLAYER_ONE else 8, state)
        opponent = GameState.Player.PLAYER_ONE if self.player == GameState.Player.PLAYER_TWO else GameState.Player.PLAYER_TWO
        min_path_for_opponent = PathSolver.solve_optimum(opponent, 8 if self.player == GameState.Player.PLAYER_ONE else 0, state)
        len_agent = len(min_path_for_agent.path) if min_path_for_agent else self.INFINITY
        len_opp = len(min_path_for_opponent.path) if min_path_for_opponent else self.INFINITY
        remaining_walls = state.player_one_remaining_walls if self.player == GameState.Player.PLAYER_ONE else state.player_two_remaining_walls
        remaining_walls_opponent = state.player_one_remaining_walls if opponent == GameState.Player.PLAYER_ONE else state.player_two_remaining_walls

        return (len_opp*self.OPP_BIAS - len_agent*self.PLAYER_BIAS) + (remaining_walls - remaining_walls_opponent)*self.WALL_VALUE
    

    def minimax(self, state: GameState, depth: int, alpha: int, beta: int, maximizer:bool) -> int:

        opponent =GameState.Player.PLAYER_TWO if self.player==GameState.Player.PLAYER_ONE else GameState.Player.PLAYER_ONE
        
        controller = GameController(state)
        if depth == 0 or controller.check_winner():
            if controller.check_winner() == self.player:
                return self.INFINITY
            elif controller.check_winner() == opponent:
                return -self.INFINITY
            else:
                return self.heuristic(state)
        
        # MAX
        if (maximizer):
            rules=GameRules(state.get_biased_for_player(self.player))
            wall_solver=WallBlockSolver(state,opponent)
            available_pawn_moves=list(rules.all_pawn_moves_absolute(self.player))
            available_walls_on_path= wall_solver.get_wall_moves_on_best_path()

            min_path_for_agent = PathSolver.solve_optimum(self.player, 0 if self.player == GameState.Player.PLAYER_ONE else 8, state)
            opponent = GameState.Player.PLAYER_ONE if self.player == GameState.Player.PLAYER_TWO else GameState.Player.PLAYER_TWO
            min_path_for_opponent = PathSolver.solve_optimum(opponent, 8 if self.player == GameState.Player.PLAYER_ONE else 0, state)
            len_agent = len(min_path_for_agent.path) if min_path_for_agent else self.INFINITY
            len_opp = len(min_path_for_opponent.path) if min_path_for_opponent else self.INFINITY

            if len_agent < len_opp:
                dfs=available_pawn_moves+available_walls_on_path
            else:
                dfs=available_walls_on_path+available_pawn_moves

            #dfs=available_pawn_moves+available_walls_on_path
            best_value = -self.INFINITY
            for move in dfs:
                temp_state = copy.copy(state)
                temp_state.active_player = self.player
                game_controller=GameController(temp_state)
                if not game_controller.apply_move(move):
                    continue
                value = self.minimax(game_controller.game_state, depth - 1, alpha, beta, maximizer= not maximizer)
                best_value = max(best_value, value)
                
                if value >= beta:
                    break
                alpha = max(alpha, best_value)
            return best_value
        
        # MIN
        else: 
            rules=GameRules(state.get_biased_for_player(opponent))
            wall_solver=WallBlockSolver(state,self.player) 
            available_pawn_moves=list(rules.all_pawn_moves_absolute(opponent))
            available_walls_on_path= wall_solver.get_wall_moves_on_best_path()

            min_path_for_agent = PathSolver.solve_optimum(self.player, 0 if self.player == GameState.Player.PLAYER_ONE else 8, state)
            opponent = GameState.Player.PLAYER_ONE if self.player == GameState.Player.PLAYER_TWO else GameState.Player.PLAYER_TWO
            min_path_for_opponent = PathSolver.solve_optimum(opponent, 8 if self.player == GameState.Player.PLAYER_ONE else 0, state)
            len_agent = len(min_path_for_agent.path) if min_path_for_agent else self.INFINITY
            len_opp = len(min_path_for_opponent.path) if min_path_for_opponent else self.INFINITY

            if len_agent > len_opp:
                dfs=available_pawn_moves+available_walls_on_path
            else:
                dfs=available_walls_on_path+available_pawn_moves

            #dfs=available_pawn_moves+available_walls_on_path
            worst_value = self.INFINITY
            for move in dfs:
                temp_state = copy.copy(state)
                temp_state.active_player = opponent
                game_controller=GameController(temp_state)
                if not game_controller.apply_move(move):
                    continue
                value = self.minimax(game_controller.game_state, depth - 1, alpha, beta, maximizer=not maximizer)
                worst_value = min(worst_value, value)
                
                if value <= alpha:
                    break
                beta = min(beta, worst_value)
            return worst_value

    def decide_move(self,current_level:int =1) -> 'GameRules.Move':
        rules=GameRules(self.state.get_biased_for_player(self.player))
        depth = 3 if self.difficulty == Agent.AgentDifficulty.HARD else 2 if self.difficulty == Agent.AgentDifficulty.MEDIUM else 1
        opponent =GameState.Player.PLAYER_TWO if self.player==GameState.Player.PLAYER_ONE else GameState.Player.PLAYER_ONE
        alpha=-self.INFINITY
        beta=self.INFINITY
        move =None
        wall_solver=WallBlockSolver(self.state, opponent) 
        available_pawn_moves=list(rules.all_pawn_moves_absolute(self.player))
        available_walls_on_path= wall_solver.get_wall_moves_on_best_path()

        min_path_for_agent = PathSolver.solve_optimum(self.player, 0 if self.player == GameState.Player.PLAYER_ONE else 8, self.state)
        opponent = GameState.Player.PLAYER_ONE if self.player == GameState.Player.PLAYER_TWO else GameState.Player.PLAYER_TWO
        min_path_for_opponent = PathSolver.solve_optimum(opponent, 8 if self.player == GameState.Player.PLAYER_ONE else 0, self.state)
        len_agent = len(min_path_for_agent.path) if min_path_for_agent else self.INFINITY
        len_opp = len(min_path_for_opponent.path) if min_path_for_opponent else self.INFINITY

        if len_agent < len_opp:
            dfs=available_pawn_moves+available_walls_on_path
        else:
            dfs=available_walls_on_path+available_pawn_moves

        """
        best_value = -self.INFINITY
            for move in dfs:
                temp_state = copy.copy(state)
                temp_state.active_player = self.player
                game_controller=GameController(temp_state)
                if not game_controller.apply_move(move):
                    continue
                value = self.minimax(game_controller.game_state, depth - 1, alpha, beta, maximizer= not maximizer)
                best_value = max(best_value, value)
                
                if value >= beta:
                    break
                alpha = max(alpha, best_value)
            return best_value
        """

        best_move=dfs[0]
        best_value = -self.INFINITY
        for move in dfs:
            temp_state = copy.copy(self.state)
            temp_state.active_player = self.player
            game_controller = GameController(temp_state)
            
            if not game_controller.apply_move(move):
                continue
            v = self.minimax(temp_state, depth - 1, alpha, beta, maximizer=False)

            if v > best_value:
                best_value = v
                best_move = move
            
            if v >= beta:
                break # Impossible in the first level.
            alpha = max(alpha, best_value)
                
        return best_move
    



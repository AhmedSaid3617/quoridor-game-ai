from src.state import GameState
from src.rules import GameRules
import unittest
import numpy as np

from src.state.game_state import GameStateBiased


class TestRulesOperations(unittest.TestCase):
    # Setup Method (Runs before *every* test method)
    def setUp(self):
        state = GameState()
        biased = state.get_biased_for_player(GameState.Player.PLAYER_ONE)
        self.rules = GameRules(biased)

    # Teardown Method (Runs after *every* test method)
    def tearDown(self):
        del self.rules

    # --- Test Methods (Must start with 'test_') ---

    def test_initial_position(self):
        self.assertEqual(self.rules.game_state.player_one, GameState.Position(4, 8))
        self.assertEqual(self.rules.game_state.player_two, GameState.Position(4, 0))

    def test_move_blocked_by_wall(self):
        horizontal_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()

        vertical_edges = np.array([
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

        self.rules.game_state.vertical_edges = vertical_edges
        self.rules.game_state.horizontal_edges = horizontal_edges
        
        self.assertTrue(self.rules._can_move_up(GameState.Position(4, 4)))
        self.assertTrue(self.rules._can_move_right(GameState.Position(4, 4)))
        self.assertTrue(self.rules._can_move_down(GameState.Position(4, 4)))
        self.assertTrue(self.rules._can_move_left(GameState.Position(4, 4)))

        self.assertFalse(self.rules._can_move_up(GameState.Position(0, 0)))
        self.assertTrue(self.rules._can_move_down(GameState.Position(0, 0)))
        self.assertTrue(self.rules._can_move_right(GameState.Position(0, 0)))
        self.assertFalse(self.rules._can_move_left(GameState.Position(0, 0)))

        self.assertTrue(self.rules._can_move_up(GameState.Position(8, 8)))
        self.assertFalse(self.rules._can_move_down(GameState.Position(8, 8)))
        self.assertFalse(self.rules._can_move_right(GameState.Position(8, 8)))
        self.assertTrue(self.rules._can_move_left(GameState.Position(8, 8)))

        # Place walls around (4,4)

        horizontal_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()

        vertical_edges = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]).astype(bool).tolist()

        self.rules.game_state.vertical_edges = vertical_edges
        self.rules.game_state.horizontal_edges = horizontal_edges

        self.assertFalse(self.rules._can_move_up(GameState.Position(4, 4)))
        self.assertFalse(self.rules._can_move_right(GameState.Position(4, 4)))
        self.assertTrue(self.rules._can_move_down(GameState.Position(4, 4)))
        self.assertTrue(self.rules._can_move_left(GameState.Position(4, 4)))

        self.assertFalse(self.rules._can_move_up(GameState.Position(3, 4)))
        self.assertTrue(self.rules._can_move_right(GameState.Position(3, 4)))
        self.assertTrue(self.rules._can_move_down(GameState.Position(3, 4)))
        self.assertFalse(self.rules._can_move_left(GameState.Position(3, 4)))

        self.assertTrue(self.rules._can_move_up(GameState.Position(3, 5)))
        self.assertTrue(self.rules._can_move_right(GameState.Position(3, 5)))
        self.assertFalse(self.rules._can_move_down(GameState.Position(3, 5)))
        self.assertFalse(self.rules._can_move_left(GameState.Position(3, 5)))

        self.assertTrue(self.rules._can_move_up(GameState.Position(4, 5)))
        self.assertFalse(self.rules._can_move_right(GameState.Position(4, 5)))
        self.assertFalse(self.rules._can_move_down(GameState.Position(4, 5)))
        self.assertTrue(self.rules._can_move_left(GameState.Position(4, 5)))

    def test_can_move_up_all_cases(self):
        rules = self.rules
        gs = rules.game_state
        # Case 1: y == 0
        self.assertFalse(rules._can_move_up(GameState.Position(4, 0)), "Should not move up from y=0")
        # Case 2: Blocked by horizontal wall
        gs.horizontal_edges[3][4] = True
        self.assertFalse(rules._can_move_up(GameState.Position(4, 4)), "Should not move up if horizontal wall above")
        gs.horizontal_edges[3][4] = False
        # Case 3: Opponent directly above
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(4, 3)
        self.assertFalse(rules._can_move_up(GameState.Position(4, 4)), "Should not move up if opponent directly above")
        # Case 4: Nothing blocks
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(0, 0)
        self.assertTrue(rules._can_move_up(GameState.Position(4, 4)), "Should move up if nothing blocks")
        # Case 5: Not a player position
        self.assertTrue(rules._can_move_up(GameState.Position(2, 2)), "Should move up from generic position if nothing blocks")
        # Reset for other tests
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)

    def test_can_move_right_all_cases(self):
        rules = self.rules
        gs = rules.game_state
        # Case 1: x == 8 (edge of board)
        self.assertFalse(rules._can_move_right(GameState.Position(8, 4)), "Should not move right from x=8")
        # Case 2: Blocked by vertical wall
        gs.vertical_edges[4][4] = True
        self.assertFalse(rules._can_move_right(GameState.Position(4, 4)), "Should not move right if vertical wall blocks")
        gs.vertical_edges[4][4] = False
        # Case 3: Opponent directly right
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(5, 4)
        self.assertFalse(rules._can_move_right(GameState.Position(4, 4)), "Should not move right if opponent directly right")
        # Case 4: Nothing blocks
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(0, 0)
        self.assertTrue(rules._can_move_right(GameState.Position(4, 4)), "Should move right if nothing blocks")
        # Case 5: Not a player position
        self.assertTrue(rules._can_move_right(GameState.Position(2, 2)), "Should move right from generic position if nothing blocks")
        # Reset for other tests
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)

    def test_can_move_left_all_cases(self):
        rules = self.rules
        gs = rules.game_state
        # Case 1: x == 0 (edge of board)
        self.assertFalse(rules._can_move_left(GameState.Position(0, 4)), "Should not move left from x=0")
        # Case 2: Blocked by vertical wall
        gs.vertical_edges[4][3] = True
        self.assertFalse(rules._can_move_left(GameState.Position(4, 4)), "Should not move left if vertical wall blocks")
        gs.vertical_edges[4][3] = False
        # Case 3: Opponent directly left
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(3, 4)
        self.assertFalse(rules._can_move_left(GameState.Position(4, 4)), "Should not move left if opponent directly left")
        # Case 4: Nothing blocks
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(0, 0)
        self.assertTrue(rules._can_move_left(GameState.Position(4, 4)), "Should move left if nothing blocks")
        # Case 5: Not a player position
        self.assertTrue(rules._can_move_left(GameState.Position(2, 2)), "Should move left from generic position if nothing blocks")
        # Reset for other tests
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)

    def test_can_move_down_all_cases(self):
        rules = self.rules
        gs = rules.game_state
        # Case 1: y == 8 (edge of board)
        self.assertFalse(rules._can_move_down(GameState.Position(4, 8)), "Should not move down from y=8")
        # Case 2: Blocked by horizontal wall
        gs.horizontal_edges[4][4] = True
        self.assertFalse(rules._can_move_down(GameState.Position(4, 4)), "Should not move down if horizontal wall blocks")
        gs.horizontal_edges[4][4] = False
        # Case 3: Opponent directly below
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(4, 5)
        self.assertFalse(rules._can_move_down(GameState.Position(4, 4)), "Should not move down if opponent directly below")
        # Case 4: Nothing blocks
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(0, 0)
        self.assertTrue(rules._can_move_down(GameState.Position(4, 4)), "Should move down if nothing blocks")
        # Case 5: Not a player position
        self.assertTrue(rules._can_move_down(GameState.Position(2, 2)), "Should move down from generic position if nothing blocks")
        # Reset for other tests
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)

    def test_can_jump_up(self):
        rules = self.rules
        gs = rules.game_state
        # Opponent directly above and can move up
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(4, 3)
        gs.horizontal_edges[2][4] = False
        self.assertTrue(rules._can_jump_up(gs.player_one), "Should jump up if opponent directly above and path is clear")
        # Opponent directly above but blocked by wall
        gs.horizontal_edges[2][4] = True
        self.assertFalse(rules._can_jump_up(gs.player_one), "Should not jump up if wall blocks opponent's up move")
        # Opponent not directly above
        gs.opponent = GameState.Position(3, 3)
        self.assertFalse(rules._can_jump_up(gs.player_one), "Should not jump up if opponent not directly above")
        # Reset
        gs.horizontal_edges[2][4] = False
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)

    def test_can_jump_down(self):
        rules = self.rules
        gs = rules.game_state
        # Opponent directly below and can move down
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(4, 5)
        gs.horizontal_edges[5][4] = False
        self.assertTrue(rules._can_jump_down(gs.player_one), "Should jump down if opponent directly below and path is clear")
        # Opponent directly below but blocked by wall
        gs.horizontal_edges[5][4] = True
        self.assertFalse(rules._can_jump_down(gs.player_one), "Should not jump down if wall blocks opponent's down move")
        # Opponent not directly below
        gs.opponent = GameState.Position(3, 5)
        self.assertFalse(rules._can_jump_down(gs.player_one), "Should not jump down if opponent not directly below")
        # Reset
        gs.horizontal_edges[5][4] = False
        gs.player_one = GameState.Position(4, 8)  
        gs.opponent = GameState.Position(4, 0)

    def test_can_jump_right(self):
        rules = self.rules
        gs = rules.game_state
        # Opponent directly right and can move right
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(5, 4)
        gs.vertical_edges[4][5] = False
        self.assertTrue(rules._can_jump_right(GameState.Position(4, 4)), "Should jump right if opponent directly right and path is clear")
        # Opponent directly right but blocked by wall
        gs.vertical_edges[4][5] = True
        self.assertFalse(rules._can_jump_right(GameState.Position(4, 4)), "Should not jump right if wall blocks opponent's right move")
        # Opponent not directly right
        gs.opponent = GameState.Position(5, 5)
        self.assertFalse(rules._can_jump_right(GameState.Position(4, 4)), "Should not jump right if opponent not directly right")
        # Reset
        gs.vertical_edges[4][5] = False
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)

    def test_can_jump_left(self):
        rules = self.rules
        gs = rules.game_state
        # Opponent directly left and can move left
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(3, 4)
        gs.vertical_edges[4][2] = False
        self.assertTrue(rules._can_jump_left(GameState.Position(4, 4)), "Should jump left if opponent directly left and path is clear")
        # Opponent directly left but blocked by wall
        gs.vertical_edges[4][2] = True
        self.assertFalse(rules._can_jump_left(GameState.Position(4, 4)), "Should not jump left if wall blocks opponent's left move")
        # Opponent not directly left
        gs.opponent = GameState.Position(3, 5)
        self.assertFalse(rules._can_jump_left(GameState.Position(4, 4)), "Should not jump left if opponent not directly left")
        # Reset
        gs.vertical_edges[4][2] = False
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)

    def test_can_move_ne(self):
        rules = self.rules
        gs = rules.game_state
        # Opponent directly above and can't move up
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(4, 3)
        gs.horizontal_edges[2][4] = True
        self.assertTrue(rules._can_move_ne(gs.player_one), "Should move ne if opponent directly above and can't move up")

        # opponent right move is blocked
        gs.vertical_edges[3][4] = True
        self.assertFalse(rules._can_move_ne(gs.player_one), "Should move not ne if opponent directly above and can't move up or right")
        gs.vertical_edges[3][4] = False

        # Opponent directly up but can move up
        gs.horizontal_edges[2][4] = False
        self.assertFalse(rules._can_move_ne(gs.player_one), "Should not move ne if opponent directly above and can move up")

        #opponent is on  the right and can't move to the right
        gs.opponent = GameState.Position(5,4)
        gs.vertical_edges [4][5] = True
        self.assertTrue(rules._can_move_ne(gs.player_one), "Should move ne if opponent directly right and can't move right")

        # opponent is not directly above or to the right
        gs.opponent = GameState.Position(4,5) 
        gs.vertical_edges [4][5] = False
        self.assertFalse(rules._can_move_ne(gs.player_one), "Should not move ne if opponent is not directly to the right or above")

        # Reset
        gs.vertical_edges[4][2] = False
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)


    def test_can_move_nw(self):
        rules = self.rules
        gs = rules.game_state
        # Opponent directly above and can't move up
        gs.player_one = GameState.Position(4, 4)
        gs.opponent = GameState.Position(4, 3)
        gs.horizontal_edges[2][4] = True
        self.assertTrue(rules._can_move_nw(gs.player_one), "Should move nw if opponent directly above and can't move up")

        # opponent left move is blocked
        gs.vertical_edges[3][3] = True
        self.assertFalse(rules._can_move_nw(gs.player_one), "Should move not nw if opponent directly above and can't move up or left")
        gs.vertical_edges[3][3] = False

        # Opponent directly up but can move up
        gs.horizontal_edges[2][4] = False
        self.assertFalse(rules._can_move_nw(gs.player_one), "Should not move nw if opponent directly above and can move up")

        #opponent is on  the right and can't move to the right
        gs.player_one = GameState.Position(2,5)
        gs.opponent = GameState.Position(1,5)
        gs.vertical_edges [5][0] = True
        gs.vertical_edges [6][0] = False
        self.assertTrue(rules._can_move_nw(gs.player_one), "Should move nw if opponent directly left and can't move left")

        # opponent is not directly above or to the left
        gs.opponent = GameState.Position(4,5) 
        self.assertFalse(rules._can_move_nw(gs.player_one), "Should not move nw if opponent is not directly to the left or above")

        # Reset
        gs.vertical_edges[4][2] = False
        gs.vertical_edges[5][0] = False
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)

    def test_can_move_se(self):
        rules = self.rules
        gs = rules.game_state
        # Opponent directly below and can't move down
        gs.player_one = GameState.Position(6, 5)
        gs.opponent = GameState.Position(6, 6)
        gs.horizontal_edges[6][6] = True
        self.assertTrue(rules._can_move_se(gs.player_one), "Should move sw if opponent directly below and can't move down")

        # opponent right move is blocked
        gs.vertical_edges[6][6] = True
        self.assertFalse(rules._can_move_se(gs.player_one), "Should move not se if opponent directly below and can't move down or right")
        gs.vertical_edges[6][6] = False

        # Opponent directly down but can move down
        gs.horizontal_edges[6][6] = False
        self.assertFalse(rules._can_move_se(gs.player_one), "Should not move se if opponent directly below and can move down")

        #opponent is on  the right and can't move to the right
        gs.opponent = GameState.Position(7,5)
        gs.vertical_edges [5][7] = True
        self.assertTrue(rules._can_move_se(gs.player_one), "Should move se if opponent directly right and can't move right")
        gs.vertical_edges [5][7] = False

        # opponent is not directly below or to the right
        gs.opponent = GameState.Position(4,5) 
        gs.vertical_edges [4][5] = False
        self.assertFalse(rules._can_move_se(gs.player_one), "Should not move se if opponent is not directly to the right or below")

        # Reset
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)


    def test_can_move_sw(self):
        rules = self.rules
        gs = rules.game_state
        gs.opponent = GameState.Position(6, 6)
        # Opponent directly below and can't move down
        gs.player_one = GameState.Position(6, 5)
        gs.opponent = GameState.Position(6, 6)
        gs.horizontal_edges[6][6] = True
        self.assertTrue(rules._can_move_sw(gs.player_one), "Should move sw if opponent directly below and can't move down")

        # opponent left move is blocked
        gs.vertical_edges[6][5] = True
        self.assertFalse(rules._can_move_sw(gs.player_one), "Should move not sw if opponent directly below and can't move down or left")
        gs.vertical_edges[6][5] = False

        # Opponent directly up but can move up
        gs.horizontal_edges[6][6] = False
        self.assertFalse(rules._can_move_sw(gs.player_one), "Should not move sw if opponent directly below and can move down")

        #opponent is on  the left and can't move to the left
        gs.player_one = GameState.Position(6,5)
        gs.opponent = GameState.Position(5,5)
        gs.vertical_edges [5][4] = True
        self.assertTrue(rules._can_move_sw(gs.player_one), "Should move sw if opponent directly left and can't move left")

        # opponent is not directly above or to the left
        gs.opponent = GameState.Position(4,5) 
        self.assertFalse(rules._can_move_sw(gs.player_one), "Should not move sw if opponent is not directly to the left or below")

        # Reset
        gs.player_one = GameState.Position(4, 8)
        gs.opponent = GameState.Position(4, 0)


    def test_all_valid_moves(self):
        rules = self.rules
        gs = rules.game_state # starting of game

        expected_relative = {
                GameRules.PawnMove(GameRules.PawnMove.SystemType.RELATIVE, movement=GameRules.PawnMove.MovementType.UP),
                GameRules.PawnMove(GameRules.PawnMove.SystemType.RELATIVE, movement=GameRules.PawnMove.MovementType.RIGHT),
                GameRules.PawnMove(GameRules.PawnMove.SystemType.RELATIVE, movement=GameRules.PawnMove.MovementType.LEFT),
        }
        actual_relative = rules.all_pawn_moves_relative(GameState.Player.PLAYER_ONE)
        
        self.assertEqual(actual_relative, expected_relative)
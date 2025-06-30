import random
import chess
from utils.constants import CHECKMATE_SCORE, DRAW_SCORE, DEFAULT_DEPTH
from .evaluator import score_board

def find_random_move(valid_moves):
    """Find a random valid move."""
    return valid_moves[random.randint(0, len(valid_moves) - 1)]

def find_best_move(game_state, valid_moves):
    """Find the best move in the current position using alpha-beta search."""
    global next_move, nodes
    next_move = None
    random.shuffle(valid_moves)
    nodes = 0

    # Convert to python-chess board for book moves and tablebases
    board = chess.Board(game_state.board_to_fen())

    # Search for the best move
    next_eval = find_move_negamax_alpha_beta(
        game_state, 
        valid_moves, 
        DEFAULT_DEPTH, 
        -CHECKMATE_SCORE, 
        CHECKMATE_SCORE, 
        1 if game_state.whiteToMove else -1
    )

    # If a mate is detected, search for the shortest mate
    if abs(next_eval) == CHECKMATE_SCORE:
        shortest_mate = search_for_shortest_mate(game_state, valid_moves)
        if shortest_mate:
            next_move, mate_in = shortest_mate
            print(f"Mate in {mate_in} moves")
            return next_move

    print("Nodes Visited:", nodes)
    return next_move

def search_for_shortest_mate(game_state, valid_moves):
    """Search for the shortest mate sequence."""
    for depth in range(1, DEFAULT_DEPTH + 1):
        result = find_mate_in_n(game_state, valid_moves, depth, game_state.whiteToMove)
        if result:
            return result
    return None

def find_mate_in_n(game_state, valid_moves, depth, is_white_to_move):
    """Find a mate in n moves."""
    for move in valid_moves:
        game_state.make_move(move)
        if game_state.checkmate:
            game_state.undo_move()
            return move, 1
        
        if depth > 1:
            opponent_moves = game_state.get_valid_moves()
            if game_state.stalemate or game_state.is_threefold_repetition() or game_state.is_fifty_move_rule():
                game_state.undo_move()
                continue
            
            all_lose = True
            for opponent_move in opponent_moves:
                game_state.make_move(opponent_move)
                opponent_valid_moves = game_state.get_valid_moves()
                result = find_mate_in_n(game_state, opponent_valid_moves, depth - 1, not is_white_to_move)
                game_state.undo_move()
                if not result:
                    all_lose = False
                    break
            game_state.undo_move()
            if all_lose:
                return move, depth
        else:
            game_state.undo_move()
    return None

def find_move_negamax_alpha_beta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    """Find the best move using negamax algorithm with alpha-beta pruning."""
    global next_move, nodes
    nodes += 1

    if depth == 0:
        return turn_multiplier * score_board(game_state)

    max_score = -CHECKMATE_SCORE
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -find_move_negamax_alpha_beta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        game_state.undo_move()
        
        if score > max_score:
            max_score = score
            if depth == DEFAULT_DEPTH:
                next_move = move
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return max_score 
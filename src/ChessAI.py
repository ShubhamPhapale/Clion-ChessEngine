# import chess
# import chess.engine
import random
# import time

# engine_path = "/opt/homebrew/bin/stockfish"
# stockfish_engine = chess.engine.SimpleEngine.popen_uci(engine_path)

piece_Score = {'K': 200, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}

white_Pawn_Scores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
    [0.5, 1, 1, -2, -2, 1, 1, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

black_Pawn_Scores = list(reversed(white_Pawn_Scores))

knight_Scores = [
    [-5, -4, -3, -3, -3, -3, -4, -5],
    [-4, -2, 0, 0, 0, 0, -2, -4],
    [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
    [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
    [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
    [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
    [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
    [-5, -4, -3, -3, -3, -3, -4, -5]
]

bishop_Scores = [
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
    [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
    [-1, 0, 1, 1, 1, 1, 0, -1],
    [-1, 1, 1, 1, 1, 1, 1, -1],
    [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]
]

white_Rook_Scores = [
    [0, 0, 0, 0.5, 0.5, 0, 0, 0],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [0.5, 1, 1, 1, 1, 1, 1, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

black_Rook_Scores = list(reversed(white_Rook_Scores))

queen_Scores = [
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-1, 0, 0.5, 0, 0, 0, 0, -1],
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
]

white_King_Scores = [
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [2, 3, 1, 0, 0, 1, 3, 2]
]

black_King_Scores = list(reversed(white_King_Scores))

white_King_Endgame_Scores = [
    [-5, -4, -3, -2, -2, -3, -4, -5],
    [-3, -2, -1, 0, 0, -1, -2, -3],
    [-3, -1, 2, 3, 3, 2, -1, -3],
    [-3, -1, 3, 4, 4, 3, -1, -3],
    [-3, -1, 3, 4, 4, 3, -1, -3],
    [-3, -1, 2, 3, 3, 2, -1, -3],
    [-3, -3, 0, 0, 0, 0, -3, -3],
    [-5, -3, -3, -3, -3, -3, -3, -5]
]

black_King_Endgame_Scores = list(reversed(white_King_Endgame_Scores))

piece_Position_Scores = {
    'wP': white_Pawn_Scores,
    'bP': black_Pawn_Scores,
    'N': knight_Scores,
    'B': bishop_Scores,
    'wR': white_Rook_Scores,
    'bR': black_Rook_Scores,
    'Q': queen_Scores,
    'wK': white_King_Scores,
    'bK': black_King_Scores,
    'wK_end': white_King_Endgame_Scores,
    'bK_end': black_King_Endgame_Scores
}

CHECKMATE = 10000
STALEMATE = 0
DEPTH = 5

# transposition_table = {}

def find_Random_Move(valid_Moves):
    return valid_Moves[random.randint(0, len(valid_Moves) - 1)]

def find_Best_Move(gs, valid_Moves, return_Queue):
    global next_Move, nodes #, DEPTH
    # if is_Endgame(gs) and DEPTH !=10:
    #     DEPTH = 10
    next_Move = None
    random.shuffle(valid_Moves)
    nodes = 0
    find_Move_Nega_Max_Alpha_Beta(gs, valid_Moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print("Nodes Visited:", nodes)
    # engine.quit()
    return_Queue.put(next_Move)

# def find_Best_Move(gs, valid_Moves, return_Queue, transposition_table):
#     print(len(transposition_table))
#     global next_Move, nodes
#     next_Move = None
#     random.shuffle(valid_Moves)
#     nodes = 0

#     # Iterative deepening
#     for depth in range(0, DEPTH + 1):
#         find_Move_Nega_Max_Alpha_Beta(gs, valid_Moves, depth, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1, transposition_table)
    
#     print("Nodes Visited:", nodes)
#     return_Queue.put(next_Move)


def find_Move_Nega_Max_Alpha_Beta(gs, valid_Moves, depth, alpha, beta, turn):
    global next_Move, nodes
    nodes += 1
    if depth == 0:
        # return evaluate_with_stockfish(gs.board_to_fen()) * turn
        return score_Board(gs) * turn

    # Move ordering (simple version: prioritize captures)
    valid_Moves.sort(key=lambda move: piece_Score.get(move.piece_Captured[1], 0) if move.is_Capture else 0, reverse=True)

    max_Score = -CHECKMATE
    for move in valid_Moves:
        gs.make_Move(move)
        next_Moves = gs.get_Valid_Moves()
        score = -find_Move_Nega_Max_Alpha_Beta(gs, next_Moves, depth - 1, -beta, -alpha, -turn)
        if score > max_Score:
            max_Score = score
            if depth == DEPTH:
                next_Move = move
                print(str(next_Move), "% .2f" % max_Score, "at depth", DEPTH)
        gs.undo_Move()
        if max_Score > alpha:
            alpha = max_Score
        if alpha >= beta:
            break

    return max_Score

# def find_Move_Nega_Max_Alpha_Beta(gs, valid_Moves, depth, alpha, beta, turn, transposition_table):
#     global next_Move, nodes
#     nodes += 1

#     position_key = gs.board_to_fen()
#     if position_key in transposition_table and transposition_table[position_key]['depth'] > depth:
#         print("Transposition Table Used")
#         return transposition_table[position_key]['score']

#     if depth == 0:
#         return score_Board(gs) * turn

#     valid_Moves.sort(key=lambda move: piece_Score.get(move.piece_Captured[1], 0) if move.is_Capture else 0, reverse=True)

#     max_Score = -CHECKMATE
#     best_Move = None
#     for move in valid_Moves:
#         gs.make_Move(move)
#         next_Moves = gs.get_Valid_Moves()
#         score = -find_Move_Nega_Max_Alpha_Beta(gs, next_Moves, depth - 1, -beta, -alpha, -turn, transposition_table)
#         if score > max_Score:
#             max_Score = score
#             best_Move = move
#         gs.undo_Move()
#         if max_Score > alpha:
#             alpha = max_Score
#         if alpha >= beta:
#             break

#     transposition_table[position_key] = {'depth': depth, 'score': max_Score}
#     if depth == DEPTH:
#         next_Move = best_Move
#         print(str(next_Move), "%.2f" % max_Score, "at depth", DEPTH)
#     return max_Score

def score_Board(gs):
    # start_time = time.time()
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = score_Position(gs)
    # end_time = time.time()  
    # elapsed_time = end_time - start_time  
    # print(f"Time taken for evaluation: {elapsed_time:.4f} seconds")
    return score

def score_Position(gs):
    score = 0
    endgame = is_Endgame(gs)
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piece_Position_Score = 0
                if square[1] == 'P':
                    piece_Position_Score = piece_Position_Scores[square][row][col]
                elif square[1] == 'R':
                    piece_Position_Score = piece_Position_Scores[square][row][col]
                elif square[1] == 'K':
                    if endgame:
                        piece_Position_Score = piece_Position_Scores[square + '_end'][row][col]
                    else:
                        piece_Position_Score = piece_Position_Scores[square][row][col]
                else:
                    piece_Position_Score = piece_Position_Scores[square[1]][row][col]

                if square[0] == 'w':
                    score += piece_Score[square[1]] + piece_Position_Score * 0.1
                elif square[0] == 'b':
                    score -= piece_Score[square[1]] + piece_Position_Score * 0.1
    return score

def is_Endgame(gs):
    """ Determine if the game is in the endgame phase """
    totalMaterial = sum(piece_Score[piece[1]] for row in gs.board for piece in row if (piece != "--" and piece[1] != 'K'))
    return totalMaterial <= 30  # arbitrary threshold for endgame

# def evaluate_with_stockfish(fen):
#     # Timing the evaluation process
#     try:
#         # Timing the board creation
#         # start_time = time.time()
#         board = chess.Board(fen)
#         # end_time = time.time()
#         # elapsed_time = end_time - start_time
#         # print(f"Time taken to create board: {elapsed_time:.4f} seconds")

#         # Timing the analysis
#         # start_time = time.time()
#         info = stockfish_engine.analyse(board, chess.engine.Limit(nodes=1))
#         # end_time = time.time()
#         # elapsed_time = end_time - start_time
#         # print(f"Time taken for analysis: {elapsed_time:.4f} seconds")

#         # Timing the score extraction
#         # start_time = time.time()
#         score = info['score'].relative.score()
#         # end_time = time.time()
#         # elapsed_time = end_time - start_time
#         # print(f"Time taken to extract score: {elapsed_time:.4f} seconds")

#         return score / 100.0
#     except Exception as e:
#         print(f"An error occurred during evaluation: {e}")
#         return None

# import atexit
# atexit.register(stockfish_engine.quit)
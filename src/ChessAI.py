import chess
import chess.engine
import random

piece_Score = {'K': 20, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}

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

CHECKMATE = 200
STALEMATE = 0
DEPTH = 5

def find_Random_Move(valid_Moves):
    return valid_Moves[random.randint(0, len(valid_Moves) - 1)]

def find_Best_Move(gs, valid_Moves, return_Queue):
    global next_Move, nodes
    next_Move = None
    random.shuffle(valid_Moves)
    nodes = 0
    find_Move_Nega_Max_Alpha_Beta(gs, valid_Moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print("Nodes Visited:", nodes)
    return_Queue.put(next_Move)

def find_Move_Nega_Max_Alpha_Beta(gs, valid_Moves, depth, alpha, beta, turn):
    global next_Move, nodes
    nodes += 1
    if depth == 0:
        return score_Board(gs) * turn

    # Move ordering (simple version: prioritize captures)
    valid_Moves.sort(key=lambda move: piece_Score.get(move.piece_Captured, 0), reverse=True)

    max_Score = -CHECKMATE
    for move in valid_Moves:
        gs.make_Move(move)
        next_Moves = gs.get_Valid_Moves()
        score = -find_Move_Nega_Max_Alpha_Beta(gs, next_Moves, depth - 1, -beta, -alpha, -turn)
        if score > max_Score:
            max_Score = score
            if depth == DEPTH:
                next_Move = move
                print("Current Best Move is", next_Move.get_Chess_Notation(), "with score", "% .2f" % max_Score)
        gs.undo_Move()
        if max_Score > alpha:
            alpha = max_Score
        if alpha >= beta:
            break
    # Adjust for checkmate depth
    return max_Score - (1 if max_Score == CHECKMATE else 0) + (1 if max_Score == -CHECKMATE else 0)

def score_Board(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = score_Position(gs)
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
    totalMaterial = sum(piece_Score[piece[1]] for row in gs.board for piece in row if piece != "--")
    return totalMaterial <= 30  # arbitrary threshold for endgame

def evaluate_with_stockfish(fen):
    with chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish") as engine:
        board = chess.Board(fen)
        info = engine.analyse(board, chess.engine.Limit(time=0.1))
        return info['score'].relative.score()
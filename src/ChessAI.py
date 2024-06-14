import random

piece_Score = {'K': 20, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}

white_Pawn_Scores = [
        [15, 15, 15, 15, 15, 15, 15, 15],
        [8, 8, 8, 8, 8, 8, 8, 8],
        [4, 4, 4, 4, 4, 4, 4, 4],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [2, 1, 2, 3, 3, 2, 1, 2],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        ]

black_Pawn_Scores = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 4, 4, 3, 3, 3],
        [4, 3, 4, 5, 5, 4, 3, 4],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [7, 7, 7, 7, 7, 7, 7, 7],
        [8, 8, 8, 8, 8, 8, 8, 8],
        [10, 10, 10, 10, 10, 10, 10, 10],
    ]

knight_Scores = [
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 1, 1, 1, 1, 0, -1],
        [-1, 0, 1, 2, 2, 1, 0, -1],
        [-1, 0, 1, 2, 2, 1, 0, -1],
        [-1, 0, 1, 1, 1, 1, 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1]
        ]

bishop_Scores = [
        [3, 2, 1, 0, 0, 1, 2, 3],
        [2, 3, 2, 1, 1, 2, 3, 2],
        [1, 2, 3, 2, 2, 3, 2, 1],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [1, 2, 3, 2, 2, 3, 2, 1],
        [2, 3, 2, 1, 1, 2, 3, 2],
        [3, 2, 3, 0, 0, 1, 2, 3]
        ]

white_Rook_Scores = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 2, 1, 1, 2, 0, 0],
        ]

black_Rook_Scores = [
        [0, 0, 2, 1, 1, 2, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [1, 1, 1, 1, 1, 1, 1, 1],
        ]

queen_Scores = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 2, 2, 2, 2, 1, 0],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [0, 1, 2, 2, 2, 2, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
        ]
white_King_Scores = [
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 0, 0, 1, 3, 1],
    ]

black_King_Scores = [
    [1, 3, 3, 0, 0, 1, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    ]

piece_Position_Scores = {'wP': white_Pawn_Scores, 'bP': black_Pawn_Scores, 'N': knight_Scores, 'B': bishop_Scores, 'wR': white_Rook_Scores, 'bR': black_Rook_Scores, 'Q': queen_Scores, 'wK': white_King_Scores, 'bK': black_King_Scores}

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
    
    # implement move ordering here later
    max_Score = -CHECKMATE
    for move in valid_Moves:
        gs.make_Move(move)
        next_Moves = gs.get_Valid_Moves()
        score = -find_Move_Nega_Max_Alpha_Beta(gs, next_Moves, depth - 1, -beta, -alpha, -turn)
        if score > max_Score:
            max_Score = score
            if depth == DEPTH:
                next_Move = move
                print("Current Best Move is", next_Move.get_Chess_Notation(), "with score", max_Score)
        gs.undo_Move()
        if max_Score > alpha:
            alpha = max_Score
        if alpha >= beta:
            break
    return max_Score
    
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
                    piece_Position_Score = piece_Position_Scores[square][row][col]
                else:
                    piece_Position_Score = piece_Position_Scores[square[1]][row][col]

                if square[0] == 'w':
                    score += piece_Score[square[1]] + piece_Position_Score * 0.1
                elif square[0] == 'b':
                    score -= piece_Score[square[1]] + piece_Position_Score * 0.1
    return score
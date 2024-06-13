import random

piece_Score = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def find_Random_Move(valid_Moves):
    return valid_Moves[random.randint(0, len(valid_Moves) - 1)]

def find_Best_Move(gs, valid_Moves):
    global next_Move
    next_Move = None
    random.shuffle(valid_Moves)
    find_Move_Nega_Max(gs, valid_Moves, DEPTH, 1 if gs.whiteToMove else -1)
    return next_Move

def find_Move_Nega_Max(gs, valid_Moves, depth, turn):
    global next_Move
    if depth == 0:
        return score_Board(gs) * turn
    
    max_Score = -CHECKMATE
    for move in valid_Moves:
        gs.make_Move(move)
        next_Moves = gs.get_Valid_Moves()
        score = -find_Move_Nega_Max(gs, next_Moves, depth - 1, -turn)
        if score > max_Score:
            max_Score = score
            if depth == DEPTH:
                next_Move = move
                print(next_Move.get_Chess_Notation(), max_Score)
        gs.undo_Move()
    return max_Score
    
def score_Board(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    
    score = score_Material(gs.board)
    return score


def score_Material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_Score[square[1]]
            elif square[0] == 'b':
                score -= piece_Score[square[1]]
    return score
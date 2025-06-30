from utils.constants import PIECE_VALUES, CHECKMATE_SCORE

def score_board(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if game_state.checkmate:
        if game_state.whiteToMove:
            return -CHECKMATE_SCORE  # Black wins
        else:
            return CHECKMATE_SCORE  # White wins
    elif game_state.stalemate:
        return 0

    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != 'K':  # Skip king position evaluation in middlegame
                    if piece[0] == 'w':
                        piece_position_score = get_piece_position_score(piece[1], row, col)
                    else:
                        piece_position_score = get_piece_position_score(piece[1], 7-row, col)

                if piece[0] == 'w':
                    score += PIECE_VALUES[piece[1]] + piece_position_score
                elif piece[0] == 'b':
                    score -= PIECE_VALUES[piece[1]] + piece_position_score

    return score

def get_piece_position_score(piece, row, col):
    """Get the position score for a piece at a given position."""
    piece_position_scores = {
        'P': [  # Pawn position scores
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ],
        'N': [  # Knight position scores
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ],
        'B': [  # Bishop position scores
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ],
        'R': [  # Rook position scores
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]
        ],
        'Q': [  # Queen position scores
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ]
    }
    
    return piece_position_scores.get(piece, [[0]*8]*8)[row][col]

def is_endgame(game_state):
    """
    Determine if the position is in the endgame phase.
    This is a simple implementation that considers it endgame if:
    1. Both sides have no queens or
    2. Every side which has a queen has additionally no other pieces or at most one minor piece
    """
    white_queen = black_queen = False
    white_minor_pieces = black_minor_pieces = 0
    
    for row in game_state.board:
        for piece in row:
            if piece == "wQ":
                white_queen = True
            elif piece == "bQ":
                black_queen = True
            elif piece in ["wN", "wB"]:
                white_minor_pieces += 1
            elif piece in ["bN", "bB"]:
                black_minor_pieces += 1
    
    if not white_queen and not black_queen:
        return True
    if white_queen and white_minor_pieces <= 1 and black_queen and black_minor_pieces <= 1:
        return True
    return False 
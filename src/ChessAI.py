import random
import chess
import chess.polyglot
import chess.syzygy

piece_Score = {'K': 9999, 'Q': 920, 'R': 510, 'B': 320, 'N': 280, 'P': 100}

pawn_Scores = [
    [ 0,   0,   0,   0,   0,   0,   0,   0,],
    [200,  200,  200,  200, 200,  200,  200,  200],
    [150,  150,  150,  150,  150,  150,  150,  150],
    [-17,  16,  -2,  15,  14,   0,  15, -13],
    [-26,   3,  10,   9,   6,   1,   0, -23],
    [-22,   9,   5, -11, -10,  -2,   3, -19],
    [-31,   8,  -7, -37, -36, -14,   3, -31],
    [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]
    ]
    # [
    # [ 0,   0,   0,   0,   0,   0,   0,   0,],
    # [78,  83,  86,  73, 102,  82,  85,  90],
    # [ 7,  29,  21,  44,  40,  31,  44,   7],
    # [-17,  16,  -2,  15,  14,   0,  15, -13],
    # [-26,   3,  10,   9,   6,   1,   0, -23],
    # [-22,   9,   5, -11, -10,  -2,   3, -19],
    # [-31,   8,  -7, -37, -36, -14,   3, -31],
    # [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]
    # ]

knight_Scores = [
    [-66, -53, -75, -75, -10, -55, -58, -70],
    [-3, -6, 100, -36, 4, 62, -4, -14],
    [10, 67, 1, 74, 73, 27, 62, -2],
    [24, 24, 45, 37, 33, 41, 25, 17],
    [-1, 5, 31, 21, 22, 35, 2, 0],
    [-18, 10, 13, 22, 18, 15, 11, -14],
    [-23, -15, 2, 0, 2, 0, -23, -20],
    [-66, -53, -75, -75, -10, -55, -58, -70]
    ]

bishop_Scores = [
    [-59, -78, -82, -76, -23, -107, -37, -50],
    [-11, 20, 35, -42, -39, 31, 2, -22],
    [-9, 39, -32, 41, 52, -10, 28, -14],
    [25, 17, 20, 34, 26, 25, 15, 10],
    [13, 10, 17, 23, 17, 16, 0, 7],
    [14, 25, 24, 15, 8, 25, 20, 15],
    [19, 20, 11, 6, 7, 6, 20, 16],
    [-7, 2, -15, -12, -14, -15, -10, -10]
    ]

rook_Scores = [
    [35,  29,  33,   4,  37,  33,  56,  50],
    [55,  29,  56,  67,  55,  62,  34,  60],
    [19,  35,  28,  33,  45,  27,  25,  15],
    [0,    5,  16,  13,  18,  -4,  -9,  -6],
    [-28, -35, -16, -21, -13, -29, -46, -30],
    [-42, -28, -42, -25, -25, -35, -26, -46],
    [-53, -38, -31, -26, -29, -43, -44, -53],
    [-30, -24, -18,   5,  -2, -18, -31, -32]
    ]

queen_Scores = [
    [  6,   1,  -8, -104,  69,  24,  88,  26],
    [ 14,  32,  60,  -10,  20,  76,  57,  24],
    [ -2,  43,  32,   60,  72,  63,  43,   2],
    [  1, -16,  22,   17,  25,  20, -13,  -6],
    [ -14, -15,  -2,   -5,  -1, -10, -20, -22],
    [ -30,  -6, -13,  -11, -16, -11, -16, -27],
    [ -36, -18,   0,  -19, -15, -15, -21, -38],
    [ -39, -30, -31,  -13, -31, -36, -34, -42]
    ]

white_King_Scores = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
]

white_King_Endgame_Scores = [
    [-50, -40, -30, -20, -20, -30, -40, -50],
    [-30, -20, -10, 0, 0, -10, -20, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -30, 0, 0, 0, 0, -30, -30],
    [-50, -30, -30, -30, -30, -30, -30, -50]
]

piece_Position_Scores = {
    "wP": pawn_Scores,
    "bP": pawn_Scores[::-1],
    "wN": knight_Scores,
    "bN": knight_Scores[::-1],
    "wB": bishop_Scores,
    "bB": bishop_Scores[::-1],
    "wR": rook_Scores,
    "bR": rook_Scores[::-1],
    "wQ": queen_Scores,
    "bQ": queen_Scores[::-1],
    'wK': white_King_Scores,
    'bK': white_King_Scores[::-1],
    'wK_end': white_King_Endgame_Scores,
    'bK_end': white_King_Endgame_Scores[::-1]
}

CHECKMATE = 100000
STALEMATE = 0
DEPTH = 3

def find_Random_Move(valid_Moves):
    return valid_Moves[random.randint(0, len(valid_Moves) - 1)]

def find_Best_Move(gs, valid_Moves, return_Queue):
    global next_Move, nodes 
    next_Move = None
    random.shuffle(valid_Moves)
    nodes = 0

    board = chess.Board(gs.board_to_fen())

    # Check for book move
    try:
        with chess.polyglot.open_reader('M11.2.bin') as reader:
            moves = []
            for entry in reader.find_all(board):
                moves.append(entry.move)
                if len(moves) >= 1:
                    break
            if moves:
                book_move = random.choice(moves)
                for move in valid_Moves:
                    if move.get_Chess_Notation() == str(book_move):
                        book_move = move
                return_Queue.put(book_move)
                return_Queue.put(0)
                return
    except:
        pass

    # try:
    #     with chess.syzygy.open_tablebase("3-4-5_pieces_Syzygy") as tablebase:
    #         wdl = tablebase.probe_wdl(board)
    #         dtz = tablebase.probe_dtz(board)
    #         if wdl is not None:
    #             print("endgame tablebase")
    #             for move in valid_Moves:
    #                 gs.make_Move(move)
    #                 if tablebase.probe_wdl(board) == wdl:
    #                     next_Move = move
    #                     break
    #                 gs.undo_Move()
    #             gs.undo_Move()
    #             return_Queue.put(next_Move)
    #             return_Queue.put(dtz if dtz is not None else 0)
    #             return
    # except Exception as e:
    #     print("Error accessing tablebase:", e)

    next_eval = find_Move_Nega_Max_Alpha_Beta(gs, valid_Moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)

    # If a mate is detected, search for the shortest mate
    if abs(next_eval) == CHECKMATE:
        shortest_mate = search_for_shortest_mate(gs, valid_Moves)
        if shortest_mate:
            next_Move, mate_in = shortest_mate
            print(f"Mate in {mate_in} moves")
            return_Queue.put(next_Move)
            return_Queue.put(CHECKMATE if gs.whiteToMove else -CHECKMATE)
            return

    print("Nodes Visited:", nodes)
    next_eval = next_eval if gs.whiteToMove else -next_eval
    return_Queue.put(next_Move)
    return_Queue.put(next_eval)

def search_for_shortest_mate(gs, valid_Moves):
    for depth in range(1, DEPTH + 1):
        result = find_mate_in_n(gs, valid_Moves, depth, gs.whiteToMove)
        if result:
            return result
    return None

def find_mate_in_n(gs, valid_Moves, depth, is_white_to_move):
    for move in valid_Moves:
        gs.make_Move(move)
        if gs.checkmate:
            gs.undo_Move()
            return move, 1
        if depth > 1:
            opponent_moves = gs.get_Valid_Moves()
            if gs.stalemate:  # Stalemate
                gs.undo_Move()
                continue
            all_lose = True
            for opp_move in opponent_moves:
                gs.make_Move(opp_move)
                sub_result = find_mate_in_n(gs, gs.get_Valid_Moves(), depth - 1, not is_white_to_move)
                gs.undo_Move()
                if not sub_result:
                    all_lose = False
                    break
            if all_lose:
                gs.undo_Move()
                return move, depth
        gs.undo_Move()
    return None

def find_Move_Nega_Max_Alpha_Beta(gs, valid_Moves, depth, alpha, beta, turn):
    global next_Move, nodes
    nodes += 1
    if depth == 0:
        return score_Board(gs) * turn

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

    if gs.stalemate: 
        max_Score = STALEMATE

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
    return score / 100

def score_Position(gs):
    score = 0
    endgame = is_Endgame(gs)
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piece_Position_Score = 0
                if square[1] == 'K':
                    if endgame:
                        piece_Position_Score = piece_Position_Scores[square + '_end'][row][col]
                    else:
                        piece_Position_Score = piece_Position_Scores[square][row][col]
                else:
                    piece_Position_Score = piece_Position_Scores[square][row][col]

                if square[0] == 'w':
                    score += piece_Score[square[1]] + piece_Position_Score
                elif square[0] == 'b':
                    score -= piece_Score[square[1]] + piece_Position_Score
    return score

def is_Endgame(gs):
    """ Determine if the game is in the endgame phase """
    totalMaterial = sum(piece_Score[piece[1]] for row in gs.board for piece in row if (piece != "--" and piece[1] != 'K'))
    return totalMaterial < 3000 
class Gamestate():
    def __init__(self):

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        
        self.whiteToMove = True
        self.moveLog = []

    def make_Move(self, move):
        self.board[move.start_Row][move.start_Col] = "--"
        self.board[move.end_Row][move.end_Col] = move.piece_Moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undo_Move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_Row][move.start_Col] = move.piece_Moved
            self.board[move.end_Row][move.end_Col] = move.piece_Captured
            self.whiteToMove = not self.whiteToMove

    def get_Valid_Moves(self):
        return self.get_All_Possible_Moves()
    
    def get_All_Possible_Moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.get_Pawn_Moves(r, c, moves)
                    elif piece == 'R':
                        self.get_Rook_Moves(r, c, moves)
        return moves

    def get_Pawn_Moves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))

    def get_Rook_Moves(self, r, c, moves):
        pass

class Move():
    ranks_To_Rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_TO_Ranks = {v: k for k, v in ranks_To_Rows.items()}
    filess_To_Cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    Cols_TO_Files = {v: k for k, v in filess_To_Cols.items()}

    def __init__(self, start_Square, end_Square, board):
        self.start_Row = start_Square[0]
        self.start_Col = start_Square[1]
        self.end_Row = end_Square[0]
        self.end_Col = end_Square[1]
        self.piece_Moved = board[self.start_Row][self.start_Col]
        self.piece_Captured = board[self.end_Row][self.end_Col]
        self.move_Id = self.start_Row * 1000 + self.start_Col * 100 + self.end_Row * 10 + self.end_Col

    '''
    overriding the equals method
    '''
    def __eq__(self, other):
        if (isinstance(other, Move)):
            return self.move_Id == other.move_Id
        return False

    def get_Chess_Notation(self):
        return self.get_Rank_Files(self.start_Row, self.start_Col) + self.get_Rank_Files(self.end_Row, self.end_Col)
    
    def get_Rank_Files(self, row, col):
        return self.Cols_TO_Files[col] + self.rows_TO_Ranks[row]
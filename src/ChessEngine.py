class Gamestate():
    def __init__(self):

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
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

    def get_Chess_Notation(self):
        return self.get_Rank_Files(self.start_Row, self.start_Col) + self.get_Rank_Files(self.end_Row, self.end_Col)
    
    def get_Rank_Files(self, row, col):
        return self.Cols_TO_Files[col] + self.rows_TO_Ranks[row]
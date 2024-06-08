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
        self.moveFunctions = {'P': self.get_Pawn_Moves, 'N': self.get_Knight_Moves, 'B': self.get_Bishop_Moves,
                              'R': self.get_Rook_Moves, 'Q': self.get_Queen_Moves, 'K': self.get_King_Moves}
        self.whiteToMove = True
        self.moveLog = []
        self.white_King_Location = (7, 4)
        self.black_King_Location = (0, 4)
        self.checkmate = False
        self.stalemate = False

    def make_Move(self, move):
        self.board[move.start_Row][move.start_Col] = "--"
        self.board[move.end_Row][move.end_Col] = move.piece_Moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.piece_Moved == 'wK':
            self.white_King_Location = (move.end_Row, move.end_Col)
        elif move.piece_Moved == 'bK':
            self.black_King_Location = (move.end_Row, move.end_Col)

    def undo_Move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_Row][move.start_Col] = move.piece_Moved
            self.board[move.end_Row][move.end_Col] = move.piece_Captured
            self.whiteToMove = not self.whiteToMove
            if move.piece_Moved == 'wK':
                self.white_King_Location = (move.start_Row, move.start_Col)
            elif move.piece_Moved == 'bK':
                self.black_King_Location = (move.start_Row, move.start_Col)

    def get_Valid_Moves(self):
        moves = self.get_All_Possible_Moves()
        for i in range(len(moves)-1, -1, -1): # when removing from a list go from last to first (backwards)
            self.make_Move(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.in_Check():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undo_Move()
        if len(moves) == 0:
            if self.in_Check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves
    
    def in_Check(self):
        if self.whiteToMove:
            return self.square_Under_Attack(self.white_King_Location[0], self.white_King_Location[1])
        else:
            return self.square_Under_Attack(self.black_King_Location[0], self.black_King_Location[1])

    def square_Under_Attack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        opponent_Moves = self.get_All_Possible_Moves()
        self.whiteToMove = not self.whiteToMove
        for move in opponent_Moves:
            if move.end_Row == r and move.end_Col == c:
                return True
        return False

    def get_All_Possible_Moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def get_Pawn_Moves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))

    def get_Knight_Moves(self, r, c, moves):
        possible_Moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally = 'w' if self.whiteToMove else 'b'
        for m in possible_Moves:
            row = r + m[0]
            col = c + m[1]
            if 0 <= row < 8 and 0 <= col < 8:
                piece = self.board[row][col][0]
                if piece != ally:
                    moves.append(Move((r,c), (row, col), self.board))

    def get_Bishop_Moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                row = r + d[0] * i
                col = c + d[1] * i
                if 0 <= row < 8 and 0 <= col < 8:
                    piece = self.board[row][col][0]
                    if piece == '-':
                        moves.append(Move((r,c), (row, col), self.board))
                    elif piece == enemy:
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_Rook_Moves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                row = r + d[0] * i
                col = c + d[1] * i
                if 0 <= row < 8 and 0 <= col < 8:
                    piece = self.board[row][col][0]
                    if piece == '-':
                        moves.append(Move((r,c), (row, col), self.board))
                    elif piece == enemy:
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_Queen_Moves(self, r, c, moves):
        self.get_Bishop_Moves(r, c, moves)
        self.get_Rook_Moves(r, c, moves)

    def get_King_Moves(self, r, c, moves):
        possible_Moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            row = r + possible_Moves[i][0]
            col = c + possible_Moves[i][1]
            if 0 <= row < 8 and 0 <= col < 8:
                piece = self.board[row][col][0]
                if piece != ally:
                    moves.append(Move((r,c), (row, col), self.board))

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
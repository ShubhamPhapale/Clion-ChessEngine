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
        self.in_Check = False
        self.pins = []
        self.checks = []
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
        moves = []
        self.in_Check, self.pins, self.checks = self.check_For_Pins_And_Checks()
        if self.whiteToMove:
            king_Row = self.white_King_Location[0]
            king_Col = self.white_King_Location[1]
        else:
            king_Row = self.black_King_Location[0]
            king_Col = self.black_King_Location[1]
        if self.in_Check:
            if len(self.checks) == 1:
                moves = self.get_All_Possible_Moves()
                check = self.checks[0]
                check_Row = check[0]
                check_Col = check[1]
                piece_Checking = self.board[check_Row][check_Col]
                valid_Squares = []
                if piece_Checking[1] == 'N':
                    valid_Squares = [(check_Row, check_Col)]
                else:
                    for i in range(1, 8):
                        valid_Square = (king_Row + check[2] * i, king_Col + check[3] * i) 
                        valid_Squares.append(valid_Square)
                        if valid_Square[0] == check_Row and valid_Square[1] == check_Col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_Moved[1] != 'K':
                        if not (moves[i].end_Row, moves[i].end_Col) in valid_Squares:
                            moves.remove(moves[i])
            else:
                self.get_King_Moves(king_Row, king_Col, moves)
        else:
            moves = self.get_All_Possible_Moves()

        if len(moves) == 0:
            if self.in_Check:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def get_All_Possible_Moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def check_For_Pins_And_Checks(self):
        pins = []
        checks = []
        in_Check = False
        if self.whiteToMove:
            enemy = 'b'
            ally = 'w'
            start_Row = self.white_King_Location[0]
            start_Col = self.white_King_Location[1]
        else: 
            enemy = 'w'
            ally = 'b'
            start_Row = self.black_King_Location[0]
            start_Col = self.black_King_Location[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for i in range(len(directions)):
            d = directions[i]
            possible_Pin = ()
            for j in range(1, 8):
                end_Row = start_Row + d[0] * j
                end_Col = start_Col + d[1] * j
                if 0 <= end_Row < 8 and 0 <= end_Col < 8:
                    end_Piece = self.board[end_Row][end_Col]
                    if end_Piece[0] == ally and end_Piece[1] != 'K':
                        if possible_Pin == ():
                            possible_Pin = (end_Row, end_Col, d[0], d[1])
                        else:
                            break
                    elif end_Piece[0] == enemy:
                        piece_Type = end_Piece[1]
                        if (0 <= i < 4 and piece_Type == 'R') or \
                            (4 <= i < 8 and piece_Type == 'B') or \
                            (j == 1 and piece_Type == 'P' and ((enemy == 'w' and 6 <= i < 8) or (enemy == 'b' and 4 <= i < 6))) or \
                            (piece_Type == 'Q') or (j == 1 and piece_Type == 'K'):
                            if possible_Pin == ():
                                in_Check = True
                                checks.append((end_Row, end_Col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_Pin)
                                break
                        else:
                            break
                else:
                    break
        possible_Moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in possible_Moves:
            end_Row = start_Row + m[0]
            end_Col = start_Col + m[1]
            if 0 <= end_Row < 8 and 0 <= end_Col < 8:
                end_Piece = self.board[end_Row][end_Col]
                if end_Piece == enemy and end_Piece[1] == 'N':
                    in_Check = True
                    checks.append((end_Row, end_Col, m[0], m[1]))
        return in_Check, pins, checks

    def get_Pawn_Moves(self, r, c, moves):
        piece_Pinned = False
        pin_Direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_Pinned = True
                pin_Direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                if not piece_Pinned or pin_Direction == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    if not piece_Pinned or pin_Direction == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    if not piece_Pinned or pin_Direction == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+1), self.board))
        
        else:
            if self.board[r+1][c] == "--":
                if not piece_Pinned or pin_Direction == (1, 0):
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r, c), (r+2, c), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    if not piece_Pinned or pin_Direction == (1, 1):
                        moves.append(Move((r, c), (r+1, c+1), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    if not piece_Pinned or pin_Direction == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board))

    def get_Knight_Moves(self, r, c, moves):
        piece_Pinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_Pinned = True
                self.pins.remove(self.pins[i])
                break

        possible_Moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally = 'w' if self.whiteToMove else 'b'
        for m in possible_Moves:
            row = r + m[0]
            col = c + m[1]
            if 0 <= row < 8 and 0 <= col < 8:
                if not piece_Pinned:
                    piece = self.board[row][col][0]
                    if piece != ally:
                        moves.append(Move((r,c), (row, col), self.board))

    def get_Bishop_Moves(self, r, c, moves):
        piece_Pinned = False
        pin_Direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_Pinned = True
                pin_Direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                row = r + d[0] * i
                col = c + d[1] * i
                if 0 <= row < 8 and 0 <= col < 8:
                    if not piece_Pinned or pin_Direction == d or pin_Direction == (-d[0], -d[1]):
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
        piece_Pinned = False
        pin_Direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_Pinned = True
                pin_Direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                row = r + d[0] * i
                col = c + d[1] * i
                if 0 <= row < 8 and 0 <= col < 8:
                    if not piece_Pinned or pin_Direction == d or pin_Direction == (-d[0], -d[1]):
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
        row_Moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_Moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            row = r + row_Moves[i]
            col = c + col_Moves[i]
            if 0 <= row < 8 and 0 <= col < 8:
                piece = self.board[row][col][0]
                if piece != ally:
                    if ally == 'w':
                        self.white_King_Location = (row, col)
                    else:
                        self.black_King_Location = (row, col)
                    in_Check, pins, checks = self.check_For_Pins_And_Checks()
                    if not in_Check:
                        moves.append(Move((r,c), (row, col), self.board))
                    if ally == 'w':
                        self.white_King_Location = (r, c)
                    else:
                        self.black_King_Location = (r, c)


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
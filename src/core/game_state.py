from .move import Move
from .castle_rights import CastleRights
from utils.fen import board_to_fen

class GameState:
    """
    Class that stores the current state of a chess game.
    This includes the board, whose turn it is, castling rights, etc.
    """
    def __init__(self):
        """Initialize the game state."""
        # Board is an 8x8 2d list
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
        self.move_functions = {
            'P': self.get_pawn_moves,
            'R': self.get_rook_moves,
            'N': self.get_knight_moves,
            'B': self.get_bishop_moves,
            'Q': self.get_queen_moves,
            'K': self.get_king_moves
        }
        self.whiteToMove = True
        self.moveLog = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []
        self.enpassant_possible = ()
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castling_right = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(
            self.current_castling_right.wks,
            self.current_castling_right.wqs,
            self.current_castling_right.bks,
            self.current_castling_right.bqs
        )]
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.board_state_count = {}
        self.add_board_state()

    def make_move(self, move):
        """Execute a move on the board."""
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        # Update king location
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        # Pawn promotion
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'

        # En passant
        if move.is_en_passant:
            self.board[move.start_row][move.end_col] = "--"

        # Update enpassant_possible
        if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_possible = ()
        self.enpassant_possible_log.append(self.enpassant_possible)

        # Castle move
        if move.is_castle:
            if move.end_col - move.start_col == 2:  # Kingside castle
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = "--"
            else:  # Queenside castle
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = "--"

        # Update castling rights
        self.update_castle_rights(move)
        self.castle_rights_log.append(CastleRights(
            self.current_castling_right.wks,
            self.current_castling_right.wqs,
            self.current_castling_right.bks,
            self.current_castling_right.bqs
        ))

        # Update 50-move rule counters
        if move.piece_moved[1] == 'P' or move.piece_captured != "--":
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # Update fullmove number after black's move
        if not self.whiteToMove:
            self.fullmove_number += 1

        # Update threefold repetition counter
        self.add_board_state()

    def undo_move(self):
        """Undo the last move made."""
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.whiteToMove = not self.whiteToMove

            # Update king location
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)

            # Undo en passant
            if move.is_en_passant:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = move.piece_captured

            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]

            # Undo castling rights
            self.castle_rights_log.pop()
            self.current_castling_right = self.castle_rights_log[-1]

            # Undo castle move
            if move.is_castle:
                if move.end_col - move.start_col == 2:  # Kingside
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = "--"
                else:  # Queenside
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"

            # Update 50-move rule counters
            if move.piece_moved[1] == 'P' or move.piece_captured != "--":
                self.halfmove_clock = move.previous_halfmove_clock
            else:
                self.halfmove_clock -= 1

            # Update fullmove number after undoing black's move
            if self.whiteToMove:
                self.fullmove_number -= 1

            # Update threefold repetition counter
            self.remove_board_state()

    def update_castle_rights(self, move):
        """Update castling rights given the move."""
        if move.piece_captured == "wR":
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castling_right.wqs = False
                elif move.end_col == 7:
                    self.current_castling_right.wks = False
        elif move.piece_captured == "bR":
            if move.end_row == 0:
                if move.end_col == 0:
                    self.current_castling_right.bqs = False
                elif move.end_col == 7:
                    self.current_castling_right.bks = False

        if move.piece_moved == 'wK':
            self.current_castling_right.wks = False
            self.current_castling_right.wqs = False
        elif move.piece_moved == 'bK':
            self.current_castling_right.bks = False
            self.current_castling_right.bqs = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:
                    self.current_castling_right.wqs = False
                elif move.start_col == 7:
                    self.current_castling_right.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:
                    self.current_castling_right.bqs = False
                elif move.start_col == 7:
                    self.current_castling_right.bks = False

    def add_board_state(self):
        """Add current board state to repetition counter."""
        fen = self.board_to_fen(for_repetition=True)
        self.board_state_count[fen] = self.board_state_count.get(fen, 0) + 1

    def remove_board_state(self):
        """Remove current board state from repetition counter."""
        fen = self.board_to_fen(for_repetition=True)
        if fen in self.board_state_count:
            self.board_state_count[fen] -= 1
            if self.board_state_count[fen] == 0:
                del self.board_state_count[fen]

    def is_threefold_repetition(self):
        """Check if the current position has occurred three times."""
        fen = self.board_to_fen(for_repetition=True)
        return self.board_state_count.get(fen, 0) >= 3

    def is_fifty_move_rule(self):
        """Check if fifty moves have been made without a pawn move or capture."""
        return self.halfmove_clock >= 100  # 50 moves = 100 half moves

    def board_to_fen(self, for_repetition=False):
        """Convert the current board state to FEN notation."""
        return board_to_fen(
            self.board,
            self.whiteToMove,
            self.current_castling_right,
            self.enpassant_possible,
            self.halfmove_clock,
            self.fullmove_number,
            for_repetition
        )

    def get_valid_moves(self):
        """Get all valid moves considering checks and pins."""
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()

        if self.whiteToMove:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]

        if self.in_check:
            if len(self.checks) == 1:  # Only 1 check, block or move king
                moves = self.get_all_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []  # Squares that pieces can move to
                if piece_checking[1] == 'N':  # Knight check: must capture knight or move king
                    valid_squares = [(check_row, check_col)]
                else:  # Other pieces: can block or capture
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i,
                                      king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                # Remove moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':  # Move doesn't move king so it must block or capture
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:  # Double check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else:  # Not in check - all moves are fine
            moves = self.get_all_possible_moves()
            if self.whiteToMove:
                self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves, 'w')
            else:
                self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves, 'b')

        if len(moves) == 0:
            if self.in_check:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def check_for_pins_and_checks(self):
        """
        Returns if the player is in check, a list of pins, and a list of checks
        """
        pins = []  # Squares pinned and the direction its pinned from
        checks = []  # Squares where enemy is applying a check
        in_check = False
        if self.whiteToMove:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        # Check outwards from king for pins and checks, keep track of pins
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1),
                     (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()  # Reset possible pins
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():  # First allied piece could be pinned
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:  # Second allied piece - no check or pin from this direction
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        if (0 <= j <= 3 and enemy_type == 'R') or \
                                (4 <= j <= 7 and enemy_type == 'B') or \
                                (i == 1 and enemy_type == 'P' and ((enemy_color == 'w' and 6 <= j <= 7) or
                                                                  (enemy_color == 'b' and 4 <= j <= 5))) or \
                                (enemy_type == 'Q') or (i == 1 and enemy_type == 'K'):
                            if possible_pin == ():  # No piece blocking, so check
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:  # Piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # Enemy piece not applying check
                            break
                else:
                    break  # Off board
        # Check for knight checks
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':  # Enemy knight attacking a king
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks

    def get_all_possible_moves(self):
        """Get all possible moves without considering checks."""
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        """Get all the pawn moves for the pawn located at row, col and add the moves to the list."""
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            move_amount = -1
            start_row = 6
            enemy_color = 'b'
            king_row, king_col = self.white_king_location
        else:
            move_amount = 1
            start_row = 1
            enemy_color = 'w'
            king_row, king_col = self.black_king_location

        if self.board[row + move_amount][col] == "--":  # 1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((row, col), (row + move_amount, col), self.board, self.halfmove_clock))
                if row == start_row and self.board[row + 2 * move_amount][col] == "--":  # 2 square pawn advance
                    moves.append(Move((row, col), (row + 2 * move_amount, col), self.board, self.halfmove_clock))

        if col - 1 >= 0:  # Capture to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[row + move_amount][col - 1][0] == enemy_color:
                    moves.append(Move((row, col), (row + move_amount, col - 1), self.board, self.halfmove_clock))
                if (row + move_amount, col - 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:  # King is left of the pawn
                            inside_range = range(king_col + 1, col - 1)
                            outside_range = range(col + 1, 8)
                        else:  # King right of the pawn
                            inside_range = range(king_col - 1, col, -1)
                            outside_range = range(col - 2, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":  # Some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col), (row + move_amount, col - 1), self.board, self.halfmove_clock, en_passant=True))

        if col + 1 <= 7:  # Capture to the right
            if not piece_pinned or pin_direction == (move_amount, 1):
                if self.board[row + move_amount][col + 1][0] == enemy_color:
                    moves.append(Move((row, col), (row + move_amount, col + 1), self.board, self.halfmove_clock))
                if (row + move_amount, col + 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:  # King is left of the pawn
                            inside_range = range(king_col + 1, col)
                            outside_range = range(col + 2, 8)
                        else:  # King right of the pawn
                            inside_range = range(king_col - 1, col + 1, -1)
                            outside_range = range(col - 1, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":  # Some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col), (row + move_amount, col + 1), self.board, self.halfmove_clock, en_passant=True))

    def get_rook_moves(self, row, col, moves):
        """Get all the rook moves for the rook located at row, col and add the moves to the list."""
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q':  # Can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Up, left, down, right
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # Check if the move is on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # Empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board, self.halfmove_clock))
                        elif end_piece[0] == enemy_color:  # Capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board, self.halfmove_clock))
                            break
                        else:  # Friendly piece
                            break
                else:  # Off board
                    break

    def get_knight_moves(self, row, col, moves):
        """Get all the knight moves for the knight located at row, col and add the moves to the list."""
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = "w" if self.whiteToMove else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:  # Not an ally piece - empty or enemy
                        moves.append(Move((row, col), (end_row, end_col), self.board, self.halfmove_clock))

    def get_bishop_moves(self, row, col, moves):
        """Get all the bishop moves for the bishop located at row, col and add the moves to the list."""
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # Diagonals
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # Check if the move is on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # Empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board, self.halfmove_clock))
                        elif end_piece[0] == enemy_color:  # Capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board, self.halfmove_clock))
                            break
                        else:  # Friendly piece
                            break
                else:  # Off board
                    break

    def get_queen_moves(self, row, col, moves):
        """Get all the queen moves for the queen located at row, col and add the moves to the list."""
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        """Get all the king moves for the king located at row, col and add the moves to the list."""
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.whiteToMove else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # Not an ally piece - empty or enemy
                    # Place king on end square and check for checks
                    if ally_color == 'w':
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board, self.halfmove_clock))
                    # Place king back on original location
                    if ally_color == 'w':
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)

    def get_castle_moves(self, row, col, moves, ally_color):
        """Generate all valid castle moves for the king at (row, col) and add them to the list of moves."""
        if self.square_under_attack(row, col, ally_color):
            return  # Can't castle while in check
        if (self.whiteToMove and self.current_castling_right.wks) or \
           (not self.whiteToMove and self.current_castling_right.bks):
            self.get_kingside_castle_moves(row, col, moves, ally_color)
        if (self.whiteToMove and self.current_castling_right.wqs) or \
           (not self.whiteToMove and self.current_castling_right.bqs):
            self.get_queenside_castle_moves(row, col, moves, ally_color)

    def get_kingside_castle_moves(self, row, col, moves, ally_color):
        """Generate kingside castle moves for the king at (row, col)."""
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
            if not self.square_under_attack(row, col + 1, ally_color) and \
               not self.square_under_attack(row, col + 2, ally_color):
                moves.append(Move((row, col), (row, col + 2), self.board, self.halfmove_clock, castle=True))

    def get_queenside_castle_moves(self, row, col, moves, ally_color):
        """Generate queenside castle moves for the king at (row, col)."""
        if self.board[row][col - 1] == '--' and \
           self.board[row][col - 2] == '--' and \
           self.board[row][col - 3] == '--':
            if not self.square_under_attack(row, col - 1, ally_color) and \
               not self.square_under_attack(row, col - 2, ally_color):
                moves.append(Move((row, col), (row, col - 2), self.board, self.halfmove_clock, castle=True))

    def square_under_attack(self, row, col, ally_color):
        """Determine if enemy can attack the square row, col."""
        enemy_color = 'w' if ally_color == 'b' else 'b'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1),
                     (-1, -1), (-1, 1), (1, -1), (1, 1))
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color:  # Blocked by friendly piece
                        break
                    elif end_piece[0] == enemy_color:
                        piece_type = end_piece[1]
                        if (0 <= i <= 1 and piece_type == 'K') or \
                           (direction in ((-1, -1), (-1, 1), (1, -1), (1, 1)) and piece_type == 'B') or \
                           (direction in ((-1, 0), (0, -1), (1, 0), (0, 1)) and piece_type == 'R') or \
                           (i == 1 and piece_type == 'P' and
                            ((enemy_color == 'w' and direction in ((1, -1), (1, 1))) or
                             (enemy_color == 'b' and direction in ((-1, -1), (-1, 1))))) or \
                           (piece_type == 'Q'):
                            return True
                        else:  # Enemy piece not applying check
                            break
                else:  # Off board
                    break
        # Check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    return True
        return False 
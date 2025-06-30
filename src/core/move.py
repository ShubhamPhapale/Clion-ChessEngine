class Move:
    """Represents a chess move with all its properties and notations."""
    
    # Mappings for chess notation
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board, halfmove_clock, en_passant=False, pawn_promotion=False, castle=False):
        """Initialize a move with start and end positions and additional properties."""
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        
        # Special move flags
        self.is_pawn_promotion = pawn_promotion
        self.is_en_passant = en_passant
        if self.is_en_passant:
            self.piece_captured = 'bP' if self.piece_moved == 'wP' else 'wP'
        
        self.is_castle = castle
        self.is_capture = self.piece_captured != "--"
        
        # For undoing moves
        self.previous_halfmove_clock = halfmove_clock

    def __eq__(self, other):
        """Override the equals method to compare moves."""
        if isinstance(other, Move):
            return (self.start_row == other.start_row and 
                    self.start_col == other.start_col and 
                    self.end_row == other.end_row and 
                    self.end_col == other.end_col)
        return False

    def get_chess_notation(self):
        """Get the move in chess notation (e.g., 'e2e4')."""
        return self.get_rank_files(self.start_row, self.start_col) + self.get_rank_files(self.end_row, self.end_col)

    def get_rank_files(self, row, col):
        """Convert row and column numbers to chess notation (e.g., 'e2')."""
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __str__(self):
        """String representation of the move."""
        if self.is_castle:
            return "O-O" if self.end_col == 6 else "O-O-O"
        
        end_square = self.get_rank_files(self.end_row, self.end_col)
        if self.piece_moved[1] == 'P':
            if self.is_capture:
                return self.cols_to_files[self.start_col] + "x" + end_square
            return end_square
            
        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square 
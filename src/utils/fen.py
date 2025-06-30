def board_to_fen(board, white_to_move, castle_rights, en_passant_target, halfmove_clock, fullmove_number, for_repetition=False):
    """Convert the current board state to FEN notation.
    
    Args:
        board: 2D list representing the chess board
        white_to_move: Boolean indicating if it's white's turn
        castle_rights: CastleRights object
        en_passant_target: Tuple of row, col for en passant target square
        halfmove_clock: Number of halfmoves since last pawn advance or capture
        fullmove_number: The number of the full moves in the game
        for_repetition: If True, only return the piece placement part
    
    Returns:
        String in FEN notation
    """
    # 1. Piece placement
    empty = 0
    fen = ""
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == "--":
                empty += 1
            else:
                if empty > 0:
                    fen += str(empty)
                    empty = 0
                fen += piece[1].upper() if piece[0] == 'w' else piece[1].lower()
        if empty > 0:
            fen += str(empty)
            empty = 0
        if row < 7:
            fen += "/"
    
    if for_repetition:
        return fen
    
    # 2. Active color
    fen += " w " if white_to_move else " b "
    
    # 3. Castling availability
    fen += str(castle_rights) + " "
    
    # 4. En passant target square
    if en_passant_target:
        file = 'abcdefgh'[en_passant_target[1]]
        rank = '87654321'[en_passant_target[0]]
        fen += file + rank
    else:
        fen += "-"
    
    # 5. Halfmove clock
    fen += f" {halfmove_clock}"
    
    # 6. Fullmove number
    fen += f" {fullmove_number}"
    
    return fen 
class CastleRights:
    """Represents castling rights for both players."""
    
    def __init__(self, wks, wqs, bks, bqs):
        """Initialize castling rights for both players.
        
        Args:
            wks: White kingside castling right
            wqs: White queenside castling right
            bks: Black kingside castling right
            bqs: Black queenside castling right
        """
        self.wks = wks  # White king side
        self.wqs = wqs  # White queen side
        self.bks = bks  # Black king side
        self.bqs = bqs  # Black queen side
    
    def __str__(self):
        """String representation of castling rights in FEN format."""
        rights = ""
        if self.wks: rights += "K"
        if self.wqs: rights += "Q"
        if self.bks: rights += "k"
        if self.bqs: rights += "q"
        return rights if rights else "-" 
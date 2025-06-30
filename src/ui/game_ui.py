import pygame
from core.game_state import GameState
from core.move import Move
from utils.constants import BOARD_WIDTH, BOARD_HEIGHT, DIMENSION, SQ_SIZE, MAX_FPS, IMAGES

class GameUI:
    """
    The main driver for our game. This will handle user input and updating the graphics.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        pygame.display.set_caption('Chess')
        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.valid_moves = self.game_state.get_valid_moves()
        self.move_made = False  # Flag variable for when a move is made
        self.animate = False  # Flag variable for when we should animate a move
        self.game_over = False
        self.sq_selected = ()  # No square is selected initially, keeps track of last click of the user (tuple: (row,col))
        self.player_clicks = []  # Keeps track of player clicks (two tuples: [(6,4), (4,4)])
        self.load_images()

    def load_images(self):
        """
        Initialize a global dictionary of images. This will be called exactly once in the main.
        """
        pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            IMAGES[piece] = pygame.transform.scale(
                pygame.image.load(f"img/{piece}.png"), (SQ_SIZE, SQ_SIZE))

    def draw_game_state(self, selected_square=None):
        """
        Responsible for all the graphics within current game state.
        """
        self.draw_board()  # Draw squares on the board
        self.highlight_squares(selected_square)  # Add piece highlighting or move suggestions
        self.draw_pieces()  # Draw pieces on top of those squares

    def draw_board(self):
        """
        Draw the squares on the board.
        """
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = colors[((row + col) % 2)]
                pygame.draw.rect(self.screen, color,
                               pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def highlight_squares(self, selected_square):
        """
        Highlight selected square and possible moves for the selected piece.
        """
        if selected_square != () and selected_square is not None:
            row, col = selected_square
            if self.game_state.board[row][col][0] == ('w' if self.game_state.whiteToMove else 'b'):
                # Highlight selected square
                s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)  # Transparency value -> 0 transparent; 255 opaque
                s.fill(pygame.Color('blue'))
                self.screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
                # Highlight moves from that square
                s.fill(pygame.Color('yellow'))
                for move in self.valid_moves:
                    if move.start_row == row and move.start_col == col:
                        self.screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))

    def draw_pieces(self):
        """
        Draw the pieces on the board using the current game_state.board
        """
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece = self.game_state.board[row][col]
                if piece != "--":  # Not empty square
                    self.screen.blit(IMAGES[piece],
                                   pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def animate_move(self, move, fps):
        """
        Animating a move
        """
        colors = [pygame.Color("white"), pygame.Color("gray")]
        d_row = move.end_row - move.start_row
        d_col = move.end_col - move.start_col
        frames_per_square = 10  # frames to move one square
        frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
        for frame in range(frame_count + 1):
            row, col = (move.start_row + d_row * frame / frame_count,
                       move.start_col + d_col * frame / frame_count)
            self.draw_board()
            self.draw_pieces()
            # Erase the piece moved from its ending square
            color = colors[(move.end_row + move.end_col) % 2]
            end_square = pygame.Rect(move.end_col * SQ_SIZE,
                                   move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(self.screen, color, end_square)
            # Draw captured piece onto rectangle
            if move.piece_captured != '--':
                if move.is_en_passant:
                    en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                    end_square = pygame.Rect(move.end_col * SQ_SIZE,
                                           en_passant_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                self.screen.blit(IMAGES[move.piece_captured], end_square)
            # Draw moving piece
            if move.piece_moved != '--':
                self.screen.blit(IMAGES[move.piece_moved],
                               pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            pygame.display.flip()
            self.clock.tick(fps)

    def handle_click(self, location):
        """
        Handle mouse clicks (location is (row, col))
        """
        if not self.game_over:
            row = location[0]
            col = location[1]
            # If the same square is selected twice, unselect everything
            if self.sq_selected == (row, col) or col >= 8:
                self.sq_selected = ()
                self.player_clicks = []
            else:
                self.sq_selected = (row, col)
                self.player_clicks.append(self.sq_selected)
            # After 2nd click
            if len(self.player_clicks) == 2:
                move = Move(self.player_clicks[0], self.player_clicks[1], self.game_state.board, self.game_state.halfmove_clock)
                for i in range(len(self.valid_moves)):
                    if move == self.valid_moves[i]:
                        self.game_state.make_move(self.valid_moves[i])
                        self.move_made = True
                        self.animate = True
                        self.sq_selected = ()
                        self.player_clicks = []
                if not self.move_made:
                    self.player_clicks = [self.sq_selected]

    def reset_game(self):
        """
        Reset the game state
        """
        self.game_state = GameState()
        self.valid_moves = self.game_state.get_valid_moves()
        self.sq_selected = ()
        self.player_clicks = []
        self.move_made = False
        self.animate = False
        self.game_over = False 
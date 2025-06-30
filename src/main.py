import pygame
from ui.game_ui import GameUI
from ai.engine import find_random_move, find_best_move
from utils.constants import MAX_FPS, SQ_SIZE, BOARD_WIDTH, BOARD_HEIGHT

def main():
    """
    The main driver for our chess game.
    This will handle user input and updating the graphics.
    """
    game_ui = GameUI()
    running = True
    player_one = True  # If a human is playing white, this will be True. If an AI is playing, False
    player_two = False  # Same as above but for black
    
    while running:
        human_turn = (game_ui.game_state.whiteToMove and player_one) or (not game_ui.game_state.whiteToMove and player_two)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Mouse handler
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_ui.game_over and human_turn:
                    location = pygame.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    game_ui.handle_click((row, col))
                    
            # Key handler
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # Undo when 'z' is pressed
                    game_ui.game_state.undo_move()
                    game_ui.move_made = True
                    game_ui.animate = False
                    game_ui.game_over = False
                if event.key == pygame.K_r:  # Reset the game when 'r' is pressed
                    game_ui.reset_game()
                    game_ui.game_over = False
        
        # AI move finder
        if not game_ui.game_over and not human_turn:
            ai_move = find_best_move(game_ui.game_state, game_ui.valid_moves)
            if ai_move is None:
                ai_move = find_random_move(game_ui.valid_moves)
            game_ui.game_state.make_move(ai_move)
            game_ui.move_made = True
            game_ui.animate = True

        if game_ui.move_made:
            if game_ui.animate:
                game_ui.animate_move(game_ui.game_state.moveLog[-1], MAX_FPS)
            game_ui.valid_moves = game_ui.game_state.get_valid_moves()
            game_ui.move_made = False
            game_ui.animate = False

        game_ui.draw_game_state(game_ui.sq_selected)
        
        if game_ui.game_state.checkmate:
            game_ui.game_over = True
            if game_ui.game_state.whiteToMove:
                draw_text(game_ui.screen, "Black wins by checkmate!")
            else:
                draw_text(game_ui.screen, "White wins by checkmate!")
        elif game_ui.game_state.stalemate:
            game_ui.game_over = True
            draw_text(game_ui.screen, "Stalemate!")
        elif game_ui.game_state.is_threefold_repetition():
            game_ui.game_over = True
            draw_text(game_ui.screen, "Draw by threefold repetition!")
        elif game_ui.game_state.is_fifty_move_rule():
            game_ui.game_over = True
            draw_text(game_ui.screen, "Draw by fifty-move rule!")

        pygame.display.flip()
        game_ui.clock.tick(MAX_FPS)

def draw_text(screen, text):
    """
    Draw text in the middle of the screen
    """
    font = pygame.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, pygame.Color("Black"))
    text_location = pygame.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH/2 - text_object.get_width()/2,
        BOARD_HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, pygame.Color('Gray'))
    screen.blit(text_object, text_location.move(2, 2))

if __name__ == "__main__":
    main()
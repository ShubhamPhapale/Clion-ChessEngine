import pygame as p
import math
import ChessEngine, ChessAI
from multiprocessing import Process, Queue
# import multiprocessing

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 256
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
EVAL_BAR_WIDTH = 32
EVAL_BAR_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

scroll_offset = 0
scroll_step = 4
SCROLL_SPEED = 20

def load_Images():
    pieces = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("img/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

def main():
    p.init()

    # manager = multiprocessing.Manager() # multiprocessing.Manager()
    # transposition_table = manager.dict()

    screen = p.display.set_mode((+ EVAL_BAR_WIDTH + BOARD_WIDTH  + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    move_Log_Font = p.font.SysFont("Arial", 16, True, False)
    gs = ChessEngine.Gamestate()
    valid_Moves = gs.get_Valid_Moves()
    move_Made = False
    animate = False
    load_Images()
    running = True
    square_Selected = ()
    player_Clicks = []
    game_Over = False
    white_Player = True
    black_Player = True
    AI_Thinking = False
    move_Finder_Process = None
    move_Undone = False

    while running: 
        human_Turn = (gs.whiteToMove and white_Player) or (not gs.whiteToMove and black_Player)
        for  e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_Over:
                    location = p.mouse.get_pos()
                    col = (location[0] - EVAL_BAR_WIDTH) // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_Selected == (row, col) or col > 7:
                        square_Selected = ()
                        player_Clicks = []
                    else:
                        square_Selected = (row, col)
                        player_Clicks.append(square_Selected)
                    if len(player_Clicks) == 2  and human_Turn:
                        move = ChessEngine.Move(player_Clicks[0], player_Clicks[1], gs.board)
                        for i in range(len(valid_Moves)):
                            if move == valid_Moves[i]:
                                gs.make_Move(valid_Moves[i])
                                move_Made = True
                                animate = True
                                square_Selected = ()
                                player_Clicks = []
                        if not move_Made:
                            player_Clicks = [square_Selected]
            
                handle_move_log_scroll(e)

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_Move()
                    move_Made = True
                    animate = False
                    game_Over = False
                    if AI_Thinking:
                        move_Finder_Process.terminate()
                        AI_Thinking = False
                    move_Undone = True
                if e.key == p.K_r:
                    gs = ChessEngine.Gamestate()
                    valid_Moves = gs.get_Valid_Moves()
                    square_Selected = ()
                    player_Clicks = []
                    move_Made = False
                    animate = False
                    game_Over = False
                    if AI_Thinking:
                        move_Finder_Process.terminate()
                        AI_Thinking = False
                    move_Undone = True

        if not game_Over and not human_Turn and not move_Made and not move_Undone:
            if not AI_Thinking:
                AI_Thinking = True
                return_Queue = Queue()
                move_Finder_Process = Process(target = ChessAI.find_Best_Move, args = (gs, valid_Moves, return_Queue)) # , transposition_table
                move_Finder_Process.start()
                # move_Finder_Process.join()

            if not move_Finder_Process.is_alive():  
                AI_Move = return_Queue.get()
                if AI_Move is None:
                    AI_Move = ChessAI.find_Random_Move(valid_Moves)
                gs.make_Move(AI_Move)
                move_Made = True
                animate = True
                AI_Thinking = False

        if move_Made:
            if animate:
                animate_Move(gs.moveLog[-1], screen, gs.board, clock)
                print("Move made:", str(gs.moveLog[-1]))
            valid_Moves = gs.get_Valid_Moves()
            move_Made = False
            animate = False
            move_Undone = False

        eval_Score = ChessAI.score_Board(gs)
        draw_Game_State(screen, gs, valid_Moves, square_Selected, move_Log_Font, eval_Score)

        if gs.checkmate or gs.stalemate:
            game_Over = True
            text = "Stalemate" if gs.stalemate else "Black Wins By Checkmate" if gs.whiteToMove else "White Wins By Checkmate"
            draw_Game_Ended_Text(screen, text)

        clock.tick(MAX_FPS)
        p.display.flip()

def draw_Game_State(screen, gs, valid_Moves, square_Selected, move_Log_Font, eval_Score):
    draw_Board(screen)
    highlight_Squares(screen, gs, valid_Moves, square_Selected)
    draw_Pieces(screen, gs.board)
    draw_Evaluation_Bar(screen, eval_Score)
    draw_Move_Log(screen, gs, move_Log_Font)

def draw_Board(screen):
    global colors 
    colors = [p.Color("light gray"), (153,102,51)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(EVAL_BAR_WIDTH + c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlight_Squares(screen, gs, valid_Moves, square_Selected):
    if square_Selected != ():
        r, c = square_Selected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (EVAL_BAR_WIDTH + c * SQUARE_SIZE, r * SQUARE_SIZE))
            s.fill(p.Color("yellow"))
            for move in valid_Moves:
                if move.start_Row == r and move.start_Col == c:
                    screen.blit(s, (EVAL_BAR_WIDTH + move.end_Col * SQUARE_SIZE, move.end_Row * SQUARE_SIZE))

def draw_Pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(EVAL_BAR_WIDTH + c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_Move_Log(screen, gs, font):
    global scroll_offset
    move_Log_Rect = p.Rect(BOARD_WIDTH + EVAL_BAR_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, (51, 34, 17), move_Log_Rect)
    moveLog = gs.moveLog
    move_Texts = []
    for i in range(0, len(moveLog), 2):
        initial_part = str(i // 2 + 1) + "."
        white_move = str(moveLog[i])
        black_move =str(moveLog[i+1]) if i + 1 < len(moveLog) else ""
        move_Texts.append((initial_part, white_move, black_move))
    
    padding = 2
    line_Spacing = 2
    text_Y = padding + line_Spacing - scroll_offset
    total_Text_Height = 0

    initial_Part_Width = 32
    move_Part_Width = 112

    for initial_part, white_move, black_move in move_Texts:
        initial_part_text = font.render(initial_part, True, p.Color("white"))
        white_move_text = font.render(white_move, True, p.Color("white"))
        black_move_text = font.render(black_move, True, p.Color("white"))
        
        initial_part_location = move_Log_Rect.move(padding + line_Spacing, text_Y)
        white_move_location = move_Log_Rect.move(padding + line_Spacing + initial_Part_Width, text_Y)
        black_move_location = move_Log_Rect.move(padding + line_Spacing + initial_Part_Width + move_Part_Width, text_Y)
        
        screen.blit(initial_part_text, initial_part_location)
        screen.blit(white_move_text, white_move_location)
        screen.blit(black_move_text, black_move_location)
        
        text_Y += initial_part_text.get_height() + line_Spacing
        total_Text_Height += initial_part_text.get_height() + line_Spacing

    max_scroll_offset = max(0, total_Text_Height - MOVE_LOG_PANEL_HEIGHT)
    scroll_offset = min(scroll_offset, max_scroll_offset)

    scrollEVAL_BAR_WIDTH = 10

    if total_Text_Height > MOVE_LOG_PANEL_HEIGHT:
        scrollEVAL_BAR_HEIGHT = int(MOVE_LOG_PANEL_HEIGHT * (MOVE_LOG_PANEL_HEIGHT / total_Text_Height))
        scrollbar_position = int((MOVE_LOG_PANEL_HEIGHT - scrollEVAL_BAR_HEIGHT) * (scroll_offset / max_scroll_offset))
        scrollbar_rect = p.Rect(BOARD_WIDTH + EVAL_BAR_WIDTH + MOVE_LOG_PANEL_WIDTH - padding - scrollEVAL_BAR_WIDTH, scrollbar_position, scrollEVAL_BAR_WIDTH, scrollEVAL_BAR_HEIGHT)
        p.draw.rect(screen, (87,80,77), scrollbar_rect)

        mouse_x, mouse_y = p.mouse.get_pos()
        scrollbar_area = p.Rect(BOARD_WIDTH + EVAL_BAR_WIDTH + MOVE_LOG_PANEL_WIDTH - padding - scrollEVAL_BAR_WIDTH, 0, scrollEVAL_BAR_WIDTH, MOVE_LOG_PANEL_HEIGHT)
        
        if p.mouse.get_pressed()[0]:  
            if scrollbar_area.collidepoint(mouse_x, mouse_y):
                delta_y = mouse_y - scrollbar_position
                scroll_offset += int(delta_y / scrollEVAL_BAR_HEIGHT * max_scroll_offset)
        
        scroll_offset = max(0, min(scroll_offset, max_scroll_offset))

def animate_Move(move, screen, board, clock):
    global colors
    dR = move.end_Row - move.start_Row
    dC = move.end_Col - move.start_Col
    frames_Per_Second = 6
    frame_Count = (abs(dR) + abs(dC)) * frames_Per_Second
    for frame in range(frame_Count + 1):
        r, c = (move.start_Row + dR * frame / frame_Count , move.start_Col + dC * frame / frame_Count)
        draw_Board(screen)
        draw_Pieces(screen, board)
        color = colors[(move.end_Row + move.end_Col) % 2]
        end_Square = p.Rect(EVAL_BAR_WIDTH + move.end_Col * SQUARE_SIZE, move.end_Row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_Square)
        if move.piece_Captured != "--":
            if move.en_Passant:
                en_Passant_Row = move.end_Row + 1 if move.piece_Captured[0] == 'b' else move.end_Row - 1
                end_Square = p.Rect(EVAL_BAR_WIDTH + move.end_Col * SQUARE_SIZE, en_Passant_Row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_Captured], end_Square)
        if move.piece_Moved != "--":
            screen.blit(IMAGES[move.piece_Moved], p.Rect(EVAL_BAR_WIDTH + c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)

def draw_Game_Ended_Text(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    text_Object = font.render(text, 0, p.Color("Gray"))
    text_Location = p.Rect(EVAL_BAR_WIDTH, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_Object.get_width() / 2, BOARD_HEIGHT / 2 - text_Object.get_height() / 2)
    screen.blit(text_Object, text_Location)
    text_Object = font.render(text, 0, p.Color("Black"))
    screen.blit(text_Object, text_Location.move(2, 2))

def draw_Evaluation_Bar(screen, eval_score):
    max_score = 20  
    eval_score_log = math.log1p(abs(1e-9 + eval_score)) # log1p(x) = log(1 + x)
    sign = 1 if eval_score >= 0 else -1
    
    white_part = EVAL_BAR_HEIGHT / 2 + sign * (eval_score_log / math.log2(math.e * max_score)) * (EVAL_BAR_HEIGHT)
    black_part = EVAL_BAR_HEIGHT - white_part
 
    white_rect = p.Rect(0, black_part, EVAL_BAR_WIDTH, white_part)
    p.draw.rect(screen, p.Color("white"), white_rect)
 
    black_rect = p.Rect(0, 0, EVAL_BAR_WIDTH, black_part)
    p.draw.rect(screen, p.Color("black"), black_rect)

    font = p.font.Font(None, 22)
    color, y_co, eval_score = (p.Color("black"), EVAL_BAR_HEIGHT - 10, eval_score) if eval_score >= 0 else (p.Color("white"), 10, -eval_score)
    text = font.render('M', True, color) if abs(eval_score) > max_score else font.render(f"{eval_score:.1f}", True, color)
    text_rect = text.get_rect(center=(EVAL_BAR_WIDTH // 2, y_co))
    screen.blit(text, text_rect)

def handle_move_log_scroll(event):
    global scroll_offset
    if event.button == 4: 
        scroll_offset = max(0, scroll_offset - scroll_step)
    elif event.button == 5:  
        scroll_offset += scroll_step

if __name__ == "__main__":
    main()
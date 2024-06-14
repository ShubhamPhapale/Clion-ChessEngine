import pygame as p;
import ChessEngine, ChessAI

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_Images():
    pieces = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("img/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
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

    while running: 
        human_Turn = (gs.whiteToMove and white_Player) or (not gs.whiteToMove and black_Player)
        for  e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_Over and human_Turn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_Selected == (row, col):
                        square_Selected = ()
                        player_Clicks = []
                    else:
                        square_Selected = (row, col)
                        player_Clicks.append(square_Selected)
                    if len(player_Clicks) == 2:
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
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_Move()
                    move_Made = True
                    animate = False
                    game_Over = False
                if e.key == p.K_r:
                    gs = ChessEngine.Gamestate()
                    valid_Moves = gs.get_Valid_Moves()
                    square_Selected = ()
                    player_Clicks = []
                    move_Made = False
                    animate = False
                    game_Over = False

        if not game_Over and not human_Turn and not move_Made:
            AI_Move = ChessAI.find_Best_Move(gs, valid_Moves)
            if AI_Move is None:
                AI_Move = ChessAI.find_Random_Move(valid_Moves)
            gs.make_Move(AI_Move)
            move_Made = True
            animate = True

        if move_Made:
            if animate:
                animate_Move(gs.moveLog[-1], screen, gs.board, clock)
                print("Move made:", gs.moveLog[-1].get_Chess_Notation())
            valid_Moves = gs.get_Valid_Moves()
            move_Made = False
            animate = False

        draw_Game_State(screen, gs, valid_Moves, square_Selected)

        if gs.checkmate:
            game_Over = True
            if gs.whiteToMove:
                draw_Text(screen, "Black Wins By Checkmate")
            else:
                draw_Text(screen, "White Wins By Checkmate")
        elif gs.stalemate:
            game_Over = True
            draw_Text(screen, "Stalemate")
    

        clock.tick(MAX_FPS)
        p.display.flip()

def highlight_Squares(screen, gs, valid_Moves, square_Selected):
    if square_Selected != ():
        r, c = square_Selected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
            s.fill(p.Color("yellow"))
            for move in valid_Moves:
                if move.start_Row == r and move.start_Col == c:
                    screen.blit(s, (move.end_Col * SQUARE_SIZE, move.end_Row * SQUARE_SIZE))

def draw_Game_State(screen, gs, valid_Moves, square_Selected):
    draw_Board(screen)
    highlight_Squares(screen, gs, valid_Moves, square_Selected)
    draw_Pieces(screen, gs.board)

def draw_Board(screen):
    global colors 
    colors = [p.Color("light gray"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_Pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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
        end_Square = p.Rect(move.end_Col * SQUARE_SIZE, move.end_Row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_Square)
        if move.piece_Captured != "--" and move.en_Passant == False:
            screen.blit(IMAGES[move.piece_Captured], end_Square)
        screen.blit(IMAGES[move.piece_Moved], p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)

def draw_Text(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    text_Object = font.render(text, 0, p.Color("Gray"))
    text_Location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_Object.get_width() / 2, HEIGHT / 2 - text_Object.get_height() / 2)
    screen.blit(text_Object, text_Location)
    text_Object = font.render(text, 0, p.Color("Black"))
    screen.blit(text_Object, text_Location.move(2, 2))

if __name__ == "__main__":
    main()
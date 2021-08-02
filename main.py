import DamiluEngine
import pygame as p

player = "white"  # switch player to black if want to play black piece
double_players = False  # change it to True if you wanna play double players
difficulty = 0  # beginner: 0 easy : 1, medium : 2, hard : 3

width = height = 500
dim = 5
sq_size = height // dim
max_fps = 15
images = {}
WHITE = (255, 255, 255)
YELLOW = (255, 255, 100)

white_start = [["bP", "bP", "bP", "bP", "bP"],
               ["--", "--", "--", "--", "--"],
               ["--", "--", "--", "--", "--"],
               ["--", "--", "--", "--", "--"],
               ["wP", "wP", "wP", "wP", "wP"]]
black_start = [["wP", "wP", "wP", "wP", "wP"],
               ["--", "--", "--", "--", "--"],
               ["--", "--", "--", "--", "--"],
               ["--", "--", "--", "--", "--"],
               ["bP", "bP", "bP", "bP", "bP"]]
initial_cells = white_start if player == "white" else black_start


def load_images():
    """
    This function is used to link the image from images folder to their corresponding pieces
    in the dictionary images. The size of the image is decided by the sq_size variable.

    :return:nothing
    """
    pieces = ["wP", "bP"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_size, sq_size))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))

    board = DamiluEngine.Board(initial_cells)
    opp = DamiluEngine.Opponent()
    load_images()
    running = True
    player_clicks = []
    players_turn = board.white_to_move() if player == "white" else not board.white_to_move()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // sq_size
                row = location[1] // sq_size
                if board.cells[row][col] == board.current_piece or len(player_clicks) == 1:
                    selected_sq = (row, col)
                    player_clicks.append(selected_sq)
                if len(player_clicks) == 2:
                    move = (player_clicks[0], player_clicks[1])
                    if move in board.get_all_moves():
                        board = board.make_move(move)
                    player_clicks = []
                    if not double_players:
                        players_turn = False

        if board.is_over():  # stalemate
            if board.is_draw():
                print("Draw by stalemate")
                running = False
            elif board.p_num["wP"] <= 1:
                print("Black wins")
                running = False
            else:
                print("White wins")
                running = False

        elif not players_turn and not double_players:
            move = opp.get_best_move(board, difficulty)
            board = board.make_move(move)
            players_turn = True

        draw_board(screen)
        if len(player_clicks) == 1:
            p.draw.rect(screen, YELLOW, p.Rect(
                player_clicks[0][1] * sq_size, player_clicks[0][0] * sq_size, sq_size, sq_size))
        draw_pieces(screen, board.cells)
        clock.tick(max_fps)
        p.display.flip()


def draw_board(screen):
    """
    The function is used to draw the squares on the screen. The size of the square is decided
    by sq_size variable

    :param screen: the main screen that is defined in the main loop.
    :return: nothing.
    """
    colours = [p.Color("white"), p.Color("gray")]
    for r in range(dim):
        for c in range(dim):
            colour = colours[((r + c) % 2)]
            p.draw.rect(screen, colour, p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))


def draw_pieces(screen, board):
    """
    The function is used to draw pieces on the board into images by using the images dictionary

    :param screen: the main screen that is defined in the main loop.
    :param board: the board object that represents the current board.
    :return: nothing
    """
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))


if __name__ == "__main__":
    main()

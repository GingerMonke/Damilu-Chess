from copy import deepcopy
import math


class Board:
    """
    The class that stores the situation on the board
    """
    def __init__(self, cells):
        """
        board is 5x5 2D List, each element of the list has 2 characters
        initial character == colour (b,w)
        second character == piece
        -- == empty space
        """

        self.cells = cells
        self.current_piece = "wP"  # white moves first
        self.opposite_piece = "bP"
        self.p_num = {"wP": 5, "bP": 5}  # each side start with 5 pieces
        self.move_log = []  # move log for checking three fold. Move recorded as set

    def check_capture(self, move):
        """
        Eliminate any piece that fits the condition of being captured from the last move

        :param move: the last move that was used by make_move() function.
        :return: nothing
        """
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # left, down, right, up
        for d in directions:  # for each direction, evaluate all pieces on that direction
            side_piece = self.get_piece(move[1], d, 1)   # piece beside the moved piece
            back_piece = self.get_piece(move[1], d, -1)  # piece beside the moved piece in -direction
            ranged_piece = self.get_piece(move[1], d, 2)  # piece 1 square away from moved piece
            far_piece = self.get_piece(move[1], d, 3)    # piece 2 squares away from moved piece

            if side_piece == self.opposite_piece:
                """ side piece will be captured if it is in line with enemy moved piece and 
                   enemy back piece while not supported by an ally piece behind it(ranged piece)
                """
                if back_piece == self.current_piece and ranged_piece != self.opposite_piece:
                    self.cells[move[1][0] + d[0]][move[1][1] + d[1]] = "--"
                    self.p_num[self.opposite_piece] -= 1  # opponent loses one piece
                """ moved piece will be captured if it is in line with enemy side piece and
                    enemy ranged piece while not supported by an ally back piece
                """
                if ranged_piece == self.opposite_piece and back_piece != self.current_piece:
                    self.cells[move[1][0]][move[1][1]] = "--"  # that was a suicidal move for moved piece
                    self.p_num[self.current_piece] -= 1

            elif side_piece == self.current_piece:
                """ ranged piece will be captured if it is in line with enemy side piece and
                    enemy moved piece while not supported by an ally far piece 
                """
                if ranged_piece == self.opposite_piece and far_piece != self.opposite_piece:
                    self.cells[move[1][0] + d[0]*2][move[1][1] + d[1]*2] = "--"
                    self.p_num[self.opposite_piece] -= 1
            self.check_supported_piece(move, d)

    def check_supported_piece(self, move, d):
        """
        Eliminate any current piece will be captured due to its supporting piece
        has moved.

        :param move: the last move that was used by make_move() function.
        :param d: the direction it hs inherited from check_capture() function
        :return: nothing
        """
        supported_piece = self.get_piece(move[0], d, 1)
        side_piece = self.get_piece(move[0], d, 2)
        ranged_piece = self.get_piece(move[0], d, 3)
        if side_piece == ranged_piece == self.opposite_piece and (
                supported_piece == self.current_piece):
            self.cells[move[0][0] + d[0]][move[0][1] + d[1]] = "--"
            self.p_num[self.current_piece] -= 1

    def white_to_move(self):
        """
        check if it is white's turn to move
        :return: True if current_piece equals white piece else False.
        """
        return self.current_piece == "wP"

    def make_move(self, move):
        """
        the function makes move on the current board

        :param move: the move that was played
        :return: a new board with the new move that has been made on it
        """
        new = deepcopy(self)
        new.cells[move[0][0]][move[0][1]] = '--'
        new.cells[move[1][0]][move[1][1]] = self.current_piece
        new.check_capture(move)
        new.opposite_piece = "wP" if new.white_to_move() else "bP"
        new.current_piece = "bP" if new.white_to_move() else "wP"
        new.move_log.append({move[0], move[1]})
        return new

    def get_piece(self, sq, direction, distance):
        """
        check if the position is in index and get the piece in the position.

        :param sq: the starting position .
        :param direction: the direction of where the piece needs to be searched.
        :param distance: the distance of the position away from the starting position.
        :return: the piece(including --) if there is one else return None.
        """
        row = sq[0] + direction[0]*distance
        col = sq[1] + direction[1]*distance
        return self.cells[row][col] if (0 <= row < 5 and 0 <= col < 5) else None

    def get_all_moves(self):
        """
        get all possible moves for the current player, record each move as tuple

        :return: a list of all possible moves
        """
        moves = []
        for r in range(5):
            for c in range(5):
                if self.cells[r][c] == self.current_piece:
                    self.get_pawn_move(r, c, moves)
        return moves

    def get_pawn_move(self, r, c, moves):
        """
        this function appends all possible moves of the piece in that position into moves list

        :param r: the row of the piece
        :param c: the column of the piece
        :param moves: the list of all possible moves
        :return: nothing
        """
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            if self.get_piece((r, c), d, 1) == "--":
                moves.append(((r, c), (r + d[0], c + d[1])))

    def is_over(self):
        """
        check if the game is over.

        :return: True if the game is over else False.
        """
        return self.p_num["wP"] <= 1 or self.p_num["bP"] <= 1 or self.is_draw()

    def is_draw(self):
        """
        check if the game is draw. The game is draw if both sides have only 1 piece or less left

        :return: True if the game is draw else False
        """
        return self.p_num["wP"] == self.p_num["bP"] <= 1 or (
            self.is_three_fold())

    def is_three_fold(self):
        """
        check if both players have repeated a move 3 times in the last 12 moves.

        :return: True if three fold else False
        """
        len(self.move_log)
        if len(self.move_log) > 6:
            return self.move_log[-12:].count(self.move_log[-6]) >= 3 and (
                self.move_log[-12:].count(self.move_log[-5]) >= 3)
        return False


class Opponent:
    """
    The class the contains minimax algorithm for non-player opponent
    """
    def minimax(self, board, depth, a, b):
        """
        The minimax alpha beta pruning algorithm that evaluates the current board's situation.

        :param board: the current board
        :param depth: how many generation the function is going to calculate, larger depth is more accurate
        :param a: alpha value
        :param b: beta value
        :return: returns the evaluation of the board
        """
        if depth == 0 or board.is_over():
            return self.evaluate(board)
        if board.white_to_move():
            best = -math.inf
            for move in board.get_all_moves():
                evaluation = self.minimax(board.make_move(move), depth - 1, a, b)
                best = max(best, evaluation)
                a = max(a, evaluation)
                if b <= a:
                    break
        else:
            best = math.inf
            for move in board.get_all_moves():
                evaluation = self.minimax(board.make_move(move), depth - 1, a, b)
                best = min(best, evaluation)
                b = min(b, evaluation)
                if b <= a:
                    break
        return best

    def get_best_move(self, board, depth):
        """
        The function selects the best possible move by using the evaluation from the minimax function.

        :param board: the current board
        :param depth: the larger the depth the better the evaluation, but too large could cause computer freeze
        :return: the best move in a tuple form.
        """
        moves = board.get_all_moves()
        best_move = " "
        best_value = -math.inf if board.white_to_move() else math.inf
        for move in moves:
            value = self.minimax(board.make_move(move), depth, -math.inf, math.inf)
            if (board.white_to_move() and value > best_value) or (
                    not board.white_to_move() and value < best_value):
                best_value = value
                best_move = move
        return best_move

    def evaluate(self, board):
        """
        a basic evaluation of the game, the larger the value the better the situation is for white, vice versa.

        :param board: the current board
        :return: the evaluation of the current board
        """

        if board.is_over():
            if board.is_draw():
                score = 0
            elif board.p_num["wP"] == 1:
                score = -10000
            else:
                score = 10000
        else:
            score = board.p_num["wP"] - board.p_num["bP"]
            for r in range(1, 4):
                for c in range(1, 4):
                    piece = board.cells[r][c]
                    if piece != "--":
                        score += 0.1 if piece == "wP" else -0.1
                        if r == 2 and c == 2:
                            score += 0.5 if piece == "wP" else -0.5
        return score
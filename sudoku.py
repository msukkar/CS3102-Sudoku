import argparse

from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

BOARDS = ['debug', 'hi']  # Available sudoku boards
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
N = 3
WIDTH = HEIGHT = MARGIN * 2 + SIDE * N * N  # Width/height of the whole board


class SudokuError(Exception):
    """
    An application specific error.
    """
    pass


def parse_arguments():
    """
    Parses arguments of the form:
        sudoku.py <board name>
    Where `board name` must be in the `BOARD` list
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--size",
                            help="Board size",
                            type=int,
                            required=False)
    arg_parser.add_argument("--pixels",
                            help="size of cells",
                            type=int,
                            required=False)

    # Creates a dictionary of keys = argument flag, and value = argument
    args = vars(arg_parser.parse_args())
    return args


class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """

    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1

        self.init_ui()

    def init_ui(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        # clear_button = Button(self,
        # text="Clear answers",
        # command=self.__clear_answers)
        # clear_button.pack(fill=BOTH, side=BOTTOM)

        submit_button = Button(self,
                               text="Submit",
                               command=self.__submit_answers)
        submit_button.pack(fill=BOTH, side=BOTTOM)

        self.draw_grid()
        self.draw_puzzle()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)

    def draw_grid(self):
        """
        Draws grid divided with blue lines into squares
        """
        for i in range(N * N + 1):
            color = "blue" if i % N == 0 else "gray"
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(N * N):
            for j in range(N * N):
                answer = self.game.board[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.board[i][j]
                    color = "black"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    def draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def cell_clicked(self, event):
        x, y = event.x, event.y
        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE
            row = int(row)
            col = int(col)

            self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1
        self.draw_cursor()

    def key_pressed(self, event):

        if event.keysym == 'Right' and self.col < N * N - 1:
            self.col += 1
            self.draw_cursor()
        if event.keysym == 'Left' and self.col > 0:
            self.col -= 1
            self.draw_cursor()
        if event.keysym == 'Down' and self.row < N * N - 1:
            self.row += 1
            self.draw_cursor()
        if event.keysym == 'Up' and self.row > 0:
            self.row -= 1
            self.draw_cursor()

        if self.row >= 0 and self.col >= 0 and event.char:
            self.game.board[self.row][self.col] = int(event.char)
            self.draw_puzzle()
            self.draw_cursor()

    # def __clear_answers(self):
    # self.game.start()
    # self.__draw_puzzle()
    def __submit_answers(self):
        self.game.solve()


class SudokuBoard(object):
    """
    Sudoku Board representation
    """

    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = []
        for i in range(N * N):
            board.append([])
            for j in range(N * N):
                board[i].append(0)
        return board

    def solve(self):
        Solver(self.board)

'''
wrapper for lists because pointers are retarded in python
'''
class OptionList(list):

    pass

class Solver(object):

    def __init__(self, board):
        #  n^2 valid options for each of the n^4 squares
        options = [[True for i in range(N**2)] for j in range(N**4)]

    def solve(self, options):
        new_options = [options[i][:] for i in range(N**4)]
        #  ToDo find min number of Trues > 1
        min = 0
        for i in range (N**4):

        #  for each item true in that box
            #  set all other items in the box false
            #  calculate current row, collumn, square
            #  iterate through each item in row, collumn, square, and set to false
            #  self.solve(new_options)

    def get_coordinates(self, i):
        return self.get_row(i), self.get_column(i)

    def get_index(self, row, column):
        return row * N**2 + column

    def get_row(self, i):
        return [i/(N * N)]

    def get_column(self, i):
        return [i%(N * N)]

    def get_square(self, row, column):
        return N * (row/N) + (column/N)

if __name__ == '__main__':
    if parse_arguments()['size']:
        N = parse_arguments()['size']
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * N * N
    if parse_arguments()['pixels']:
        SIDE = parse_arguments()['pixels']
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * N * N

    game = SudokuBoard()

    root = Tk()
    SudokuUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()

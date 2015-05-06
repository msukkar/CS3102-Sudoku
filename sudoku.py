import argparse

from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

BOARDS = ['debug', 'hi']  # Available sudoku boards
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
N=3

WIDTH = HEIGHT = MARGIN * 2 + SIDE * N*N  # Width and height of the whole board


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
                            required=False,
                            )
    arg_parser.add_argument("--pixels",
                            help="size of cells",
                            type=int,
                            required=False,
                            )

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
        
        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        # clear_button = Button(self,
        #                       text="Clear answers",
        #                       command=self.__clear_answers)
        # clear_button.pack(fill=BOTH, side=BOTTOM)

        submit_button=Button(self,
        					 text="Submit",
        					 command=self.__submit_answers)
        submit_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into squares
        """
        for i in range(N*N+1):
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

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(N*N):
            for j in range(N*N):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    def __draw_cursor(self):
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

    def __cell_clicked(self, event):
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE
            row=int(row)
            col=int(col)
       
            self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):



        if event.keysym=='Right' and self.col<N*N-1:
            self.col+=1
            self.__draw_cursor()
        if event.keysym=='Left' and self.col>0:
            self.col-=1
            self.__draw_cursor()
        if event.keysym=='Down' and self.row<N*N-1:
            self.row+=1
            self.__draw_cursor()
        if event.keysym=='Up' and self.row>0:
            self.row-=1
            self.__draw_cursor()

        if self.row >= 0 and self.col >= 0 and event.char:
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.__draw_puzzle()
            self.__draw_cursor()


    def __clear_answers(self):
        self.game.start()
        self.__draw_puzzle()
    def __submit_answers(self):
        self.game

class SudokuBoard(object):
    """
    Sudoku Board representation
    """
    def __init__(self):
        self.board = self.__create_board()

    def __create_board(self):
        board=[]
        for i in range(N*N):
            board.append([])
            for j in range (N*N):
                board[i].append(0)
        return board

class SudokuGame(object):
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """
    def __init__(self):
        self.start_puzzle = SudokuBoard().board

    def start(self):
        self.game_over = False
        self.puzzle = []
        for i in range(N*N):
            self.puzzle.append([])
            for j in range(N*N):
                self.puzzle[i].append(self.start_puzzle[i][j])

    def __check_block(self, block):
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block(
            [self.puzzle[row][column] for row in range(N*N)]
        )

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in range(row * N, (row + 1) * N)
                for c in range(column * N, (column + 1) * N)
            ]
        )

    def __solve(self):
    	"hi"


if __name__ == '__main__':
    if parse_arguments()['size']:
        N=parse_arguments()['size']
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * N*N
    if parse_arguments()['pixels']:
        SIDE=parse_arguments()['pixels']
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * N*N

    game = SudokuGame()
    game.start()

    root = Tk()
    SudokuUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()

import argparse, random

from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, X


BOARDS = ['debug', 'hi']  # Available sudoku boards
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
N = 3
WIDTH = HEIGHT = MARGIN * 2 + SIDE * N**2  # Width/height of the whole board

nonomino = -1
nonomino_squares=[[] for i in range (N**2)]
nonomino_cells=[0 for i in range (N**4)]

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
    arg_parser.add_argument("--file",
                             help="file to read from",
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
        self.r, self.g, self.b = 0, 0, 0

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
                               command=self.submit_answers)
        submit_button.pack(fill=X, side=BOTTOM)

        
        nonomino_button = Button(self,
                                 text="Nonomino",
                                 command=self.nonomino)
        nonomino_button.pack(fill=X, side=BOTTOM)

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
                    color = "white" if nonomino else "black"
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
            
            outline='white' if nonomino>=0 else 'red'
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline=outline, tags="cursor"
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

        global nonomino
        
      
        if nonomino>=0 and nonomino<N**4 and self.row>=0:

            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            
            nonomino_squares[nonomino/N**2]=self.row*N**2+self.col
            nonomino_cells[self.row*N**2+self.col]=nonomino/N**2
            
            if (nonomino) % N**2==0:
                self.r = random.randint(20, 255)   
                self.g = random.randint(20,255)
                self.b = random.randint(20,255) 
            self.canvas.create_rectangle(x0, y0, x1, y1, fill= "#%02x%02x%02x" % (self.r, self.g, self.b))
            nonomino+=1
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

        if event.keysym == 'BackSpace' or event.keysym=='Delete' and self.row>=0 and self.col>=0:
            self.game.board[self.row][self.col]=0
            self.draw_puzzle()
        
        elif self.row >= 0 and self.col >= 0 and event.char:
            current_val=self.game.board[self.row][self.col]
            if  current_val != 0:
                self.game.board[self.row][self.col]= int(str(current_val)+event.char)
            else:
                self.game.board[self.row][self.col]= int(event.char)
            self.draw_puzzle()
            self.draw_cursor()


    # def __clear_answers(self):
    # self.game.start()
    # self.__draw_puzzle()
    def submit_answers(self):
        self.game.solve()
        self.draw_puzzle()

    def nonomino(self):
        global nonomino
        nonomino=0



class SudokuBoard(object):
    """
    Sudoku Board representation
    """

    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        
        board = []
        if parse_arguments()['file']:
            board=eval(self.read_file(parse_arguments()['file']))
        else:
            for i in range(N**2):
                board.append([])
                for j in range(N**2):
                    board[i].append(0)
        return board

    def solve(self):
        Solver(self.board)

    def read_file(self, sudoku_file):
        with open (sudoku_file, "r") as sudoku:
            return sudoku.read().replace('\n', '')



class Solver(object):
    def __init__(self, board):
        #  testing board
        #board = [[0, 0, 0, 0, 6, 0, 0, 5, 0], [0, 4, 2, 5, 0, 0, 0, 6, 0], [6, 0, 0, 7, 0, 0, 0, 9, 0], [0, 9, 5, 0, 0, 4, 1, 0, 6], [4, 6, 0, 1, 2, 5, 0, 8, 7], [1, 0, 7, 6, 0, 0, 4, 3, 0], [0, 8, 0, 0, 0, 3, 0, 0, 9], [0, 3, 0, 0, 0, 7, 2, 1, 0], [0, 7, 0, 0, 8, 0, 0, 0, 0]]

        #  n^2 valid options for each of the n^4 squares and an extra flag
        # stating whether option is actually selected
        options = [[True for i in range(N**2 + 1)] for j in range(N**4)]
        
        for i in range(N**2):
            for j in range(N**2):
                cell_value = board[i][j]
                if cell_value != 0:
                    index = self.get_index(i,j)
                    self.guess(options, index, cell_value-1)
        self.board=board
        options = self.solve(options)

        if options:
            for i in range(N**4):
                board[self.get_row(i)][self.get_column(i)] = self.get_value(options[i]) + 1
            print board

        

    def solve(self, options):
        #  find min number of Trues in un-guessed cells
        min_index = -1
        min = N**2 + 1 #  not possible unless all 1
        for i in range (N**4):
            sum = self.options_left(options[i])
            if sum <= min and options[i][N**2]:
                min = sum
                min_index = i
        if min == 0:
            return None
        if min == N**2 + 1:
            return options

        #  for each item true in that box
        for i in range(N**2):
            if options[min_index][i]:
                #  copy
                guess = [options[j][:] for j in range(N**4)]

                self.guess(guess, min_index, i)

                #  recursively solve
                guess = self.solve(guess)
                if guess:
                    return guess
        return None

    def guess(self, options, cell, value):
        #  set all other items in the box false
        for i in range(N**2):
            options[cell][i] = False
        #  calculate current row, collumn, square
        row, column = self.get_row(cell), self.get_column(cell)
        square_row, square_column = self.get_square(row, column)
        #  iterate through each item in row, collumn, square, and set to false
        queue = []
        for i in range(N**2):
            options[self.get_index(row, i)][value] = False
            options[self.get_index(i, column)][value] = False

        if nonomino:
            options[cell][value]=True
            for cell in self.get_square(row, column): options[cell][value]=False 
        else:
            for i in range(N):
                for k in range(N):
                    options[self.get_index(square_row + i, square_column + k)][value] = False
            options[cell][value] = True

        options[cell][N**2] = False


    def options_left(self, cell):
        sum = 0
        for option in cell:
            if option:
                sum += 1
        return sum

    def get_value(self, cell):
        for i in range(N**2):
            if cell[i]:
                return i

    def get_index(self, row, column):
        return row * N**2 + column

    def get_row(self, i):
        return i/(N * N)

    def get_column(self, i):
        return i%(N * N)

 
    def get_square(self, row, column):
        if nonomino:
            num_square=nonomino_cells[self.get_index(row, column)]
            return nonomino_squares[num_square]
        return N * (row/N), N * (column/N)


if __name__ == '__main__':
    if parse_arguments()['size']:
        N = parse_arguments()['size']
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * N * N
    if parse_arguments()['pixels']:
        SIDE = parse_arguments()['pixels']
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * N * N

    game = SudokuBoard()

    root = Tk()
    ui = SudokuUI(root, game)
    window_height = HEIGHT+60
    root.geometry("%dx%d" % (WIDTH, window_height))
    root.mainloop()

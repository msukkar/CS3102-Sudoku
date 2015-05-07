import argparse, random

from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, X

BOARDS = ['debug', 'hi']  # Available sudoku boards
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
N = 3
WIDTH = HEIGHT = MARGIN * 2 + SIDE * N**2  # Width/height of the whole board

nonomino = -1
nonomino_squares=[[] for i in range (N**2)]
nonomino_cells=[0 for j in range (N**4)]

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
    arg_parser.add_argument("--nfile",
                             help="nonomino file",
                             required=False)
    arg_parser.add_argument("--generate",
                             help="generate a random board",
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
        self.rgb= [[[] for i in range(3)] for j in range(N**2)]

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
        self.draw_puzzle(False)

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

    def draw_puzzle(self, submitted):
        self.canvas.delete("numbers")
        for i in range(N * N):
            for j in range(N * N):
                answer = self.game.board[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.board[i][j]
                    
                    if submitted and 0 in [cell for row in self.game.board for cell in row]: color="red" 
                    elif nonomino>=0: color = "white" 
                    else: color="black"
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

        x0 = MARGIN + self.col * SIDE + 1
        y0 = MARGIN + self.row * SIDE + 1
        x1 = MARGIN + (self.col + 1) * SIDE - 1
        y1 = MARGIN + (self.row + 1) * SIDE - 1
        
       
        # if nonomino>=0 and nonomino<N**4 and self.row>=0:

        #     square_num=nonomino/N**2

        #     nonomino_squares[square_num]=self.row*N**2+self.col
        #     nonomino_cells[self.row*N**2+self.col]=square_num

        #     if (nonomino) % N**2==0:
        #         self.rgb[square_num][0]=random.randint(20, 230)
        #         self.rgb[square_num][1]=random.randint(20, 230)
        #         self.rgb[square_num][2]=random.randint(20, 230)
        #     self.canvas.create_rectangle(x0, y0, x1, y1, fill= "#%02x%02x%02x" % (self.rgb[square_num][0], self.rgb[square_num][1], self.rgb[square_num][2]))
        #     nonomino+=1
            
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
            self.draw_puzzle(False)
        
        elif self.row >= 0 and self.col >= 0 and event.char.isdigit():
            current_val=self.game.board[self.row][self.col]
            if  current_val != 0:
                self.game.board[self.row][self.col]= int(str(current_val)+event.char)
            else:
                self.game.board[self.row][self.col]= int(event.char)
            self.draw_puzzle(False)
            self.draw_cursor()

        elif self.row >= 0 and self.col >= 0 and event.char.isalpha() and nonomino>=0:
            square_num=ord(event.char)-97
            
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            

            if square_num>=0 and square_num<N**2:
                for square in nonomino_squares:
                    if self.row*N**2+self.col in square:
                        square.remove(self.row*N**2+self.col)
                nonomino_squares[square_num].append(self.row*N**2+self.col)
                nonomino_cells[self.row*N**2+self.col]=square_num
                if not self.rgb[square_num][0]:
                    self.rgb[square_num][0]=random.randint(20, 230)
                    self.rgb[square_num][1]=random.randint(20, 230)
                    self.rgb[square_num][2]=random.randint(20, 230)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill= "#%02x%02x%02x" % (self.rgb[square_num][0], self.rgb[square_num][1], self.rgb[square_num][2]))


    def submit_answers(self):

        self.game.solve()
        self.draw_puzzle(True)

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
            board = eval(self.read_file(parse_arguments()['file']))
        elif parse_arguments()['generate']:
            board = self.generate_board()
        else:
            for i in range(N**2):
                board.append([])
                for j in range(N**2):
                    board[i].append(0)
        return board

    def generate_board(self):
        while True:
            gen_board = [[0 for i in range(N**2)] for j in range(N**2)]
            for i in range(int(float(N)**3.2)):
                row = random.randint(0, N**2 - 1)
                column = random.randint(0, N**2 - 1)
                value = random.randint(1, N**2)
                gen_board[row][column] = value
            if self.solve([x[:] for x in gen_board]):
                print gen_board
                return gen_board

    def solve(self, new_board=None):
        if new_board:
            solver = Solver(new_board)
            return solver.possible
        else:
            solver = Solver(self.board)
            return solver.possible

    def read_file(self, sudoku_file):
        with open (sudoku_file, "r") as sudoku:
            return sudoku.read().replace('\n', '')


class Solver(object):
    def __init__(self, board):
        #  testing board
        #board = [[0, 0, 0, 0, 6, 0, 0, 5, 0], [0, 4, 2, 5, 0, 0, 0, 6, 0], [6, 0, 0, 7, 0, 0, 0, 9, 0], [0, 9, 5, 0, 0, 4, 1, 0, 6], [4, 6, 0, 1, 2, 5, 0, 8, 7], [1, 0, 7, 6, 0, 0, 4, 3, 0], [0, 8, 0, 0, 0, 3, 0, 0, 9], [0, 3, 0, 0, 0, 7, 2, 1, 0], [0, 7, 0, 0, 8, 0, 0, 0, 0]]

        #  n^2 valid options for each of the n^4 squares and an extra flag
        #  stating whether option is actually selected
        options = [[True for i in range(N**2 + 1)] for j in range(N**4)]
        self.possible = False
        #  counter to memoize current num_options
        for cell in options:
            cell.append(N**2)
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
            print "solved: " + str(board)
            self.possible = True

    def solve(self, options):
        #  find min number of Trues in un-guessed cells
        min_index = 0
        min = N**2 + 4 #  not possible unless all 1
        for i in range (N**4):
            if options[i][-1] == 0:
                return None
            if options[i][-1] < min and options[i][-2]:
                min = options[i][-1]
                min_index = i
        if min == N**2 + 4:
            print [self.get_value(option) + 1 for option in options]
            return options

        #  for each item true in that box
        good_guess = None
        for i in range(N**2):
            if options[min_index][i]:
                #  copy or reference
                if min == 1:
                    guess = options
                else:
                    guess = [options[j][:] for j in range(N**4)]

                self.guess(guess, min_index, i)

                #  recursively solve
                guess = self.solve(guess)

                if guess:
                    good_guess = guess
        return good_guess

    def guess(self, options, cell, value):
        #  calculate current row, collumn, square
        row, column = self.get_row(cell), self.get_column(cell)
        
        #  iterate through each item in row, collumn, square, and set to false
        for i in range(N**2):
            index = self.get_index(row, i)
            if options[index][value]:
                options[index][-1] -= 1
                options[index][value] = False
            index = self.get_index(i, column)
            if options[index][value]:
                options[index][-1] -= 1
                options[index][value] = False
        if nonomino>=0:
            for index in nonomino_squares[self.get_square(row, column)]:
                options[index][value]=False 
                options[index][-1] -= 1
        else:
            square_row, square_column = self.get_square(row, column)
            for i in range(N):
                for k in range(N):
                    index = self.get_index(square_row + i, square_column + k)
                    if options[index][value]:
                        options[index][-1] -= 1
                        options[index][value] = False

        #  set all other items in the box false
        for i in range(N**2):
            options[cell][i] = False
        options[cell][value] = True
        options[cell][-1] = 1
        options[cell][-2] = False

    def options_left(self, cell, min=N**2+2):
        sum = 0
        for i in range(N**2):
            if cell[i] == True:
                sum += 1
            if sum >= min:
                break
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
        if nonomino>=0:
            return nonomino_cells[self.get_index(row, column)]
        return N * (row/N), N * (column/N)


if __name__ == '__main__':
    if parse_arguments()['size']:
        N = parse_arguments()['size']
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * N * N
        nonomino_squares=[[] for i in range (N**2)]
        nonomino_cells=[0 for j in range (N**4)]
    if parse_arguments()['pixels']:
        SIDE = parse_arguments()['pixels']
        WIDTH = HEIGHT = MARGIN * 2 + SIDE * N * N
        nonomino_squares=[[] for i in range (N**2)]
        nonomino_cells=[0 for j in range (N**4)]

    game = SudokuBoard()

    root = Tk()
    ui = SudokuUI(root, game)
    window_height = HEIGHT+60
    root.geometry("%dx%d" % (WIDTH, window_height))
    root.mainloop()

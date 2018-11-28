import Tkinter as tk
import board
import logging
import os

from config import XX, OO

logging.basicConfig(level=logging.DEBUG)

SQUARE_COLOR = '#58ae8b'

SQUARE_SIZE = 200

TEXT_FACTOR = 1 - max(len(XX), len(OO)) / 7.0

MYDIR = os.path.dirname(os.path.realpath(__file__))

def flip_coords(x,y):
    return (x,2-y)

class TicTacToe(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.grid()
        self._board = board.Board()

        self.sides_normal = True

        self.label = tk.Label(self, text="", font=('Times', int(SQUARE_SIZE*.1)))
        self.label.grid(row=0, column=1, columnspan=3)

        self.canvas = tk.Canvas(self, width=3*SQUARE_SIZE, height=3*SQUARE_SIZE)

        for ridx, rname in enumerate(list('321')):
            for fidx, fname in enumerate(list('abc')):
                tag = fname + rname

                tags = [fname+rname, 'square']

                self.canvas.create_rectangle(
                    fidx*SQUARE_SIZE, ridx*SQUARE_SIZE,
                    fidx*SQUARE_SIZE+SQUARE_SIZE, ridx*SQUARE_SIZE+SQUARE_SIZE,
                    outline='black', fill=SQUARE_COLOR, tag=tags)
        
        self.canvas.grid(row=1, column=1, columnspan=3)

        self.refresh()

        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=2, column=1)

        self.newButton = tk.Button(self, text='New Game', command=self.reset_board)
        self.newButton.grid(row=2, column=2)

        self.flipButton = tk.Button(self, text='Flip Sides', command=self.flip_sides)
        self.flipButton.grid(row=2, column=3)

    def reset_board(self):
        self._board = board.Board()
        self.refresh()

    def flip_sides(self):
        self.sides_normal = not self.sides_normal
        self.reset_board()

    def get_text_and_color(self, piece):
        text = piece
        if not self.sides_normal:
            text = OO if piece == XX else XX

        color = 'blue' if text == XX else 'red'

        return (text, color)

    def place_piece(self, square, piece):
        p, fill = self.get_text_and_color(piece)
        # canvas rectangle objects are tagged with 'a1', etc.
        item = self.canvas.find_withtag(square)
        # get bounding box of rectangle
        coords = self.canvas.coords(item)
        # do it
        image = self.canvas.create_text(coords[0]+SQUARE_SIZE/2, coords[1]+SQUARE_SIZE/2, text=p,
                                         state=tk.NORMAL, tag='piece', font=('Times', int(SQUARE_SIZE*TEXT_FACTOR)), fill=fill)

    def refresh(self):
        self.canvas.delete('piece')
        self.canvas.delete('line')

        # add bindings for clicking on any object with the "square" tag
        self.canvas.tag_bind("square", "<ButtonPress-1>", self.mouse_click)

        for x, fname in enumerate(list('abc')):
            for y, rname in enumerate(list('123')):
                sname = fname + rname

                piece = self._board.get_piece(x,y)
                if piece is not None:
                    #self.canvas.update_idletasks()
                    self.place_piece(sname, piece)

        result = self._board.game_over()
        if not result['over']:
            text, color = self.get_text_and_color(self._board.active)
            self.label.config(text="It's {}'s turn!".format(text), fg=color)
        else:
            text = "Game Over!"

            # disable the clicking
            self.canvas.tag_bind("square", "<ButtonPress-1>", lambda x: None)

            if result['winner'] is None:
                text += " Draw!"
            else:
                text += " {} Won!".format(self.get_text_and_color(result['winner'])[0])
        
            self.label.config(text=text, fg="black")
            
            line = result['line']
            if line is None:
                # out of moves. no need to draw a line
                return

            start, end = result['line']
            extras = [SQUARE_SIZE/2]*4
            start = flip_coords(*start)
            end   = flip_coords(*end)

            if start[0] != end[0]:
                extras[0] += (start[0] - 1)*SQUARE_SIZE/4
                extras[2] += (end[0] - 1)*SQUARE_SIZE/4

            if start[1] != end[1]:
                extras[1] += (start[1] - 1)*SQUARE_SIZE/4
                extras[3] += (end[1] - 1)*SQUARE_SIZE/4

            self.canvas.create_line(start[0]*SQUARE_SIZE+extras[0], start[1]*SQUARE_SIZE+extras[1],
                                    end[0]*SQUARE_SIZE+extras[2], end[1]*SQUARE_SIZE+extras[3],
                                    fill='yellow', width=5, tags='line')

    def mouse_click(self, event):
        '''Place a piece if possible'''

        coords = flip_coords(event.x / SQUARE_SIZE, event.y / SQUARE_SIZE)
        logging.debug("Clicking coords {}".format(board.c2n(*coords)))

        self._board.place_piece(*coords)
        self.refresh()

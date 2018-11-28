import logging
import copy

logging.basicConfig(level=logging.DEBUG)

from config import XX, OO

def validate_name(name):
    if name not in (XX, OO):
        raise Exception, "Piece name {} is not allowed".format(name)

def c2n(x,y):
    return chr(ord('A')+x) + chr(ord('1')+y)

class Board(object):
    def __init__(self):
        self.board = [[None for j in range(3)] for i in range(3)]

        self.active = XX

        logging.debug("Finished board setup")

    def __repr__(self):
        sep = "-------------------"
        output  = ["   | A | B | C |   "]
        output.append(sep)
        for i in range(3):
            line = " {} |".format(i+1)
            for j in range(3):
                piece = self.board[j][i]
                line += " {} |".format(' ' if piece is None else str(piece))
            line += "   "
            output.append(line)
            output.append(sep)
        output.append("   |   |   |   |   ")
        output.reverse()
        output.append("TURN: {}".format(self.active))
        
        return "\n".join(output)

    def flip_active(self):
        self.active = OO if self.active == XX else XX

    # get a piece given its x and y coordinates
    def get_piece(self, x, y):
        return self.board[x][y]

    def place_piece(self, x, y):
        piece = self.get_piece(x,y)

        if piece is not None:
            logging.info("Invalid move: There is already a piece in the clicked location.")
            return

        self.board[x][y] = self.active

        ## FLIP ACTIVE
        self.flip_active()

        ## DONE
        logging.debug("Current board position\n{}\n".format(self))

    def game_over(self):

        # this is the default when we run out of moves
        result = {'over' : True, 'winner' : None, 'line' : None }

        # check vertical and horizontal lines first
        for i in range(3):
            if self.board[i][0] is not None and (self.board[i][0] == self.board[i][1] == self.board[i][2]):
                result['line'] = ((i,0), (i,2))
            elif self.board[0][i] is not None and (self.board[0][i] == self.board[1][i] == self.board[2][i]):
                result['line'] = ((0,i), (2,i))
                
        # check the 2 diagonals
        if self.board[1][1] is not None:
            if self.board[0][0] == self.board[1][1] == self.board[2][2]:
                result['line'] = ((0,0), (2,2))
            elif self.board[0][2] == self.board[1][1] == self.board[2][0]:
                result['line'] = ((0,2), (2,0))

        if result['line'] is not None:
            start = result['line'][0]
            # we have a winner
            result['winner'] = self.board[start[0]][start[1]]
            return result

        # any moves left?
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    result['over'] = False  # there are free squares so we're not done
                    break

        return result
        



import os
from constants import *

class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        """Insantiate a Piece class object; texture is optional and should be a path to an image file."""
        self.name = name
        self.color = color
        value_sign = 1 if color == WHITE else -1
        self.value = value * value_sign
        if (texture == None):
            self.setTexture()
        else:
            self.texture = texture
        self.texture_rect = texture_rect
        
        #Might improve this
        self.moves = []
        self.moved = False

    def setTexture(self, size=80):
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    #Might improve this
    def addMove(self, move):
        self.moves.append(move)

    def clearMoves(self):
        self.moves = []
class Pawn(Piece):
    def __init__(self, color):
        self.direction = -1 if color == WHITE else 1
        super().__init__(PAWN, color, PAWN_VALUE)

class Knight(Piece):
    def __init__(self, color):
        self.direction = -1 if color == WHITE else 1
        super().__init__(KNIGHT, color, KNIGHT_VALUE)

class Rook(Piece):
    def __init__(self, color):
        self.direction = -1 if color == WHITE else 1
        super().__init__(ROOK, color, ROOK_VALUE)

class Bishop(Piece):
    def __init__(self, color):
        self.direction = -1 if color == WHITE else 1
        super().__init__(BISHOP, color, BISHOP_VALUE)

class Queen(Piece):
    def __init__(self, color):
        self.direction = -1 if color == WHITE else 1
        super().__init__(QUEEN, color, QUEEN_VALUE)

class King(Piece):
    def __init__(self, color):
        self.direction = -1 if color == WHITE else 1
        self.leftRook = None
        self.rightRook = None
        super().__init__(KING, color, KING_VALUE)
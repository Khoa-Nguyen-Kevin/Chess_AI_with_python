
class Square:

    #ALPHACOLS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        #self.alphacols = self.ALPHACOLS[col]
    
    def __eq__(self, object) -> bool:
        return isinstance(object, Square) and self.row == object.row and self.col == object.col
    
    def __repr__(self) -> str:
        return '(' + str(self.row) + ', ' + str(self.col) + ')'
    
    def hasPiece(self):
        return self.piece != None
    
    def isEmpty(self):
        return not self.hasPiece()
    
    def hasAllyPiece(self, color):
        return self.hasPiece() and self.piece.color == color
    
    def hasRivalPiece(self, color):
        return self.hasPiece() and self.piece.color != color
    
    def isEmptyOrRival(self, color):
        """Check if the square is empty or has a rival piece, which makes it possible to move to."""
        return self.isEmpty() or self.hasRivalPiece(color)

    @staticmethod
    def inBounds(*args):
        """Check if square is in bounds."""
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    @staticmethod
    def getAlphaCol(col):
        ALPHACOLS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
        return ALPHACOLS[col]

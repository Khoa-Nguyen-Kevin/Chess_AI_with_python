
class Move:

    def __init__(self, initialPos, finalPos):
        self.initialPos = initialPos
        self.finalPos = finalPos

    def __eq__(self, object) -> bool:
        return isinstance(object, Move) and self.initialPos == object.initialPos and self.finalPos == object.finalPos
    
    def __str__(self) -> str:
        return str(self.initialPos) + ", " + str(self.finalPos)
    
    def __repr__(self) -> str:
        return str(self.initialPos) + ", " + str(self.finalPos)

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
    
    def __hash__(self) -> int:
        return hash(self.finalPos.col+10*self.finalPos.row) #We hash by final position, each square on board is one index starting from 0,1,2,3,4,5,6,7
                                                            #                                                                           8,9,10,11,12,13,14,15
                                                            #                                                                           15,16,17,18,19,20,21,22
                                                            #                                                                              ..........
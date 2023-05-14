import random
from constants import *
import copy

class AIModel:
    def __init__(self) -> None:
        self.algorithm = None
    
    def randomMove(self, board, color):
        move = None
        while(move == None):
            for row in range(ROWS):
                for col in range(COLS):
                    if board.squares[row][col].hasAllyPiece(color):
                        piece = board.squares[row][col].piece
                        board.calValidMoves(piece,row,col)
                        for validmove in piece.moves:
                            if (random.randint(1,10) == 1):
                                move = validmove
                                return piece, move
    
    def captureWhenAbleMove(self, board, color):
        valueSign = -1 if color == BLACK else 1
        tempBoard = copy.deepcopy(board)
        initialBoardValue = self.calBoardValue(tempBoard)
        finalBoardValues = {}
        Move = None
        for row in range(ROWS):
            for col in range(COLS):
                if tempBoard.squares[row][col].hasAllyPiece(color):
                    tempPiece = tempBoard.squares[row][col].piece
                    tempBoard.calValidMoves(tempPiece, row, col)
                    for move in tempPiece.moves:
                        if tempBoard.squares[move.finalPos.row][move.finalPos.col].hasRivalPiece(color):
                            rivalPiece = tempBoard.squares[move.finalPos.row][move.finalPos.col].piece
                            finalBoardValue = initialBoardValue + (valueSign*rivalPiece.value)
                            if color == WHITE:
                                if finalBoardValue > initialBoardValue:
                                    return tempPiece, move
                            if color == BLACK:
                                if finalBoardValue < initialBoardValue:
                                    return tempPiece, move
                            #finalBoardValues[move] = finalBoardValue
        if Move == None:
            return self.randomMove(board, color)
        #if len(finalBoardValues) == 0: #If there are no caturing moves
        #    return self.randomMove(board, color)
        #if color == BLACK:
        #    return min(finalBoardValues, key=finalBoardValues.get)
        #else:
        #    return max(finalBoardValues, key=finalBoardValues.get)
    
    def calBoardValue(self, board, color=WHITE):
        allyValue = 0
        rivalValue = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].hasAllyPiece(color):
                    allyValue += board.squares[row][col].piece.value
                if board.squares[row][col].hasRivalPiece(color):
                    rivalValue += board.squares[row][col].piece.value
        boardValue = allyValue + rivalValue
        return boardValue
    
    def minMaxMove(self, board, color):
        pass

    def alphaBetaPruning(self, board, color):
        pass

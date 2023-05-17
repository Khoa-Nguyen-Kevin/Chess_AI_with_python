import random
from constants import *
import copy
from move import Move
from square import Square

MINIMAX_CUTOFF = 2
ALPHABETA_CUTOFF = 2

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
    
    def miniMaxMove(self, board, color):
        cutoffVal = MINIMAX_CUTOFF
        tempBoard = copy.deepcopy(board)
        if color == BLACK:
            returnsTuple = self.minValue(tempBoard, cutoffVal)
        else:
            returnsTuple = self.maxValue(tempBoard, cutoffVal)
        return returnsTuple[1], returnsTuple[2]

    def maxValue(self, tempBoard, cutoff):
        moveList = []
        pieceList = []
        valList = []
        if cutoff == 0:
            return self.calBoardValue(tempBoard), None, None
        else:
            for row in range(ROWS):
                for col in range(COLS):
                    if tempBoard.squares[row][col].hasAllyPiece(WHITE):
                        piece = tempBoard.squares[row][col].piece
                        tempBoard.calValidMoves(piece,row,col)
                        for move in piece.moves:
                            board = copy.deepcopy(tempBoard)
                            #backtrackMove = Move(move.finalPos, move.initialPos)
                            board.move(piece,move)
                            moveValue = self.minValue(board, cutoff-1)[0]
                            valList.append(moveValue)
                            pieceList.append(piece)
                            moveList.append(move)
                            #tempBoard.move(piece,backtrackMove) #move the piece back, to save processing power
        
        #print("MaxValues:")
        #print(pieceList)
        #print(moveList)
        #print(valList)
        chosenPiece = pieceList[valList.index(max(valList))]
        chosenMove = moveList[valList.index(max(valList))]
        print(chosenMove)
        return max(valList), chosenPiece, chosenMove

    def minValue(self, tempBoard, cutoff):
        moveList = []
        pieceList = []
        valList = []
        if cutoff == 0:
            return self.calBoardValue(tempBoard), None, None
        else:
            for row in range(ROWS):
                for col in range(COLS):
                    if tempBoard.squares[row][col].hasAllyPiece(BLACK):
                        piece = tempBoard.squares[row][col].piece
                        tempBoard.calValidMoves(piece,row,col)
                        for move in piece.moves:
                            board = copy.deepcopy(tempBoard)
                            #backtrackMove = Move(move.finalPos, move.initialPos)
                            board.move(piece,move)
                            moveValue = self.maxValue(board, cutoff-1)[0]
                            valList.append(moveValue)
                            pieceList.append(piece)
                            moveList.append(move)
                            #tempBoard.move(piece,backtrackMove) #move the piece back, to save processing power
        
        #print("MinValues:")
        #print(pieceList)
        #print(moveList)
        #print(valList)
        chosenPiece = pieceList[valList.index(min(valList))]
        chosenMove = moveList[valList.index(min(valList))]
        print(chosenMove)
        return min(valList), chosenPiece, chosenMove
    
    def alphaBetaPruning(self, board, color):
        cutoffVal = ALPHABETA_CUTOFF
        alpha = -10000
        beta = 10000
        tempBoard = copy.deepcopy(board)
        if color == BLACK:
            returnsTuple = self.betaValue(tempBoard, cutoffVal, alpha, beta)
        else:
            returnsTuple = self.alphaValue(tempBoard, cutoffVal, alpha, beta)
        return returnsTuple[1], returnsTuple[2]
    def alphaValue(self, tempBoard, cutoff, alpha, beta):
        moveList = []
        pieceList = []
        valList = []
        if cutoff == 0:
            return self.calBoardValue(tempBoard), None, None, alpha, beta
        else:
            for row in range(ROWS):
                for col in range(COLS):
                    if tempBoard.squares[row][col].hasAllyPiece(WHITE):
                        piece = tempBoard.squares[row][col].piece
                        tempBoard.calValidMoves(piece,row,col)
                        for move in piece.moves:
                            board = copy.deepcopy(tempBoard)
                            #backtrackMove = Move(move.finalPos, move.initialPos)
                            board.move(piece,move)
                            returnTuple = self.betaValue(board, cutoff-1, alpha, beta)
                            moveValue = returnTuple[0]
                            alpha = max(returnTuple[3], alpha)
                            beta = returnTuple[4]
                            if moveValue >= beta:
                                return moveValue, piece, move, moveValue, beta
                            valList.append(moveValue)
                            pieceList.append(piece)
                            moveList.append(move)
                            #tempBoard.move(piece,backtrackMove) #move the piece back, to save processing power
        
        #print("MaxValues:")
        #print(pieceList)
        #print(moveList)
        #print(valList)
        if (len(valList) == 0): #No moves are available
            return -10000, None, None, alpha, beta
        chosenPiece = pieceList[valList.index(max(valList))]
        chosenMove = moveList[valList.index(max(valList))]
        #print(chosenMove)
        return max(valList), chosenPiece, chosenMove, alpha, beta

    def betaValue(self, tempBoard, cutoff, alpha, beta):
        moveList = []
        pieceList = []
        valList = []
        if cutoff == 0:
            return self.calBoardValue(tempBoard), None, None, alpha, beta
        else:
            for row in range(ROWS):
                for col in range(COLS):
                    if tempBoard.squares[row][col].hasAllyPiece(BLACK):
                        piece = tempBoard.squares[row][col].piece
                        tempBoard.calValidMoves(piece,row,col)
                        for move in piece.moves:
                            board = copy.deepcopy(tempBoard)
                            #backtrackMove = Move(move.finalPos, move.initialPos)
                            board.move(piece,move)
                            returnTuple = self.alphaValue(board, cutoff-1, alpha, beta)
                            moveValue = returnTuple[0]
                            alpha = returnTuple[3]
                            beta = min(returnTuple[4],beta)
                            if moveValue <= alpha:
                                return moveValue, piece, move, alpha, moveValue
                            valList.append(moveValue)
                            pieceList.append(piece)
                            moveList.append(move)
                            #tempBoard.move(piece,backtrackMove) #move the piece back, to save processing power
        
        #print("MinValues:")
        #print(pieceList)
        #print(moveList)
        #print(valList)
        if (len(valList) == 0):#No moves are available
            return 10000, None, None, alpha, beta
        chosenPiece = pieceList[valList.index(min(valList))]
        chosenMove = moveList[valList.index(min(valList))]
        #print(chosenMove)
        return min(valList), chosenPiece, chosenMove, alpha, beta
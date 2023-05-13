from constants import *
from square import Square
from piece import *
from move import Move
import copy

class Board:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.lastMove = None
        self.create()
        self.addPieces()

    def create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row,col)

    def calValidMoves(self, piece, row, col, calInCheck=True):
        """Calculate all posible valid moves for the given piece and position"""
        if piece.name == PAWN: 
            possibleMoves = [
                (row+piece.direction, col)
            ]
            if not piece.moved:
                possibleMoves.append((row+piece.direction*2, col))
            possibleCaptures = [
                (row+piece.direction, col-1), (row+piece.direction, col+1)
            ]
            obstacles = []

            for move in possibleCaptures:
                moveRow, moveCol = move

                if Square.inBounds(moveRow, moveCol):
                    if self.squares[moveRow][moveCol].hasRivalPiece(piece.color):
                        initialPos = Square(row, col)
                        finalPiece = self.squares[moveRow][moveCol].piece
                        finalPos = Square(moveRow, moveCol, finalPiece)
                        move = Move(initialPos, finalPos)
                        if calInCheck:
                            if not self.inCheck(piece, move):
                                #Add new move to piece
                                piece.addMove(move)
                        else:
                            piece.addMove(move)
            for move in possibleMoves:
                moveRow, moveCol = move
                check = True

                if Square.inBounds(moveRow, moveCol):
                    for obstacle in obstacles:
                        obstacleRow, obstacleCol = obstacle
                        if (row > obstacleRow):
                            if (moveRow < obstacleRow):
                                check = False
                                break
                        if (row < obstacleRow):
                            if (moveRow > obstacleRow):
                                check = False
                                break
                        if (col > obstacleCol):
                            if (moveCol < obstacleCol):
                                check = False
                                break
                        if (col < obstacleCol):
                            if (moveCol > obstacleCol):
                                check = False
                                break
                    if (check == False): #There is an obstacle in the way
                        continue

                    #Empty square
                    if self.squares[moveRow][moveCol].isEmpty():
                        initialPos = Square(row, col)
                        finalPos = Square(moveRow, moveCol)
                        m = Move(initialPos, finalPos)
                        if calInCheck:
                            if not self.inCheck(piece, m):
                                #Add new move to piece
                                piece.addMove(m)
                            else:
                                continue
                        else:
                            piece.addMove(m)
                    if self.squares[moveRow][moveCol].hasPiece():
                        obstacles.append(move)
        elif piece.name == KNIGHT:
            possibleMoves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1)
            ]

            for move in possibleMoves:
                moveRow, moveCol = move

                if Square.inBounds(moveRow, moveCol):
                    if self.squares[moveRow][moveCol].isEmptyOrRival(piece.color):
                        initialPos = Square(row, col)
                        finalPiece = self.squares[moveRow][moveCol].piece
                        finalPos = Square(moveRow, moveCol, finalPiece)
                        m = Move(initialPos, finalPos)
                        if calInCheck:
                            if not self.inCheck(piece, m):
                                #Add new move to piece
                                piece.addMove(m)
                            else:
                                continue
                        else:
                            piece.addMove(m)
        elif piece.name == ROOK:
            possibleMoves = [
                (row, col+1), (row, col+2), (row, col+3), (row, col+4), (row, col+5), (row, col+6), (row, col+7),
                (row, col-1), (row, col-2), (row, col-3), (row, col-4), (row, col-5), (row, col-6), (row, col-7),
                (row+1, col), (row+2, col), (row+3, col), (row+4, col), (row+5, col), (row+6, col), (row+7, col),
                (row-1, col), (row-2, col), (row-3, col), (row-4, col), (row-5, col), (row-6, col), (row-7, col),
            ]

            obstacles = []

            for move in possibleMoves:
                moveRow, moveCol = move
                check = True

                if Square.inBounds(moveRow, moveCol):
                    for obstacle in obstacles:
                        obstacleRow, obstacleCol = obstacle
                        if (row > obstacleRow):
                            if (moveRow < obstacleRow):
                                check = False
                                break
                        if (row < obstacleRow):
                            if (moveRow > obstacleRow):
                                check = False
                                break
                        if (col > obstacleCol):
                            if (moveCol < obstacleCol):
                                check = False
                                break
                        if (col < obstacleCol):
                            if (moveCol > obstacleCol):
                                check = False
                                break
                    if (check == False): #There is an obstacle in the way
                        continue

                    #Empty square
                    if self.squares[moveRow][moveCol].isEmpty():
                        initialPos = Square(row, col)
                        finalPos = Square(moveRow, moveCol)
                        m = Move(initialPos, finalPos)
                        if calInCheck:
                            if not self.inCheck(piece, m):
                                #Add new move to piece
                                piece.addMove(m)
                            else:
                                continue
                        else:
                            piece.addMove(m)

                    if self.squares[moveRow][moveCol].hasPiece():
                        #Rival square
                        if self.squares[moveRow][moveCol].hasRivalPiece(piece.color):
                            initialPos = Square(row, col)
                            finalPiece = self.squares[moveRow][moveCol].piece
                            finalPos = Square(moveRow, moveCol, finalPiece)
                            m = Move(initialPos, finalPos)
                            if calInCheck:
                                if not self.inCheck(piece, m):
                                    #Add new move to piece
                                    piece.addMove(m)
                                    #Add the square to obstacles
                                    obstacles.append(move)
                                else:
                                    continue
                            else:
                                piece.addMove(m)
                                obstacles.append(move)
                        #Ally square
                        if self.squares[moveRow][moveCol].hasAllyPiece(piece.color):
                            obstacles.append(move)
        elif piece.name == BISHOP:
            possibleMoves = [
                (row+1, col+1), (row+2, col+2), (row+3, col+3), (row+4, col+4), (row+5, col+5), (row+6, col+6), (row+7, col+7),
                (row+1, col-1), (row+2, col-2), (row+3, col-3), (row+4, col-4), (row+5, col-5), (row+6, col-6), (row+7, col-7),
                (row-1, col-1), (row-2, col-2), (row-3, col-3), (row-4, col-4), (row-5, col-5), (row-6, col-6), (row-7, col-7),
                (row-1, col+1), (row-2, col+2), (row-3, col+3), (row-4, col+4), (row-5, col+5), (row-6, col+6), (row-7, col+7),
            ]

            obstacles = []

            for move in possibleMoves:
                moveRow, moveCol = move
                check = True

                if Square.inBounds(moveRow, moveCol):
                    for obstacle in obstacles:
                        obstacleRow, obstacleCol = obstacle
                        obstacleVector = (obstacleRow - row, obstacleCol - col)
                        moveVector = (moveRow - row, moveCol - col)

                        if ((obstacleVector[0]*moveVector[0] + obstacleVector[1]*moveVector[1] > 0) and (abs(obstacleVector[0]) + abs(obstacleVector[1]) < abs(moveVector[0]) + abs(moveVector[1]))):
                            check = False
                            break
                        
                    if (check == False): #There is an obstacle in the way
                        continue

                    #Empty square
                    if self.squares[moveRow][moveCol].isEmpty():
                        initialPos = Square(row, col)
                        finalPos = Square(moveRow, moveCol)
                        m = Move(initialPos, finalPos)
                        if calInCheck:
                            if not self.inCheck(piece, m):
                                #Add new move to piece
                                piece.addMove(m)
                            else:
                                continue
                        else:
                            piece.addMove(m)

                    if self.squares[moveRow][moveCol].hasPiece():
                        #Rival square
                        if self.squares[moveRow][moveCol].hasRivalPiece(piece.color):
                            initialPos = Square(row, col)
                            finalPiece = self.squares[moveRow][moveCol].piece
                            finalPos = Square(moveRow, moveCol, finalPiece)
                            m = Move(initialPos, finalPos)
                            if calInCheck:
                                if not self.inCheck(piece, m):
                                    #Add new move to piece
                                    piece.addMove(m)
                                    #Add the square to obstacles
                                    obstacles.append(move)
                                else:
                                    continue
                            else:
                                piece.addMove(m)
                                obstacles.append(move)
                        #Ally square
                        if self.squares[moveRow][moveCol].hasAllyPiece(piece.color):
                            obstacles.append(move)
        elif piece.name == QUEEN:
            possibleMoves = [
                (row+1, col+1), (row+2, col+2), (row+3, col+3), (row+4, col+4), (row+5, col+5), (row+6, col+6), (row+7, col+7),
                (row+1, col-1), (row+2, col-2), (row+3, col-3), (row+4, col-4), (row+5, col-5), (row+6, col-6), (row+7, col-7),
                (row-1, col-1), (row-2, col-2), (row-3, col-3), (row-4, col-4), (row-5, col-5), (row-6, col-6), (row-7, col-7),
                (row-1, col+1), (row-2, col+2), (row-3, col+3), (row-4, col+4), (row-5, col+5), (row-6, col+6), (row-7, col+7),
                (row, col+1), (row, col+2), (row, col+3), (row, col+4), (row, col+5), (row, col+6), (row, col+7),
                (row, col-1), (row, col-2), (row, col-3), (row, col-4), (row, col-5), (row, col-6), (row, col-7),
                (row+1, col), (row+2, col), (row+3, col), (row+4, col), (row+5, col), (row+6, col), (row+7, col),
                (row-1, col), (row-2, col), (row-3, col), (row-4, col), (row-5, col), (row-6, col), (row-7, col)
            ]

            obstacles = []

            for move in possibleMoves:
                moveRow, moveCol = move
                check = True

                if Square.inBounds(moveRow, moveCol):
                    for obstacle in obstacles:
                        obstacleRow, obstacleCol = obstacle
                        obstacleVector = (obstacleRow - row, obstacleCol - col)
                        moveVector = (moveRow - row, moveCol - col)
                        rowDiff = float(moveVector[0]/obstacleVector[0]) if obstacleVector[0] != 0 else float(moveVector[1]/obstacleVector[1])
                        colDiff = float(moveVector[1]/obstacleVector[1]) if obstacleVector[1] != 0 else float(moveVector[0]/obstacleVector[0])
                        if (rowDiff == colDiff and rowDiff > 0 and colDiff > 0):
                            check = False
                            break
                    if (check == False): #There is an obstacle in the way
                        continue

                    #Empty square
                    if self.squares[moveRow][moveCol].isEmpty():
                        initialPos = Square(row, col)
                        finalPos = Square(moveRow, moveCol)
                        m = Move(initialPos, finalPos)
                        if calInCheck:
                            if not self.inCheck(piece, m):
                                #Add new move to piece
                                piece.addMove(m)
                            else:
                                continue
                        else:
                            piece.addMove(m)

                    if self.squares[moveRow][moveCol].hasPiece():
                        #Rival square
                        if self.squares[moveRow][moveCol].hasRivalPiece(piece.color):
                            initialPos = Square(row, col)
                            finalPiece = self.squares[moveRow][moveCol].piece
                            finalPos = Square(moveRow, moveCol, finalPiece)
                            m = Move(initialPos, finalPos)
                            if calInCheck:
                                if not self.inCheck(piece, m):
                                    #Add new move to piece
                                    piece.addMove(m)
                                    #Add the square to obstacles
                                    obstacles.append(move)
                                else:
                                    continue
                            else:
                                piece.addMove(m)
                                obstacles.append(move)
                        #Ally square
                        if self.squares[moveRow][moveCol].hasAllyPiece(piece.color):
                            obstacles.append(move)
        elif piece.name == KING:
            possibleMoves = [
                (row+1, col+1), 
                (row+1, col-1), 
                (row-1, col-1), 
                (row-1, col+1), 
                (row, col+1), 
                (row, col-1), 
                (row+1, col),
                (row-1, col)
            ]

            obstacles = []

            for move in possibleMoves:
                moveRow, moveCol = move
                check = True

                if Square.inBounds(moveRow, moveCol):
                    for obstacle in obstacles:
                        obstacleRow, obstacleCol = obstacle
                        if (row > obstacleRow):
                            if (moveRow < obstacleRow):
                                check = False
                                break
                        if (row < obstacleRow):
                            if (moveRow > obstacleRow):
                                check = False
                                break
                        if (col > obstacleCol):
                            if (moveCol < obstacleCol):
                                check = False
                                break
                        if (col < obstacleCol):
                            if (moveCol > obstacleCol):
                                check = False
                                break
                    if (check == False): #There is an obstacle in the way
                        continue

                    #Empty square
                    if self.squares[moveRow][moveCol].isEmpty():
                        initialPos = Square(row, col)
                        finalPos = Square(moveRow, moveCol)
                        m = Move(initialPos, finalPos)
                        if calInCheck:
                            if not self.inCheck(piece, m):
                                #Add new move to piece
                                piece.addMove(m)
                            else:
                                continue
                        else:
                            piece.addMove(m)

                    if self.squares[moveRow][moveCol].hasPiece():
                        #Rival square
                        if self.squares[moveRow][moveCol].hasRivalPiece(piece.color):
                            initialPos = Square(row, col)
                            finalPiece = self.squares[moveRow][moveCol].piece
                            finalPos = Square(moveRow, moveCol, finalPiece)
                            m = Move(initialPos, finalPos)
                            if calInCheck:
                                if not self.inCheck(piece, m):
                                    #Add new move to piece
                                    piece.addMove(m)
                                    #Add the square to obstacles
                                    obstacles.append(move)
                                else:
                                    continue
                            else:
                                piece.addMove(m)
                                obstacles.append(move)
                        #Ally square
                        if self.squares[moveRow][moveCol].hasAllyPiece(piece.color):
                            obstacles.append(move)
            if not piece.moved:
                #King castling
                leftRook = self.squares[row][0].piece if piece.color == WHITE else self.squares[0][0].piece
                rookRow = row if piece.color == WHITE else 0
                if isinstance(leftRook, Rook):
                    if not leftRook.moved:
                        for i in range(1,4):
                            if self.squares[rookRow][i].hasPiece(): #There are pieces between king and rook
                                break
                            if i == 3:
                                piece.leftRook = leftRook
                                #Rook move
                                initialPos = Square(rookRow, 0)
                                finalPos = Square(rookRow, 3)
                                move = Move(initialPos, finalPos)
                                if calInCheck:
                                    if not self.inCheck(leftRook, move):
                                        leftRook.addMove(move)
                                else:
                                    leftRook.addMove(move)
                                #King move
                                initialPos = Square(rookRow, col)
                                finalPos = Square(rookRow, 2)
                                move = Move(initialPos, finalPos)
                                if calInCheck:
                                    if not self.inCheck(piece, move):
                                        piece.addMove(move)
                                else:
                                    piece.addMove(move)
                #Queen castling
                rightRook = self.squares[row][7].piece if piece.color == WHITE else self.squares[0][7].piece
                rookRow = row if piece.color == WHITE else 0
                if isinstance(rightRook, Rook):
                    if not rightRook.moved:
                        for i in range(5,7):
                            if self.squares[rookRow][i].hasPiece(): #There are pieces between king and rook
                                break
                            if i == 6:
                                piece.rightRook = rightRook
                                #Rook move
                                initialPos = Square(rookRow, 7)
                                finalPos = Square(rookRow, 5)
                                move = Move(initialPos, finalPos)
                                if calInCheck:
                                    if not self.inCheck(rightRook, move):
                                        rightRook.addMove(move)
                                else:
                                    rightRook.addMove(move)
                                #King move
                                initialPos = Square(rookRow, col)
                                finalPos = Square(rookRow, 6)
                                move = Move(initialPos, finalPos)
                                if calInCheck:
                                    if not self.inCheck(piece, move):
                                        piece.addMove(move)
                                else:
                                    piece.addMove(move)
    def isValidMove(self, piece, move):
        return move in piece.moves
    def checkPawnPromotion(self, piece, finalPos):
        if finalPos.row == 0 or finalPos.row == 7:
            self.squares[finalPos.row][finalPos.col].piece = Queen(piece.color)
    def castling(self, initialPos, finalPos):
        return abs(initialPos.col - finalPos.col) == 2
    def inCheck(self, piece, move):
        tempBoard = copy.deepcopy(self)
        tempPiece = copy.deepcopy(piece)
        tempBoard.move(tempPiece, move, checking=True)

        for row in range(ROWS):
            for col in range(COLS):
                if tempBoard.squares[row][col].hasRivalPiece(tempPiece.color):
                    rivalPiece = tempBoard.squares[row][col].piece
                    tempBoard.calValidMoves(rivalPiece, row, col, False)
                    for m in rivalPiece.moves:
                        if isinstance(m.finalPos.piece, King) and m.finalPos.piece.color == tempPiece.color:
                            return True
        return False
    def isStalemate(self, color):
        tempBoard = copy.deepcopy(self)
        for row in range(ROWS):
            for col in range(COLS):
                if tempBoard.squares[row][col].hasAllyPiece(color):
                    piece = tempBoard.squares[row][col].piece
                    tempBoard.calValidMoves(piece, row, col)
                    if len(piece.moves) != 0:
                        return False
        return True
    def addPieces(self):
        #Add white pieces
        #Pawns
        for col in range(COLS):
            self.squares[6][col] = Square(6, col, Pawn(WHITE))
        #Rooks
        self.squares[7][0] = Square(7, 0, Rook(WHITE))
        self.squares[7][7] = Square(7, 7, Rook(WHITE))
        #Knights
        self.squares[7][1] = Square(7, 1, Knight(WHITE))
        self.squares[7][6] = Square(7, 6, Knight(WHITE))
        #Bishops
        self.squares[7][2] = Square(7, 2, Bishop(WHITE))
        self.squares[7][5] = Square(7, 5, Bishop(WHITE))
        #Queen
        self.squares[7][3] = Square(7, 3, Queen(WHITE))
        #King
        self.squares[7][4] = Square(7, 4, King(WHITE))
        
        #Add black pieces
        #Pawns
        for col in range(COLS):
            self.squares[1][col] = Square(1, col, Pawn(BLACK))
        #Rooks
        self.squares[0][0] = Square(0, 0, Rook(BLACK))
        self.squares[0][7] = Square(0, 7, Rook(BLACK))
        #Knights
        self.squares[0][1] = Square(0, 1, Knight(BLACK))
        self.squares[0][6] = Square(0, 6, Knight(BLACK))
        #Bishops
        self.squares[0][2] = Square(0, 2, Bishop(BLACK))
        self.squares[0][5] = Square(0, 5, Bishop(BLACK))
        #Queen
        self.squares[0][3] = Square(0, 3, Queen(BLACK))
        #King
        self.squares[0][4] = Square(0, 4, King(BLACK))
    
    def move(self, piece, move, checking=False):
        initialPos = move.initialPos
        finalPos = move.finalPos

        self.squares[initialPos.row][initialPos.col].piece = None
        self.squares[finalPos.row][finalPos.col].piece = piece

        #Pawn promotion
        if isinstance(piece, Pawn):
            self.checkPawnPromotion(piece, finalPos)
        piece.moved = True
        piece.clearMoves()

        if isinstance(piece, King):
            if self.castling(initialPos, finalPos) and not checking:
                diff = finalPos.col - initialPos.col
                rook = piece.leftRook if diff < 0 else piece.rightRook
                self.move(rook, rook.moves[-1])
        self.lastMove = move
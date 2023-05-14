import pygame
from constants import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
from aimodel import AIModel

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.model = AIModel()
        self.config = Config()
        self.next_player = WHITE
        self.hovered_sqr = None
        self.gameover = False
        self.gamemode = PVP

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (204, 102, 0) #Dark brown
                else:
                    color = (255, 204, 153) #Light brown
                
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                #Show position markers
                if col == 0:
                    color = (204, 102, 0) if (row + col) % 2 != 0 else (255, 204, 153)
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    labelPos = (5, 5 + row * SQSIZE)
                    surface.blit(lbl, labelPos)
                if row == 7:
                    color = (204, 102, 0) if (row + col) % 2 != 0 else (255, 204, 153)
                    lbl = self.config.font.render(Square.getAlphaCol(col), 1, color)
                    labelPos = (col *SQSIZE+SQSIZE-20, HEIGHT-20)
                    surface.blit(lbl, labelPos)
                #Show current gamemode
                color = '#ff1a1a'
                mode = "Mode:PvP" if self.gamemode == PVP else "Mode:PvE"
                lbl = self.config.modeFont.render(mode, 1, color)
                labelPos = ((COLS - 1)*SQSIZE-20, 5) #Top-right corner
                surface.blit(lbl, labelPos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].hasPiece():
                    piece = self.board.squares[row][col].piece
                    
                    if piece is not self.dragger.piece:
                        piece.setTexture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                color = "#99cc00" if ((move.finalPos.row + move.finalPos.col) % 2 != 0) else "#86b300" #Pick the first color if the final square is a brighter-colored one
                rect = (move.finalPos.col * SQSIZE, move.finalPos.row * SQSIZE, SQSIZE, SQSIZE)
                #Draw the rect
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.lastMove:
            initialPos = self.board.lastMove.initialPos
            finalPos = self.board.lastMove.finalPos

            for pos in [initialPos, finalPos]:
                color = (244, 247, 116) if (pos.row + pos.col) % 2 != 0 else (172, 195, 51)
                rect = (pos.col*SQSIZE, pos.row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface,color,rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col*SQSIZE, self.hovered_sqr.row*SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=4)
    
    def show_game_over(self, surface, pieceColor):
        pieceColor = 'White' if pieceColor == BLACK else 'Black'
        rectColor = "#00001a"
        rect = (0, 3*SQSIZE, 8*SQSIZE, 2*SQSIZE)
        pygame.draw.rect(surface, rectColor, rect)
        textColor = "#f2f2f2"
        lbl1 = self.config.font.render('Game Over.'+pieceColor+' won.', 1, textColor)
        lbl2 = self.config.font.render('Press R to restart.', 1, textColor)
        lbl1Pos = (3*SQSIZE, 4*SQSIZE-20)
        lbl2Pos = (3*SQSIZE, 4*SQSIZE+20)
        surface.blit(lbl1, lbl1Pos)
        surface.blit(lbl2, lbl2Pos)

    def play_sound(self, isCaptured=False):
        if isCaptured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def next_turn(self):
        self.next_player = WHITE if self.next_player == BLACK else BLACK

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]
    
    def change_modes(self):
        self.gamemode = PVP if self.gamemode == PVE else PVE

    def reset(self):
        self.__init__()
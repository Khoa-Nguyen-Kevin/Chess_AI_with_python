import pygame
from constants import *

class Dragger:
    
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initialRow = 0
        self.initialCol = 0

    def updateBlit(self, surface):
        #Set texture
        self.piece.setTexture(size=128)
        texture = self.piece.texture

        #Prepare the img
        img = pygame.image.load(texture)
        imgCenter = (self.mouseX,self.mouseY)
        self.piece.texture_rect = img.get_rect(center=imgCenter)
        
        surface.blit(img, self.piece.texture_rect)
    def updateMouse(self, pos):
        self.mouseX, self.mouseY = pos

    def saveInitial(self, pos):
        self.initialCol = pos[0] // SQSIZE
        self.initialRow = pos[1] // SQSIZE

    def dragPiece(self, piece):
        self.piece = piece
        self.dragging = True
    
    def dropPiece(self):
        self.piece = None
        self.dragging = False
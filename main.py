#Credit: https://github.com/AlejoG10/python-chess-ai-yt
#Thank you to Alejo for the original source code!!!

import pygame
import sys
from constants import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
        pygame.display.set_caption("Chess AI")
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_hover(screen)
            game.show_pieces(screen)
            if game.gameover:
                game.show_game_over(screen, game.next_player)
            if dragger.dragging:
                dragger.updateBlit(screen)


            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.updateMouse(event.pos)
                    eventRow = dragger.mouseY // SQSIZE
                    eventCol = dragger.mouseX // SQSIZE

                    if board.squares[eventRow][eventCol].hasPiece():
                        piece = board.squares[eventRow][eventCol].piece
                        if piece.color == game.next_player:
                            board.calValidMoves(piece, eventRow, eventCol, True)
                            dragger.saveInitial(event.pos)
                            dragger.dragPiece(piece)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    game.set_hover(event.pos[1] // SQSIZE, event.pos[0] // SQSIZE)
                    if game.gameover:
                        dragger.dropPiece()
                    if dragger.dragging:
                        dragger.updateMouse(event.pos)
                        #We call show_bg and show_pieces again to ensure there's no "image residue" when dragging the piece
                        #But this has shown to create a slight lag between the cursor and the dragged piece image
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_hover(screen)
                        game.show_pieces(screen)
                        dragger.updateBlit(screen)
                        if game.gameover:
                            game.show_game_over(screen, game.next_player)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.updateMouse(event.pos)
                        droppedRow = dragger.mouseY // SQSIZE
                        droppedCol = dragger.mouseX // SQSIZE
                        initialPos = Square(dragger.initialRow,dragger.initialCol)
                        finalPos = Square(droppedRow, droppedCol)
                        move = Move(initialPos, finalPos)

                        if board.isValidMove(dragger.piece, move):
                            isCaptured = board.squares[droppedRow][droppedCol].hasPiece()
                            board.move(dragger.piece, move)
                            game.next_turn()
                            game.play_sound(isCaptured)
                            #Show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            if board.isStalemate(game.next_player):
                                game.gameover = True
                                game.show_game_over(screen, game.next_player)
                        dragger.piece.clearMoves()

                    dragger.dropPiece()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: #Restart the board
                        game.reset()
                        game = self.game
                        screen = self.screen
                        dragger = self.game.dragger
                        board = self.game.board

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.mainloop()

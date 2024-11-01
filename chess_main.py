
import pygame as pg
import chess_engine


WIDTH = HEIGHT = 512
DIMENSION = 8
MAX_FPS = 28
SQUARE_SIZE = HEIGHT // DIMENSION
IMAGES = {}

def loadImages():
    pieces = ['wQ','wK','wP','wR','wN','bQ','bK','bP','bR','bN','bs','ws',"wgL","wgR","bgL","bgR"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(f"./images/{piece}.png") , (SQUARE_SIZE , SQUARE_SIZE))

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH , HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color('white'))

    gs = chess_engine.GameState()
    loadImages()

    validMoves = gs.getValidMoves()
    moveMade = False 

    squareSelected = () 
    playerClicks = []
    running = True
    gameOver = False
    playerOne = True 
    playerTwo = True
    while running:

        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN: 
                if not gameOver and humanTurn:
                    location = pg.mouse.get_pos() 
                    col = location[0]//SQUARE_SIZE
                    row = location[1]//SQUARE_SIZE
                    if squareSelected == (row, col): 
                        squareSelected = ()
                        playerClicks = []
                    else:
                        squareSelected = (row, col)
                        playerClicks.append(squareSelected)
                    
                    if  len(playerClicks) == 2:
                        move = chess_engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                squareSelected = ()
                                playerClicks = []
                                break
                        
                        if not moveMade:
                            playerClicks = [squareSelected]
            elif e.type == pg.KEYDOWN:    
                if e.key == pg.K_z:  
                    gs.undoMove()
                    gs.undoMove()
                    moveMade = True
                    gameOver = False
                elif e.key == pg.K_r: 
                    gs = chess_engine.GameState()
                    validMoves = gs.getValidMoves()
                    squareSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False


        if moveMade:
            validMoves = gs.getValidMoves()

            moveMade = False

        drawGameState(screen , gs, validMoves, squareSelected)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Каралар утту ")
            else:
                drawText(screen, "Актар утту ")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "PAT")

        clock.tick(MAX_FPS )
        pg.display.flip()



def drawGameState(screen , gs, validMoves, squareSelected):
    drawBoard(screen) 
    highlightSquares(screen, gs, validMoves, squareSelected)
    drawPieces(screen , gs.board) 



def drawBoard(screen):
    global colors
    colors = [pg.Color('white') , pg.Color('gray')]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row+col)%2]
            pg.draw.rect(screen , color , pg.Rect(col*SQUARE_SIZE , row*SQUARE_SIZE , SQUARE_SIZE , SQUARE_SIZE))



def drawPieces(screen , board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--": 
                screen.blit(IMAGES[piece] , pg.Rect(col*SQUARE_SIZE , row*SQUARE_SIZE , SQUARE_SIZE , SQUARE_SIZE))


def highlightSquares(screen, gs, validMoves, squareSelected):
    if squareSelected != ():
        row, col = squareSelected
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'):  
            pg.draw.rect(screen, pg.Color('yellow'), pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

            surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
            surface.set_alpha(100) 
            screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    center = (move.endCol * SQUARE_SIZE + SQUARE_SIZE // 2,
                              move.endRow * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pg.draw.circle(screen, pg.Color("green"), center, SQUARE_SIZE // 6)



def drawText(screen, text):
    font = pg.font.SysFont("arial", 36, True, False)
    textObject = font.render(text, 0, pg.Color("red"))
    textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()
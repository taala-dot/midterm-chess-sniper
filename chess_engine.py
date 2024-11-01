
class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bgL", "bQ", "bK", "bgR", "bN", "bR"],
            ["bs", "bP", "bP", "bP", "bP", "bP", "bP", "bs"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["ws", "wP", "wP", "wP", "wP", "wP", "wP", "ws"],
            ["wR", "wN", "wgL", "wQ", "wK", "wgL", "wN", "wR"]
        ]
        self.moveFunctions = {'P' : self.getPawnMoves, 'R' : self.getRookMoves, 'N' : self.getKnightMoves,
         'B' : self.getBishopMoves, 'Q' : self.getQueenMoves, 'K' : self.getKingMoves,'g':self.getGooseMoves,'s':self.getSniperTargets}
        self.whiteToMove = True
        self.movesLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enPassantPossible = () 
        self.checkmate = False
        self.sniperUsed = {'w': False, 'b': False} 
        self.stalemate = False
        self.currCastlingRight = castleRights(True , True , True , True)
        self.castlingRightLog = [castleRights(self.currCastlingRight.wks , self.currCastlingRight.bks,
                                              self.currCastlingRight.wqs , self.currCastlingRight.bqs)]


    def makeMove(self, move):
        if move.pieceCaptured[1] == 's':
            print("Снайпера нельзя съесть!")
            return False
        if move.pieceMoved[1] == 's':
            color = move.pieceMoved[0]  
            if self.sniperUsed[color]:  
                print("Бир эле жолу колдонсо болот")
                return
        if move.pieceMoved[1] == 's':
            target_row, target_col = move.endRow, move.endCol
            if move.pieceCaptured != "--":
                self.board[target_row][target_col] = "--" 
            self.sniperUsed[move.pieceMoved[0]] = True
            self.movesLog.append(move)  
            self.selectedPiece = None
            return
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movesLog.append(move) 
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = "--"
        if move.pieceMoved[1] == 'P' and abs(move.startRow-move.endRow) == 2:
            self.enPassantPossible = ((move.startRow+move.endRow//2), move.startCol)
        else :
            self.enPassantPossible = ()
         #rokirovka
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] =  self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'
        self.updateCastleRights(move)
        self.castlingRightLog.append(castleRights(self.currCastlingRight.wks , self.currCastlingRight.bks,
                                              self.currCastlingRight.wqs , self.currCastlingRight.bqs))

    def updateCastleRights(self , move):
        if move.pieceMoved == 'bK':
            self.currCastlingRight.bqs = False
            self.currCastlingRight.bks = False
        elif move.pieceMoved == 'wK':
            self.currCastlingRight.wks = False
            self.currCastlingRight.wqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: 
                    self.currCastlingRight.wqs = False
                elif move.startCol == 7: 
                    self.currCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: # ferz
                    self.currCastlingRight.bqs = False
                elif move.startCol == 7: # korol
                    self.currCastlingRight.bks = False

 
    def undoMove(self):
        if len(self.movesLog) != 0:
            move = self.movesLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow, move.endCol)
            
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()

            self.castlingRightLog.pop()
            self.currCastlingRight = self.castlingRightLog[-1]
            
            if move.isCastleMove:
                if move.endCol - move.startCol == 2 :
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

            self.checkmate = False
            self.stalemate = False

    def getValidMoves(self):
        tempEnPassantPossible = self.enPassantPossible
        tempCastleRights = castleRights(self.currCastlingRight.wks , self.currCastlingRight.bks,
                                        self.currCastlingRight.wqs , self.currCastlingRight.bqs)
        moves = []
        self.inCheck , self.pins , self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        
        if self.inCheck:
            if len(self.checks) == 1: 
                moves = self.getAllPossibleMoves()
                if self.whiteToMove:
                    self.getCastleMoves(self.whiteKingLocation[0] , self.whiteKingLocation[1] , moves)  
                else:
                    self.getCastleMoves(self.blackKingLocation[0] , self.blackKingLocation[1] , moves)
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = [] 
                if pieceChecking == 'N': 
                    validSquares = [(checkRow , checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i , kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1 , -1 , -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow , moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: 
                self.getKingMoves(kingRow , kingCol , moves)
        else:
            moves = self.getAllPossibleMoves()
            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0] , self.whiteKingLocation[1] , moves)  
            else:
                self.getCastleMoves(self.blackKingLocation[0] , self.blackKingLocation[1] , moves)
        self.enPassantPossible = tempEnPassantPossible
        self.currCastlingRight = tempCastleRights
        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True

        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    def squareUnderAttack(self, row, col):
        if self.board[row][col][1] == 's':
            return False
        self.whiteToMove = not self.whiteToMove 
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove 
        for move in oppMoves:
            if self.board[row][col][1] == 's':
                return False
            if move.endRow == row and move.endCol == col: 
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'b' and not self.whiteToMove) or (turn == 'w' and self.whiteToMove):
                    piece = self.board[row][col][1]
                    if piece == 'g':
                        self.getGooseMoves(row, col, moves, self.board[row][col])
                    elif piece == 's' and not self.sniperUsed[turn]:  
                        self.getSniperTargets(row, col, moves)
                    else:
                        self.moveFunctions[piece](row, col, moves)

        return moves

    def getPawnMoves(self , row , col , moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1 , -1 , -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2] , self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            if row-1 >=0 and self.board[row-1][col] == "--":
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((row, col), (row-1, col), self.board))
                    if row == 6 and self.board[row-2][col] == "--": 
                        moves.append(Move((row, col), (row-2, col), self.board))
            
            if col-1 >=0 and self.board[row-1][col-1][0] == 'b': 
                if not piecePinned or pinDirection == (-1,-1):
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            elif (row-1, col-1) == self.enPassantPossible:
                moves.append(Move((row, col), (row-1, col-1), self.board, isEnPassantMove = True))


            if col+1 < 8 and self.board[row-1][col+1][0] == 'b':  
                if not piecePinned or pinDirection == (-1,1):
                    moves.append(Move((row, col), (row-1, col+1), self.board))
            elif (row-1, col+1) == self.enPassantPossible:
                moves.append(Move((row, col), (row-1, col+1), self.board, isEnPassantMove = True))
                 
        else: 
            if row+1 < 8 and self.board[row+1][col] == "--": 
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((row, col), (row+1, col), self.board))
                    if row == 1 and self.board[row+2][col] == "--": 
                        moves.append(Move((row, col), (row+2, col), self.board))
            
            if col-1 >=0 and self.board[row+1][col-1][0] == 'w': 
                if not piecePinned or pinDirection == (1,-1):
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            elif (row+1, col-1) == self.enPassantPossible:
                moves.append(Move((row, col), (row+1, col-1), self.board, isEnPassantMove = True))

            if col+1 < 8 and self.board[row+1][col+1][0] == 'w':  
                if not piecePinned or pinDirection == (1,1):
                    moves.append(Move((row, col), (row+1, col+1), self.board))
            elif (row+1, col+1) == self.enPassantPossible:
                moves.append(Move((row, col), (row+1, col+1), self.board, isEnPassantMove = True))
            

    def getRookMoves(self , row , col ,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1 , -1 , -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2] , self.pins[i][3])
                if self.board[row][col][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        directions = [(-1,0) , (1,0) , (0,-1) , (0,1)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = row + d[0]*i
                endCol = col + d[1]*i
                if endRow>=0 and endRow<8 and endCol>=0 and endCol<8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0] , -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((row,col) , (endRow , endCol) , self.board))
                        elif endPiece[0] == enemyColor:   
                            moves.append(Move((row,col) , (endRow , endCol) , self.board))
                            break
                        else: 
                            break
                else:
                    break


    def getKnightMoves(self , row , col ,moves):
        piecePinned = False
        for i in range(len(self.pins) - 1 , -1 , -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = [(-2,-1) , (-2,1) , (2,-1) , (2,1) , (1,2) , (1,-2) , (-1,2) , (-1,-2)]
        ourColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = row + m[0]
            endCol = col + m[1]
            if endRow>=0 and endRow<8 and endCol>=0 and endCol<8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != ourColor:
                        moves.append(Move((row,col) , (endRow , endCol) , self.board))


    def getBishopMoves(self , row , col ,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1 , -1 , -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2] , self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = [(-1,-1) , (-1,1) , (1,-1) , (1,1)] 
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = row + d[0]*i
                endCol = col + d[1]*i
                if endRow>=0 and endRow<8 and endCol>=0 and endCol<8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0] , -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((row,col) , (endRow , endCol) , self.board))
                        elif endPiece[0] == enemyColor:  
                            moves.append(Move((row,col) , (endRow , endCol) , self.board))
                            break
                        else: 
                            break
                else:
                    break
    def getQueenMoves(self , row , col ,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1 , -1 , -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2] , self.pins[i][3])
                if self.board[row][col][1] != 'Q': 
                    self.pins.remove(self.pins[i])
                break

        directions = [(-1,0) , (1,0) , (0,-1) , (0,1)]
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = row + d[0]*i
                endCol = col + d[1]*i
                if endRow>=0 and endRow<8 and endCol>=0 and endCol<8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0] , -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((row,col) , (endRow , endCol) , self.board))
                        elif endPiece[0] == enemyColor:  
                            moves.append(Move((row,col) , (endRow , endCol) , self.board))
                            break
                        else: 
                            break
                else:
                    break
        for i in range(len(self.pins) - 1 , -1 , -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2] , self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        directions = [(-1,-1) , (-1,1) , (1,-1) , (1,1)]  
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = row + d[0]*i
                endCol = col + d[1]*i
                if endRow>=0 and endRow<8 and endCol>=0 and endCol<8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0] , -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((row,col) , (endRow , endCol) , self.board))
                        elif endPiece[0] == enemyColor:   
                            moves.append(Move((row,col) , (endRow , endCol) , self.board))
                            break
                        else:
                            break
                else:
                    break




    def getKingMoves(self , row , col ,moves):
        rowMoves = [-1,-1,-1,0,0,1,1,1]
        colMoves = [-1,0,1,-1,1,-1,0,1]
        ourColor = 'w' if self.whiteToMove else 'b'
        for m in range(8):
            endRow = row + rowMoves[m]
            endCol = col + colMoves[m]
            if endRow>=0 and endRow<8 and endCol>=0 and endCol<8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ourColor:
                    if ourColor == 'w':
                        self.whiteKingLocation = (endRow , endCol)
                    else:
                        self.blackKingLocation = (endRow , endCol)
                    inCheck , pins , checks = self.checkForPinsAndChecks()

                    if not inCheck:
                        moves.append(Move((row,col) , (endRow , endCol) , self.board))

                    if ourColor == 'w':
                        self.whiteKingLocation = (row , col)
                    else:
                        self.blackKingLocation = (row , col)

    def getSniperTargets(self, r, c, moves):
        color = self.board[r][c][0]
        target_color = 'b' if color == 'w' else 'w'
        targets = ['P', 'N', 'g'] 
        for target_row in range(8):
            for target_col in range(8):
                piece = self.board[target_row][target_col]
                if piece != "--" and piece[0] == target_color and piece[1] in targets:
                    moves.append(Move((r, c), (target_row, target_col), self.board)) 

    def getGooseMoves(self, r, c, moves, gooseType):
        color = self.board[r][c][0]

        directions = []
        if gooseType == "wgL":
            directions = [(-2, 0), (0, -2), (1, -1), (-1, -1), (0, 2), (-1, 1)]
        elif gooseType == "wgR":
            directions = [(-2, 0), (0, 2), (-1, -1), (0, -2), (1, 1)]
        elif gooseType == "bgL":
            directions = [(2, 0), (0, -2), (1, -1), (-1, -1), (0, -2), (1, 1), (0, 2)]
        elif gooseType == "bgR":
            directions = [(2, 0), (0, 2), (1, 1), (1, -1), (0, -2), (-1, -1)]

        for dr, dc in directions:
            new_r = r + dr
            new_c = c + dc
            if 0 <= new_r < 8 and 0 <= new_c < 8:
                if self.board[new_r][new_c] == "--":
                    moves.append(Move((r, c), (new_r, new_c), self.board))
                elif self.board[new_r][new_c][0] != color:
                    moves.append(Move((r, c), (new_r, new_c), self.board))

    def getCastleMoves(self , row , col , moves):
        if self.squareUnderAttack(row , col , ):
            return 
        if (self.whiteToMove and self.currCastlingRight.wks) or (not self.whiteToMove and self.currCastlingRight.bks):
            self.getKingSideCastleMoves(row , col , moves)
        
        if (self.whiteToMove and self.currCastlingRight.wqs) or (not self.whiteToMove and self.currCastlingRight.bqs):
            self.getQueenSideCastleMoves(row , col , moves)
    
    def getKingSideCastleMoves(self , row , col , moves):
        if self.board[row][col+1] == '--' and self.board[row][col+2] == '--':
            if not self.squareUnderAttack(row , col + 1) and not self.squareUnderAttack(row , col+2):
                moves.append(Move((row , col) , (row , col + 2) , self.board , isCastleMove = True))

    def getQueenSideCastleMoves(self , row , col , moves):
        if self.board[row][col-1] == '--' and self.board[row][col-2] == '--' and self.board[row][col-3]:
            if not self.squareUnderAttack(row , col - 1) and not self.squareUnderAttack(row , col - 2):
                moves.append(Move((row , col) , (row , col - 2) , self.board , isCastleMove = True))


    
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            ourColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            ourColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        
        directions = [(-1,0) , (0,-1) , (1,0) , (0,1) , (-1,-1) , (-1,1) , (1,-1) , (1,1)]
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if endRow>=0 and endRow<8 and endCol>=0 and endCol<8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == ourColor and endPiece[1] != 'K':
                        if possiblePin == (): 
                            possiblePin = (endRow , endCol , d[0] , d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                       
                        if (0<=j<=3 and type == 'R') or (4<=j<=7 and type == 'B') or (i == 1  and type == 'P' and ((enemyColor == 'b' and 4<=j<=5) or (enemyColor == 'w' and 6<=j<=7))) or (type == 'Q') or (i==1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow , endCol , d[0] , d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break 
                else: 
                    break
        
        knightMoves = [(-2,-1) , (-2 , 1) , (2,-1) , (2,1) , (-1,2) , (1,2) ,(1,-2) , (-1,-2)]
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if endRow>=0 and endRow<8 and endCol>=0 and endCol<8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow ,endCol , m[0] , m[1]))
        return inCheck , pins , checks
    
class castleRights():
    def __init__(self, wks , bks , wqs , bqs) -> None:
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
    

class Move():

    ranksToRows = {"8" : 0, "7" : 1, "6" : 2, "5" : 3, "4" : 4, "3" : 5, "2" : 6, "1" : 7}
    rowsToRanks = {rows : ranks for ranks, rows in ranksToRows.items()}

    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    colsToFiles = {cols : files for files, cols in filesToCols.items()}


    def __init__(self, startSquare, endSquare, board, isEnPassantMove = False , isCastleMove = False):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
        self.isPawnPromotion = (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7)
        
        self.isCastleMove = isCastleMove

        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"
        if self.pieceMoved[1] == 's':
            self.isAttackOnly = True
        else:
            self.isAttackOnly = False

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, o: object) -> bool:
        if isinstance(o , Move):
            return self.moveID == o.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]

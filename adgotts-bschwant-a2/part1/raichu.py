#
# raichu.py : Play the game of Raichu
#
# Andrew Gotts (adgotts), Brian Schwantes (bschwant)
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import numpy as np

def np2string(npmat):
    ''' Converts a numpy matrix to a string'''
    
    np2Dls = npmat.tolist()
    npls = [ y for x in np2Dls for y in x]
    npstr = ''.join(npls)
    return npstr

def string2np(board_str, N):
    ''' Given a board string and the size of the board ... convert it to a numpy matrix'''
    boardls = list(board_str)
    board = np.array(boardls).reshape(N,N)
    return board

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

class pichus:
    ''' Returns all possible moves for pichus'''
    def __init__(self, pichuls, player, player_raichu, enemy, enemy_raichu, board) -> None:
        self.board = board
        self.locationls = pichuls
        self.player = player.lower()
        self.player_raichu = player_raichu
        self.enemy_pichu = enemy.lower()
        self.enemy_pika = enemy.upper()
        self.enemy_raichu = enemy_raichu
        self.N = len(board)
        self.successors = []
    
    def valid_moves(self):
        ''' Append all valid possible moves for a pichu to successors []'''
        
        # Used to flip logic depending on the color of the player
        moveval = 1
        if self.player == 'b':
            moveval = -1
        
        # Find successors for each pichu on board
        for pichu in self.locationls:
            row = pichu[0]
            coll = pichu[1]

            self.move_right_diag(np.copy(self.board), row, coll, moveval, flag = 1) # flag for calculating opposite set of diagonals
            self.move_right_diag(np.copy(self.board), row, coll, moveval, flag = -1)

        return self.successors
    
    def raichu_upgrade(self, rmove):
        ''' Check to see if the new move warrants an upgrade to a raichu'''
        
        if (rmove == 0 or rmove == (self.N-1)): # Raichu Upgrade
            return self.player_raichu
        else:
            return self.player

    def move_right_diag(self, board, row, coll, moveval, flag):
        ''' Find the valid pichu moves for .. w = down -> right, b = up ->left'''
        try:
            assert(0 <= row+moveval < self.N) # Check for edges
            assert(0 <= coll+(moveval*flag) < self.N)

            board[row,coll] = '.'

            player = self.raichu_upgrade(row+moveval)

            if board[row+moveval,coll+(moveval*flag)] == '.':
                board[row+moveval,coll+(moveval*flag)] = player
                self.successors.append(np2string(board))
            elif board[row+moveval,coll+(moveval*flag)] == self.enemy_pichu and board[row+(2*moveval),coll+(2*moveval*flag)] == '.':
                assert(0 <= row+(2*moveval) < self.N) # Check for end of board
                assert(0 <= coll+(2*moveval*flag) < self.N) # Check for edges

                player = self.raichu_upgrade(row+(2*moveval))
                board[row+moveval,coll+(moveval*flag)] = '.'
                board[row+(2*moveval),coll+(2*moveval*flag)] = player
                self.successors.append(np2string(board))
        
        except (AssertionError, IndexError):
            pass

class pikachus:
    ''' Returns all possible moves for pikachus'''
    def __init__(self, pikals, player, player_raichu, enemy, enemy_raichu, board) -> None:
        self.board = board
        self.locationls = pikals
        self.player = player.upper()
        self.player_raichu = player_raichu
        self.enemy_pichu = enemy.lower()
        self.enemy_pika = enemy.upper()
        self.enemy_raichu = enemy_raichu
        self.N = len(board)
        self.successors = []
    
    def valid_moves(self):
        ''' Append all valid possible moves for a pikachu to self.successors []'''
               
        # Find successors for each pichu on board
        for pichu in self.locationls:
            row = pichu[0]
            coll = pichu[1]
            
            if self.player == 'B':
                self.move_U(np.copy(self.board), row, coll) # move up
            else:
                self.move_D(np.copy(self.board), row, coll) # move down
            self.move_L(np.copy(self.board), row, coll) # move left
            self.move_R(np.copy(self.board), row, coll) # move right


        return self.successors
    
    def raichu_upgrade(self, rmove):
        ''' Check to see if the new move warrants an upgrade to a raichu'''
        
        if (rmove == 0 or rmove == (self.N -1)): # Raichu Upgrade
            return self.player_raichu
        else:
            return self.player

    def move_U(self, board, row, coll):
        ''' Find the valid up pikachu moves for W and B'''

        cmove = coll # We will not be moving colls
        board[row,coll] = '.' # Delete the pikachu at og location

        for i in range(1,3):
            
            rmove = row-i
            if rmove < 0 or rmove >= self.N: # Edge has been hit
                break
            
            player = self.raichu_upgrade(rmove)

            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = player
                self.successors.append(np2string(newboard))                
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika):                
                
                if ((rmove-1) < 0 or (rmove-1) >= self.N): # Edge has been hit
                    break        
                if (board[rmove-1,cmove] != '.'):
                    break

                player = self.raichu_upgrade(rmove-1)
                
                board[rmove, cmove] = '.' # Delete Jumped player
                board[rmove-1,cmove] = player
                self.successors.append(np2string(board))
                return
            
            else: # We hit our own team, no more moves left
                break

    def move_D(self, board, row, coll):
        ''' Find the valid down pikachu moves for W and B'''

        cmove = coll # We will not be moving colls
        board[row,coll] = '.' # Delete the pikachu at og location

        for i in range(1,3):
            rmove = row+i

            if rmove < 0 or rmove >= self.N: # Edge has been hit
                break

            player = self.raichu_upgrade(rmove)

            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = player
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika):                
                if ((rmove+1) < 0 or (rmove+1) >= self.N): # Edge has been hit
                    break 
                
                if (board[rmove+1,cmove] != '.'):
                    break

                player = self.raichu_upgrade(rmove+1)
                
                board[rmove, cmove] = '.' # Delete Jumped player
                board[rmove+1,cmove] = player
                self.successors.append(np2string(board))
                return
            
            else: # We hit our own team, no more moves left
                break
    
    def move_L(self, board, row, coll):
        ''' Find the valid left pikachu moves for W and B'''

        rmove = row # We will not be moving colls
        board[row,coll] = '.' # Delete the pikachu at og location

        for i in range(1,3):
            cmove = coll-i

            if cmove < 0 or cmove >= self.N: # Edge has been hit
                break

            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = self.player
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika):                
                if ((cmove-1) < 0 or (cmove-1) >= self.N): # Edge has been hit
                    break 
                
                if (board[rmove,cmove-1] != '.'):
                    break
                
                board[rmove, cmove] = '.' # Delete Jumped player
                board[rmove,cmove-1] = self.player
                self.successors.append(np2string(board))
                return
            
            else: # We hit our own team, no more moves left
                break
        
    def move_R(self, board, row, coll):
        ''' Find the valid right pikachu moves for W and B'''

        rmove = row # We will not be moving colls
        board[row,coll] = '.' # Delete the pikachu at og location

        for i in range(1,3):
            cmove = coll+i

            if cmove < 0 or cmove >= self.N: # Edge has been hit
                break

            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = self.player
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika):                
                if ((cmove+1) < 0 or (cmove+1) >= self.N): # Edge has been hit
                    break 
                
                if (board[rmove,cmove+1] != '.'):
                    break
                
                board[rmove, cmove] = '.' # Delete Jumped player
                board[rmove,cmove+1] = self.player
                self.successors.append(np2string(board))
                return
            
            else: # We hit our own team, no more moves left
                break

class raichus:
    ''' Returns all the possible moves for raichus'''
    def __init__(self, raichuls, player, player_raichu, enemy, enemy_raichu, board) -> None:
        self.board = board
        self.locationls = raichuls
        self.player = player
        self.enemy_pichu = enemy.lower()
        self.enemy_pika = enemy.upper()
        self.enemy_raichu = enemy_raichu
        self.player_raichu = player_raichu
        self.N = len(board)
        self.successors = []
    
    def valid_moves(self):
        ''' Append all valid possible moves for a raichu to self.successors []'''
              
        for riachu in self.locationls:
            row = riachu[0]
            coll = riachu[1]

            self.move_L(np.copy(self.board), row, coll) # move right once space
            self.move_R(np.copy(self.board), row, coll) # move right once space
            self.move_U(np.copy(self.board), row, coll) # move right once space
            self.move_D(np.copy(self.board), row, coll) # move right once space
            self.move_UR(np.copy(self.board), row, coll) # move right once space
            self.move_UL(np.copy(self.board), row, coll) # move right once space
            self.move_DR(np.copy(self.board), row, coll) # move right once space
            self.move_DL(np.copy(self.board), row, coll) # move right once space

        return self.successors

    def move_L(self, board, row, coll):
        ''' Find the valid left raichu moves for W and B'''

        rmove = row # We will not be moving rows
        board[row,coll] = '.' # Delete the raichu at og location

        for i in range(1,coll+1):
            cmove = coll-i
            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = self.player_raichu # Move raichu
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika or board[rmove,cmove] == self.enemy_raichu):
                board[rmove, cmove] = '.' # Delete Jumped player
                for i in range(1,cmove+1): # Distance to jump after
                    cjump = cmove - i
                    if board[rmove,cjump] == '.':
                        newboard2 = np.copy(board)
                        newboard2[rmove,cjump] = self.player_raichu # Move raichu
                        self.successors.append(np2string(newboard2))
                    else:
                        break
                return
            else: # We hit our own team, no more moves left
                break
    
    def move_R(self, board, row, coll):
        ''' Find the valid right raichu moves for W and B'''

        rmove = row # We will not be moving rows
        board[row,coll] = '.' # Delete the raichu at og location

        for i in range(1,(self.N-coll)):
            cmove = coll+i
            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = self.player_raichu # Move raichu
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika or board[rmove,cmove] == self.enemy_raichu):
                board[rmove, cmove] = '.' # Delete Jumped player
                for i in range(1,(self.N-cmove)): # Distance to jump after
                    cjump = cmove + i
                    if board[rmove,cjump] == '.':
                        newboard2 = np.copy(board)
                        newboard2[rmove,cjump] = self.player_raichu # Move raichu
                        self.successors.append(np2string(newboard2))
                    else:
                        break
                return
            else: # We hit our own team, no more moves left
                break
    
    def move_U(self, board, row, coll):
        ''' Find the valid up raichu moves for W and B'''

        cmove = coll # We will not be moving colls
        board[row,coll] = '.' # Delete the raichu at og location

        for i in range(1,row+1):
            rmove = row-i
            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = self.player_raichu # Move raichu
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika or board[rmove,cmove] == self.enemy_raichu):
                board[rmove, cmove] = '.' # Delete Jumped player
                for i in range(1,rmove+1): # Distance to jump after
                    rjump = rmove - i
                    if board[rjump,cmove] == '.':
                        newboard2 = np.copy(board)
                        newboard2[rjump,cmove] = self.player_raichu # Move raichu
                        self.successors.append(np2string(newboard2))
                    else:
                        break
                return
            else: # We hit our own team, no more moves left
                break
    
    def move_D(self, board, row, coll):
        ''' Find the valid down raichu moves for W and B'''

        cmove = coll # We will not be moving colls
        board[row,coll] = '.' # Delete the raichu at og location

        for i in range(1,(self.N - row)):
            rmove = row+i
            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = self.player_raichu # Move raichu
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika or board[rmove,cmove] == self.enemy_raichu):
                board[rmove, cmove] = '.' # Delete Jumped player
                for i in range(1,(self.N - rmove)): # Distance to jump after
                    rjump = rmove + i
                    if board[rjump,cmove] == '.':
                        newboard2 = np.copy(board)
                        newboard2[rjump,cmove] = self.player_raichu # Move raichu
                        self.successors.append(np2string(newboard2))
                    else:
                        break
                return
            else: # We hit our own team, no more moves left
                break
    
    def move_UR(self, board, row, coll):
        ''' Find the valid diagonal upper right raichu moves for W and B'''
 
        board[row,coll] = '.' # Delete the raichu at og location
 
        for i in range(1,row+1):
            rmove = row-i
            cmove = coll+i

            if cmove < 0 or cmove >= self.N or rmove < 0  or rmove >= self.N: # Edge has been hit
                break

            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = self.player_raichu # Move raichu
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika or board[rmove,cmove] == self.enemy_raichu):
                board[rmove, cmove] = '.' # Delete Jumped player
                for i in range(1,rmove+1): # Distance to jump after
                    rjump = rmove - i
                    cjump = cmove + i

                    if cjump < 0 or cjump >= self.N or rjump < 0  or rjump >= self.N: # Edge has been hit
                        break

                    if board[rjump,cjump] == '.':
                        newboard2 = np.copy(board)
                        newboard2[rjump,cjump] = self.player_raichu # Move raichu
                        self.successors.append(np2string(newboard2))
                    else:
                        break
                return
            else: # We hit our own team, no more moves left
                break
    
    def move_UL(self, board, row, coll):
        ''' Find the valid diagonal upper right raichu moves for W and B'''
 
        board[row,coll] = '.' # Delete the raichu at og location
 
        for i in range(1,row+1):
            rmove = row-i
            cmove = coll-i

            if cmove < 0 or cmove >= self.N or rmove < 0  or rmove >= self.N: # Edge has been hit
                break

            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = self.player_raichu # Move raichu
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika or board[rmove,cmove] == self.enemy_raichu):
                board[rmove, cmove] = '.' # Delete Jumped player
                for i in range(1,rmove+1): # Distance to jump after
                    rjump = rmove - i
                    cjump = cmove - i

                    if cjump < 0 or cjump >= self.N or rjump < 0  or rjump >= self.N: # Edge has been hit
                        break

                    if board[rjump,cjump] == '.':
                        newboard2 = np.copy(board)
                        newboard2[rjump,cjump] = self.player_raichu # Move raichu
                        self.successors.append(np2string(newboard2))
                    else:
                        break
                return
            else: # We hit our own team, no more moves left
                break
    
    def move_DR(self, board, row, coll):
        ''' Find the valid diagonal lower right raichu moves for W and B'''
 
        board[row,coll] = '.' # Delete the raichu at og location
 
        for i in range(0,(self.N - row)):
            rmove = row+i
            cmove = coll+i

            if cmove < 0 or cmove >= self.N or rmove < 0  or rmove >= self.N: # Edge has been hit
                break

            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = self.player_raichu # Move raichu
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika or board[rmove,cmove] == self.enemy_raichu):
                board[rmove, cmove] = '.' # Delete Jumped player
                for i in range(1,(self.N - rmove)): # Distance to jump after
                    rjump = rmove + i
                    cjump = cmove + i

                    if cjump < 0 or cjump >= self.N or rjump < 0  or rjump >= self.N: # Edge has been hit
                        break

                    if board[rjump,cjump] == '.':
                        newboard2 = np.copy(board)
                        newboard2[rjump,cjump] = self.player_raichu # Move raichu
                        self.successors.append(np2string(newboard2))
                    else:
                        break
                return
            else: # We hit our own team, no more moves left
                break
    
    def move_DL(self, board, row, coll):
        ''' Find the valid diagonal lower left raichu moves for W and B'''
 
        board[row,coll] = '.' # Delete the raichu at og location
 
        for i in range(1,(self.N - row)):
            rmove = row+i
            cmove = coll-i

            if cmove < 0 or cmove >= self.N or rmove < 0  or rmove >= self.N: # Edge has been hit
                break

            if board[rmove,cmove] == '.':
                newboard = np.copy(board)
                newboard[rmove,cmove] = self.player_raichu # Move raichu
                self.successors.append(np2string(newboard))
            elif (board[rmove,cmove] == self.enemy_pichu or board[rmove,cmove] == self.enemy_pika or board[rmove,cmove] == self.enemy_raichu):
                board[rmove, cmove] = '.' # Delete Jumped player
                for i in range(1,(self.N - rmove)): # Distance to jump after
                    rjump = rmove + i
                    cjump = cmove - i

                    if cjump < 0 or cjump >= self.N or rjump < 0  or rjump >= self.N: # Edge has been hit
                        break

                    if board[rjump,cjump] == '.':
                        newboard2 = np.copy(board)
                        newboard2[rjump,cjump] = self.player_raichu # Move raichu
                        self.successors.append(np2string(newboard2))
                    else:
                        break
                return
            else: # We hit our own team, no more moves left
                break
   
def find_successors_np(board_str, player, player_raichu, enemy_player, enemy_raichu, N):
    ''' Given a board configuration, and the player (b,w) find all possible resulting board states'''
    
    # Create a numpy matrix
    board = string2np(board_str, N)

    # Get index of Pichu, Pikachu, and Raichu in matrix
    row,coll = np.where(board == player) # pichus
    pichuls = list(zip(row, coll))
    row,coll = np.where(board == player.upper()) # pikachus
    pikals = list(zip(row, coll))
    row,coll = np.where(board == player_raichu) # pikachus
    raichuls = list(zip(row, coll))

    
    successors = []
    
    # Pichu moves  
    pch = pichus(pichuls, player, player_raichu, enemy_player, enemy_raichu, board)
    pch_moves = pch.valid_moves()

    #Pikachu moves
    pk = pikachus(pikals, player, player_raichu, enemy_player, enemy_raichu, board)
    pk_moves = pk.valid_moves()

    # Raichu Moves
    rk = raichus(raichuls, player, player_raichu, enemy_player, enemy_raichu, board)
    rk_moves = rk.valid_moves()
    
    successors = successors + pch_moves + pk_moves + rk_moves

    return successors

def evaluation(board, player, enemy_player, player_raichu, enemy_player_raichu):
    ''' Simple Evaluation function for a given state'''
    
    Maxpichu = board.count(player)
    Minpichu = board.count(enemy_player)
    Maxpika = board.count(player.upper())
    Minpika = board.count(enemy_player.upper())
    Maxraichu = board.count(player_raichu)
    Minraichu = board.count(enemy_player_raichu)

    val = (Maxpichu-Minpichu) + 3*(Maxpika-Minpika) + 10*(Maxraichu-Minraichu)
    return val

def minimax(depth, board, Maxplayer, alpha, beta, player, enemy_player, player_raichu, enemy_raichu, N):
    ''' Recursively calculate the minimax algorithm'''

    if depth == 5:
        x = evaluation(board, player,enemy_player, player_raichu, enemy_raichu )
        return x
  
    # If we are the max player
    if Maxplayer:
      
        best = -2000
        successors = find_successors_np(board,player, player_raichu, enemy_player, enemy_raichu, N)
        mv_pair = []

        for move in successors:
            value = minimax(depth + 1, move, False, alpha, beta, player, enemy_player, player_raichu, enemy_raichu, N)
            best = max(best, value)
            alpha = max(alpha, best)
            mv_pair.append((move,value))

            if depth == 0:
                for move in mv_pair:
                    if move[1] == best:
                        print(move[0])
 
            if beta <= alpha:
                break
        
        if depth == 0:
            for move in mv_pair:
                if move[1] == best:
                    return move[0]

        else:
            return best
    
    # If we are the min player
    else:
        best = 2000
        successors = find_successors_np(board,enemy_player, enemy_raichu, player, player_raichu, N)

        for move in successors:
            value = minimax(depth + 1, move, True, alpha, beta, player, enemy_player, player_raichu, enemy_raichu, N)
            best = min(best, value)
            beta = min(beta, best)
 
            if beta <= alpha:
                break
        
        return best

def find_best_move(board, N, player, timelimit):
    ''' Find the best board configuration'''
    
    # Determine enemy player and raichu type
    player = player.lower()
    if player == 'w':
        enemy_player = 'b'
        enemy_raichu = '$'
        player_raichu = '@'
    elif player:
        enemy_player = 'w'
        enemy_raichu = '@'
        player_raichu = '$'


    final = minimax(0, board, True, -2000, +2000, player, enemy_player, player_raichu, enemy_raichu, N)
    print(final)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    find_best_move(board, N, player, timelimit)

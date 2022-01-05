# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys

from itertools import groupby
from copy import deepcopy

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

    # Rewards of a row can be cleared
    def reward_clears(self, board, piece, column, score):
        all_succ = self.successors(board, piece, column, score)
        count = 0
        clear_list = []
        for temp_board in all_succ:
            for row in temp_board:
                if row == "xxxxxxxxxx":
                    count+=1
                clear_list.append(count)
        return clear_list

    # Rewards piece that touches the bottom of board
    def reward_bottom(self, board, piece, column, score):
        # for_print = zip(*board)
        # print("\n".join(board))
        # print(board)
        all_succ = self.successors(board, piece, column, score)
        # print("here:",all_succ[0])
        bottom = board[-1].count('x')
        bottom_list = []
        # print(type(board))
        for temp_board in all_succ:
            # print("\n".join(temp_board[0]))
            # print(temp_board)
            num_bottom = temp_board[0][-1].count('x')
            # print(temp_board[0][-1])
            # print(num_bottom)
            # print(type(temp_board))
            # print("\n")
            # print(temp_board)
           
            # temp = temp_board[0]
            # print(type(temp_board[-1]))
            # print(len(temp[-1]))
            # print("________\n",temp[-1])
            # print(temp)
            bottom_list.append((temp_board[-1].count('x')-bottom, temp_board[1])) #-bottom, temp_board[1]))
        return bottom_list

    #Reward piece touching edges
    def reward_edges(self, board, piece, column, score):
        all_succ = self.successors(board,piece, column, score)
        zip_board = list(zip(*board))
        edge = zip_board[0].count('x')+zip_board[-1].count('x')
        edge_list = []
        for temp_board in all_succ:
            x = board[0]
            # temp = zip(*x)
            edge_list.append((temp_board[0].count('x')+temp_board[-1].count('x')-edge, temp_board[1]))
        return edge_list

    # Helper function to compute height based on board
    def get_height(self, board):
        temp_list = []
        for row in board:
            if 'x' in row:
                temp_list.append(board.index(row))
        return min(temp_list) if temp_list else 0

    # Penalize moves that increase height
    def height_penalty(self, board, piece, column, score):
        all_succ = self.successors(board,piece, column, score)
        curr_height =  self.get_height(board)
        height_list= []
        for temp_board in all_succ:
            height_list.append((self.get_height(temp_board)-curr_height, temp_board[1]))

        return height_list

    # Helper function to compute how many holes exisit in a board
    def get_blocks(self, board):
        num_blocks = 0
        col_list = [[(i, len(list(g))) for i, g in groupby(col)] for col in zip(*board)]
        for col in col_list:
            for i in range (len(col)-1):
                if (col[i][0]=='x' and col[i+1][0]==' '):
                    num_blocks+=col[i][1] # +=1
        return num_blocks

    # Penalize moves that create blocked areas
    def block_penalty(self, board, piece, column, score):
        num_blocks = self.get_blocks(board)
        all_succ = self.successors(board,piece, column, score)
        block_list = []
        for temp_board in all_succ:
            move=temp_board[1]
            block_list.append((self.get_blocks(temp_board[0])-num_blocks, temp_board[1]))
        return block_list

    def move_penalty(self, board, piece, column, score):
        all_succ = self.successors(board, piece, column, score)
        bottom = self.reward_bottom(board,piece,column, score)
        clear = self.reward_clears(board,piece,column, score)
        edge = self.reward_edges(board,piece,column, score)
        height = self.height_penalty(board, piece, column, score)
        blocks = self.block_penalty(board, piece, column, score)
        move_penalty = []

        for i in range (len(all_succ)):
            bottom_weight = 3
            clear_weight = 20
            block_weight = 5
            edge_weight = 2
            height_weight = 7.5

            temp_bottom = bottom[i][0] * bottom_weight
            temp_clear = clear[i] * clear_weight
            temp_block = blocks[i][0] * block_weight
            temp_edge = edge[i][0] * edge_weight
            temp_height = height[i][0] * height_weight
            
            temp_penalty = temp_bottom + temp_clear - temp_block + temp_edge - temp_height
            move_penalty.append((temp_penalty,all_succ[i][1]))
       
        sorted_moves = sorted(move_penalty,key=lambda tup:tup[0])
        temp_index = 0
        temp_weight = float(sorted_moves[-1][0])
        for i in range (len(sorted_moves)):
            if(float(sorted_moves[i][0])<temp_weight):
                temp_index = i 
        # print(sorted_moves)
        return sorted_moves[0]

    def current_positions(self, board):
        b_zip = zip(*board)

        ind_list = []
        col_num = 0

        for col in b_zip:
            temp_col = list(col)

            if 'x' in temp_col:
                ind_list.append((col_num, temp_col.index('x')))
            else:
                ind_list.append((col_num,20))
            col_num +=1

        return ind_list

    '''
        Function to find all successors of a new piece
        Returns: List of all successors
    '''
    def successors(self, board, piece, column, score):
        try:
            temp_game = QuintrisGame()
            all_pos = self.current_positions(board)

            # Add all possible rotations of current piece to list
            possible_rotations = []
            possible_rotations.append(piece)
            possible_rotations.append(temp_game.rotate_piece(piece[0], 90))
            possible_rotations.append(temp_game.rotate_piece(piece[0], 180))
            possible_rotations.append(temp_game.rotate_piece(piece[0], 270))

            # Find succesors of all possible rotations of piece
            all_successors = []
            for piece in possible_rotations:

                curr_move = ""
                curr_index = possible_rotations.index(piece)

                if curr_index == 1:
                    curr_move += "n"
                elif curr_index == 2:
                    curr_move += "nn"
                elif curr_index == 3:
                    curr_move += "nnn"

                # Do all possible moves to right
                # Do all possible moves to left
                piece_height = len(piece[0])
                piece_width = len(max(piece[0], key=len))
                for pos in all_pos:
                    collision = temp_game.check_collision(board, score, piece[0], pos[1]-piece_height, pos[0])
                    if not collision:
                        if pos[0]+piece_width and pos[1]-piece_height-1>=0:
                            new_board = temp_game.place_piece(board, score,piece[0],pos[1]-piece_height-1, pos[0])

                            if pos[0]<column:
                                all_successors.append((new_board[0],curr_move+"b"*(column-pos[0])))
                            elif pos[0]>column:
                                all_successors.append((new_board[0],curr_move+"m"*(pos[0]-column)))
                            elif pos[0]==column:
                                all_successors.append((new_board[0], curr_move))

            if all_successors:
                return all_successors
            else:
                sys.exit(0)
        except IndexError:
            raise EndOfGame("Game Over!")
            sys.exit(0)


    # def successors(self, board, piece, column, score):
    #     # print(piece)

    #     # Piece (self.piece, self.row, self.col)
    #     piece_row = piece[1]
    #     piece_col = piece[1]

    #     temp_game = QuintrisGame()
    #     temp_board = deepcopy(board)

    #     # COMMANDS = { "b": self.left, "n": self.rotate, "m": self.right, "h": self.hflip }
    #     temp_game.place_piece(temp_board, score,piece[0], piece_row, piece_col)

    #     rotations = [0,1,2,3]
    #     flips = [0,1]

    #     possible_moves = []
    #     move_str = ""

    #     # Given a piece -> first we account for all rotations and flips
    #     for rotation in rotations:
    #         for flip in flips:
    #             move_str = ""
    #             move_str_right = ""
    #             move_str_left = ""

    #             for i in range (int(rotation)):
    #                 temp_game.rotate()
    #                 move_str +="n"

    #             for i in range (int(flip)):
    #                 temp_game.hflip()
    #                 move_str +="h"

    #             for i in range(0,15):
    #                 temp_col = temp_game.get_piece()
    #                 temp_col = temp_col[2]
    #                 print(temp_col)
    #                 collision_left = temp_game.check_collision(temp_board, score, piece[0], piece_row, temp_col-1)
    #                 collision_right = temp_game.check_collision(temp_board, score, piece[0], piece_row, temp_col+1)
    #                 # print("Coll Left: ", collision_left, "Coll right: ", collision_right)
    #                 if i<piece_col and not collision_left:
    #                     print("HERE")
    #                     quintris.right()
    #                     move_str_right+= "b"

    #                     possible_moves.append ((curr_board, move_str+move_str_right))

    #                 elif i<piece_col and collision_left:
    #                     # print("HERE")
    #                     temp_game.down()
    #                     # move_str+= " "
    #                     curr_board = temp_game.get_board()
    #                     move_str+=move_str_left
    #                     # print("move srt left: ",move_str_left)
    #                     possible_moves.append ((curr_board, move_str))

    #                 elif i>piece_col and not collision_right:
    #                     # print("HERE")
    #                     quintris.left()
    #                     # move_str_left+= "m"
    #                     possible_moves.append ((curr_board, move_str+move_str_left))

    #                 elif i>piece_col and collision_right:
    #                     # print("HERE")
    #                     temp_game.down()
    #                     # move_str+= " "
    #                     move_str += move_str_right
    #                     curr_board = temp_game.get_board()
    #                     possible_moves.append ((curr_board, move_str))
    #                 elif i == piece_col:
    #                     temp_game.down()
    #                     curr_board = temp_game.get_board()
    #                     possible_moves.append ((curr_board, move_str))

    #     return possible_moves

            # curr_move = ""
            # curr_index = possible_rotations.index(piece)
            # if curr_index == 1:
            #     curr_move += "n"
            # elif curr_index == 2:
            #     curr_move += "nn"
            # elif curr_index == 3:
            #     curr_move += "nnn"

            # Every iteration piece can move left, right, or stay
            # def place_piece(board, score, piece, row, col):
            # while(1):
            #     temp_game.place_piece(board, score,piece[0],pos[1]-piece_height-1, pos[0])


    def get_moves(self, quintris):
        board = quintris.get_board()
        piece = quintris.get_piece()
        next_piece = quintris.get_next_piece()
        # score = quintris.get_score()
        score = board[1]
        # successors(self, board, piece, column, score):
        move = self.move_penalty(board, piece, piece[2], score)
        return move[1]

#        possible_moves = self.successors(board, piece, piece[2], score)


    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < quintris.col):
                quintris.left()
            elif(index > quintris.col):
                quintris.right()
            else:
                quintris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)




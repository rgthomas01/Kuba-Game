# Rachel Thomas
# 6/1/21
# Description : Sets up a Kuba Game class that in conjunction with the Player class that can be utilized to simulate
# playing the Kuba Game

import copy



class KubaGame:
    """Create an object to represent the game board and initialize all variables, hold methods for checking if moves are legal,
    making moves, and updating status for win, draw, or unfinished.
    Contains Player Objects and will communicate with that class
    """

    def __init__(self, player_1, player_2):
        """ Initialize game board, marble counts, turn and winner values,  and takes player information as a tuple containing player name and color being
        played """
        self._p1_captured = 0
        self._p2_captured = 0

        self._p1 = Player(player_1[0], player_1[1], self._p1_captured)
        self._p2 = Player(player_2[0], player_2[1], self._p2_captured)

        self._turn = None
        self._winner = None

        self._row = 0
        self._column = 0
        self._white_count = 8
        self._black_count = 8
        self._red_count = 13
        self._ko_check = None

        self._x_counter = 0
        self._lower_bound = 0
        self._upper_bound = 6
        self._upper_bound = 6
        self._lower_bound = 0
        self._eliminated_piece = 0

        self._board = [['W', 'W', 'X', 'X', 'X', 'B', 'B'],
                       ['W', 'W', 'X', 'R', 'X', 'B', 'B'],
                       ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
                       ['X', 'R', 'R', 'R', 'R', 'R', 'X'],
                       ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
                       ['B', 'B', 'X', 'R', 'X', 'W', 'W'],
                       ['B', 'B', 'X', 'X', 'X', 'W', 'W']]

        self._prev_board = copy.deepcopy(self._board)
        self._test_board = copy.deepcopy(self._board)

    def print_board(self):
        """Print visual representation of the Board"""

        for self._row in self._board:
            print(self._row)
        print()

    def get_game_status(self):
        """Prints out turn, captured marbles, remaining marble count, and winner """
        print("Current Status:")
        print("Turn:", self._turn)
        print("P1 score:", self.get_captured('Player 1'))
        print("P2 score:", self.get_captured('Player 2'))
        print("Remaining Marbles in W,B,R", self.get_marble_count())
        print("Winner", self.get_winner())
        print()

    def get_player_obj(self, playername):
        """ Get player object given their name"""
        if self._p1.get_player_name() == playername:
            return self._p1
        if self._p2.get_player_name() == playername:
            return self._p2

    def get_current_turn(self):
        """Returns name of player whose turn it is, initialized to none before game starts"""
        return self._turn

    def set_current_turn(self, playername):
        """ Set whose turn it is,takes player_name parameter and returns player_name, is called after a move is successfully
        made. Is set to opposite player who made the move as no consecutive turns are allowed """
        if self._p1.get_player_name() == playername:
            self._turn = self._p2.get_player_name()

        if self._p2.get_player_name() == playername:
            self._turn = self._p1.get_player_name()

    def get_winner(self):
        """ returns Name of winner if there is one, else returns none"""
        return self._winner

    def set_winner(self, playername):
        """Sets winner"""
        self._winner = playername

    def check_winner(self, playername):
        """ Checks win conditions, takes player object and compares number captured to 7. Also checks if any player
        runs out of pieces. Calls set_winner if winner is found """
        if self.get_captured(playername) == 7:
            self.set_winner(playername)

        if self._black_count == 0 or self._white_count == 0:
            self.set_winner(playername)

    def make_move(self, playername, coordinates, direction):
        """Makes move listed by player provided movie is valid"""

        vert_coord = coordinates[0]
        horiz_coord = coordinates[1]
        player_obj = self.get_player_obj(playername)
        player_color = player_obj.get_player_color()

        if self._winner is not None:  # checks if game is still in play
            #print(self.get_winner(), "Already Won")
            return False

        if self.get_current_turn() is not None:
            if playername != self.get_current_turn():  # compare player to whose turn it is
                # print("Not your turn")
                return False

        if player_color != self.get_marble(
                coordinates):  # compares marble at coordinates given to player's marble color
            # print("Nice try, you can only move your own Pieces")
            return False

        if vert_coord > 6 or vert_coord < 0:  # if player tries to make a play out of bounds
            # print("Thats not a place on the board ")
            return False

        if horiz_coord > 6 or horiz_coord < 0:  # if player tries to make a play out of bounds
            # print("Thats not a place on the board ")
            return False


        # CHECK ACCESSIBLE TO MOVE--------------------------------------------------------------------------------------
        if direction == 'L':
            if horiz_coord != 0 and horiz_coord != 6:  # if its not an edge check value to right
                if self._board[vert_coord][horiz_coord + 1] != 'X':  # if square to the right is non empty
                    return False

        if direction == 'R':
            if horiz_coord != 0 and horiz_coord != 6:  # if its not an edge check value to left
                if self._board[vert_coord][horiz_coord - 1] != 'X':
                    return False

        if direction == 'F':
            if vert_coord != 0 and vert_coord != 6:  # if its not an edge check value backward from it
                if self._board[vert_coord + 1][horiz_coord] != 'X':
                    return False

        if direction == 'B':
            if vert_coord != 0 and vert_coord != 6:  # if its not an edge check value forward from it
                if self._board[vert_coord - 1][horiz_coord] != 'X':
                    return False

        self.ko_test(playername, coordinates, direction)
        if self._ko_check == True:
            self.set_current_turn(playername)
            self.check_winner(playername)
            return True
        else:
            return False

    def get_captured(self, playername):
        """Returns how many red marbles a player has captured takes player name as param"""
        if self._p1.get_player_name() == playername:
            return self._p1.get_player_captured()
        elif self._p2.get_player_name() == playername:
            return self._p2.get_player_captured()
        else:
            return False

    def set_captured(self, playername):
        """Take player_name and adds to their captured total"""
        if self._p1.get_player_name() == playername:
            return self._p1.add_capture()
        elif self._p2.get_player_name() == playername:
            return self._p2.add_capture()

    def get_marble(self, coordinates):
        """Returns color of marble at location  given by the tuple passed to it or X if empty"""
        return self._board[coordinates[0]][coordinates[1]]

    def get_marble_count(self):
        """Returns count of marbles remaining on Board in White, Black, Red Order, values are updated throughout game
        play """
        marble_count = (self._white_count, self._black_count, self._red_count)
        return marble_count

    def player_status(self):
        """ Prints  attributes of player Objects"""
        print("Current Scores:")
        print(self._p1.get_player_name(), self._p1.get_player_color(), self._p1.get_player_captured())
        print(self._p2.get_player_name(), self._p2.get_player_color(), self._p2.get_player_captured())

    def ko_test(self, playername, coordinates, direction):
        """ Tests that a potential move doesnt violate the Ko rule , is called during make move.
         Makes a move on a deep copy of the board from previous turn and then compares """

        vert_coord = coordinates[0]
        horiz_coord = coordinates[1]
        player_obj = self.get_player_obj(playername)
        player_color = player_obj.get_player_color()

        self._lower_bound = 0  # resets these to edge cases every call
        self._upper_bound = 6

        self._eliminated_piece = 0
        self._ko_check = None

        # LEFT MOVE ----------------------------------------------------------------------------------------------------
        if direction == "L":

            if horiz_coord != 0:            # if it is not the edge find next empty
                for i in range(horiz_coord, -1, -1):  # for items from horiz coord to left edge
                    for item in self._test_board[vert_coord][i]:  # for items in this row
                        if item == "X" and self._lower_bound == 0:      #finds next empty
                            self._lower_bound = i

            if self._lower_bound == 0:  # if a piece will get pushed off the edge or empty is edge
                self._eliminated_piece = self._test_board[vert_coord][0]
                if self._eliminated_piece != 'X':
                    if self._eliminated_piece == 'W' and player_color == 'W':  # if player would bump off their own piece
                         # print("You cant knock your own piece off silly")
                        return False
                    if self._eliminated_piece == 'B' and player_color == 'B':
                        # print("You cant knock your own piece off silly")
                        return False
                    self._test_board[vert_coord][self._lower_bound] = 'X'  # replace edge case with empty

            for i in range(self._lower_bound, horiz_coord):  # from the empty on the left side
                self._test_board[vert_coord][i] = self._test_board[vert_coord][
                        i + 1]  # makes item on board equal to the previous stopping when it reaches the the
            self._test_board[vert_coord][horiz_coord] = 'X'  # empty space where marble was

        # RIGHT MOVE ---------------------------------------------------------------------------------------------------
        if direction == "R":

            if horiz_coord != 6:            # if it is not the edge find next empty
                for i in range(horiz_coord, 7):
                    for item in self._test_board[vert_coord][i]:
                        if item == "X" and self._upper_bound == 6:
                            self._upper_bound = i

            if self._upper_bound == 6:
                self._eliminated_piece = self._test_board[vert_coord][6]
                if self._eliminated_piece != 'X':
                    if self._eliminated_piece == 'W' and player_color == 'W':  # if player would bump off their own piece
                        # print("You cant knock your own piece off silly")
                        return False
                    if self._eliminated_piece == 'B' and player_color == 'B':
                        # print("You cant knock your own piece off silly")
                        return False
                    self._test_board[vert_coord][self._upper_bound] = 'X'  # replace edge case with empty

            for i in range(self._upper_bound, horiz_coord, -1):  # from the empty on the right side
                self._test_board[vert_coord][i] = self._test_board[vert_coord][
                    i - 1]  # makes item on board equal to the next stopping when it reaches the the
            self._test_board[vert_coord][horiz_coord] = 'X'  # empty space where marble was

        # BACKWARD 'DOWN' MOVE -----------------------------------------------------------------------------------------
        if direction == "B":  # if moving to the right need to coord and move right until edge or empty

            if vert_coord != 6:  # if it is not the edge find next empty
                for i in range(vert_coord, 7):  # for items from horiz coord to right edge
                    for item in self._test_board[i][horiz_coord]:  # for items in this row
                        if item == "X" and self._upper_bound == 6:
                            self._upper_bound = i

            if self._upper_bound == 6:  # if a piece will get pushed off the edge, or an empty at edge is replaced
                self._eliminated_piece = self._test_board[6][horiz_coord]
                if self._eliminated_piece != 'X':  # if true edge case not empty at edge
                    if self._eliminated_piece == 'W' and player_color == 'W':  # if player would bump off their own piece
                        # print("You cant knock your own piece off silly")
                        return False
                    if self._eliminated_piece == 'B' and player_color == 'B':
                        # print("You cant knock your own piece off silly")
                        return False
                    self._test_board[self._upper_bound][horiz_coord] = 'X'  # replace edge case with empty

            for i in range(self._upper_bound, vert_coord, -1):  # from the empty below
                self._test_board[i][horiz_coord] = self._test_board[i - 1][
                    horiz_coord]  # makes item on board equal to the previous stopping when it reaches the the
            self._test_board[vert_coord][horiz_coord] = 'X'  # empty space where marble was

        # FORWARD 'UP' MOVE --------------------------------------------------------------------------------------------
        if direction == "F":  # if moving to the right need to coord and move right until edge or empty

            if vert_coord != 0:  # if it is not the edge find next empty
                for i in range(vert_coord, -1, -1):  # for items from horiz coord to right edge
                    for item in self._test_board[i][horiz_coord]:  # for items in this row
                        if item == "X" and self._lower_bound == 0:
                            self._lower_bound = i

            if self._lower_bound == 0:  # if a piece will get pushed off the edge, or an empty at edge is replaced
                self._eliminated_piece = self._test_board[self._lower_bound][horiz_coord]
                if self._eliminated_piece != 'X':  # if true edge case not empty at edge#
                    if self._eliminated_piece == 'W' and player_color == 'W':  # if player would bump off their own piece
                        # print("You cant knock your own piece off silly")
                        return False
                    if self._eliminated_piece == 'B' and player_color == 'B':
                        # print("You cant knock your own piece off silly")
                        return False
                    self._test_board[self._lower_bound][horiz_coord] = 'X'  # replace edge case with empty

            for i in range(self._lower_bound, vert_coord):  # from the empty below
                self._test_board[i][horiz_coord] = self._test_board[i + 1][
                    horiz_coord]  # makes item on board equal to the previous stopping when it reaches the the
            self._test_board[vert_coord][horiz_coord] = 'X'  # empty space where marble was

        if self._turn is not None:
            if self._test_board == self._prev_board:        #if move fails ko test
                #print("That just undoes the prev move, big NOPE")
                self._test_board = copy.deepcopy(self._board)
                self._ko_check = False

            else:
                self._test_board != self._prev_board          #if move passes ko test , we can make the move
                self._ko_check = True
                self._prev_board = copy.deepcopy(self._board)   #saves board before move in prev
                self._board = copy.deepcopy(self._test_board)


        else:  #if it is the first turn
            self._ko_check = True
            self._board = copy.deepcopy(self._test_board)

        if self._eliminated_piece != 'X':  # todo in other directions
            if self._eliminated_piece == 'R':  # if its a red piece
                self.set_captured(playername)  # add to players total
                self._red_count -= 1  # remove from count of red on board

            if self._eliminated_piece == 'W':
                self._white_count -= 1

            if self._eliminated_piece == 'B':
                self._black_count -= 1


class Player:
    """Class that represents player in Kuba Game"""

    def __init__(self, playername, color, captured):
        self._playername = playername
        self._color = color
        self._captured = captured

    def get_player_name(self):
        """ Get player's name"""
        return self._playername

    def get_player_color(self):
        """Get player's token color"""
        return self._color

    def get_player_captured(self):
        """ Check within object how many pieces are captured"""
        return self._captured

    def add_capture(self):
        """ Adds 1 to captured """
        self._captured += 1
        return self._captured

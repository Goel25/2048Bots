import random
import copy
DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3


# ----------TODO STUFF TO CHANGE----------
# near_sight
# look_ahead (best at 4)
# score_normalizer (not below 50)
# eval_max vs eval_avg
# Use score bonus, for look ahead and for normal (Much better w/ score bonus)
# Look at only boards at the end vs. boards that are finished

# MAJOR TODO CHECK_ALL ONLY CALC'S FITNESS FOR LAST MOVE, NOT ALL MOVES

# MAJOR  TODO BUG IT DOES NOT WANT TO BUILD A TILE THAT IS EQUAL TO THE ONE
# HIGHER THAN IT BECAUSE IT WILL LOSE THE BONUS

# TODO Encourage if it increases largest tile

# TODO See if changing near_sight actually matters. It may only
# matter if it is above a certain value, or below that value,
# because all of the probs are changed by that amount.

# TODO Should the correct order function have the if statements nested?

# TODO Perhaps Keep track of the path taken to get to the final
# state, then once its found try that path again with diff RNG
# and make sure that is actually good


# TODO Maybe also add into the calculation of what percent change there is
# to get a bad RNG for the next piece the higher the chance, the more
# fitness subtracted

# ----------TODO STUFF I'VE CHANGED----------
# TODO Add early game algorithm to just spam Right and Down! (I sorta did this)

# TODO Modify correct order function to change when you get a certain tile
# that is high enough. Expand it to be able to play until 4096

class Decider:
    def __init__(self, look_ahead=4):
        self.look_ahead = look_ahead
        self.score_normalizer = 1250
        self.check_all_boards = True
        self.near_sight = 5.75
        self.scoring = {
            2: [0.8, 0.6],
            3: [.7, .5, .4, .2],
            4: [.7, .5, .4, .2, .1]
        }

    def decide(self, board):
        probs = [-9999] * 4

        down_board = self.move(DOWN, board)
        right_board = self.move(RIGHT, board)
        left_board = self.move(LEFT, board)
        up_board = self.move(UP, board)

        if down_board is not False:
            down_boards = []
            self.check_all(down_board, down_boards)
            down_max = self.eval_max(down_boards)
            probs[DOWN] = down_max
            probs[DOWN] += (self.eval_fit(down_board) * self.near_sight)

        if right_board is not False:
            right_boards = []
            self.check_all(right_board, right_boards)
            right_max = self.eval_max(right_boards)
            probs[RIGHT] = right_max
            probs[RIGHT] += (self.eval_fit(right_board) * self.near_sight)

        if left_board is not False:
            left_boards = []
            self.check_all(left_board, left_boards)
            left_max = self.eval_max(left_boards)
            probs[LEFT] = left_max
            probs[LEFT] += (self.eval_fit(left_board) * self.near_sight)

        if up_board is not False:
            up_boards = []
            self.check_all(up_board, up_boards)
            up_max = self.eval_max(up_boards)
            probs[UP] = up_max
            probs[UP] += (self.eval_fit(up_board) * self.near_sight)

        m = max(probs)
        if m == -9999:
            # print("No moves!")
            return 0
        else:
            return probs.index(max(probs))

    def check_all(self, board, add_to, current_index=0):
        if current_index < self.look_ahead:
            down_board = self.move(DOWN, board[1])
            right_board = self.move(RIGHT, board[1])
            left_board = self.move(LEFT, board[1])
            up_board = self.move(UP, board[1])
            added_old_board = False

            if down_board is not False:
                self.check_all(down_board, add_to, current_index + 1)
            elif self.check_all_boards and not added_old_board:
                add_to.append(board)
                added_old_board = True

            if right_board is not False:
                self.check_all(right_board, add_to, current_index + 1)
            elif self.check_all_boards and not added_old_board:
                add_to.append(board)
                added_old_board = True

            if left_board is not False:
                self.check_all(left_board, add_to, current_index + 1)
            elif self.check_all_boards and not added_old_board:
                add_to.append(board)
                added_old_board = True

            if up_board is not False:
                self.check_all(up_board, add_to, current_index + 1)
            elif self.check_all_boards and not added_old_board:
                add_to.append(board)
                added_old_board = True
        else:
            add_to.append(board)

    def eval_max(self, boards):
        # return 0
        best_fit = -1
        for board in boards:
            fit = self.eval_fit(board, True)
            if fit > best_fit:
                best_fit = fit
        return best_fit

    def eval_avg(self, boards):
        if len(boards) > 0:
            avg_fit = 0
            for board in boards:
                fit = self.eval_fit(board)
                avg_fit += fit
            avg_fit /= len(boards)
            return avg_fit
        else:
            return 0

    def eval_fit(self, board, use_score=True):
        fit = 0
        if use_score:
            fit += board[2]/self.score_normalizer  # Score bonus
        fit += self.in_correct_order(board[1])
        return fit

    def in_correct_order(self, board):

        # board_copy = copy.deepcopy(board)
        # points = 0
        # high_spots = self.find_highest_spots(board_copy)
        # highest_tile = high_spots[0]
        # highest_spots = high_spots[1]

        # iterations = 2 if highest_tile <= 8 else 3
        # iterations = iterations if highest_tile <= 10 else 4
        # # print(iterations)
        # if (3, 3) in highest_spots[-1]:
        #     points += self.scoring[iterations][0]
        #     highest_spots[-1].remove((3, 3))  # TODO SEE IF THIS LINE MATTERS

        # for i in range(1, iterations):
        #     if self.is_in(highest_spots, (3, 3-i), i - 1):
        #         points += self.scoring[iterations][i-1]
        #         try:
        #             highest_spots[i-1].remove((3, 3-i))
        #         except:
        #             try:
        #                 highest_spots[i-2].remove((3, 3-i))
        #             except:
        #                 pass
        #                 # print("None found")

        # if iterations == 4:
        #     if self.is_in(highest_spots, (2, 0), i - 1):
        #         points += self.scoring[4][4]

        # if highest_tile <= 8:  # Do this if highest tile is 256 or below
        #     if (3, 3) in highest_spots[-1]:
        #         points += .8  # This is right, checking for highest, then what?
        #         highest_spots[-1].remove((3, 3))
        #     if self.is_in(highest_spots, (3, 2), 0):
        #         points += .6  # TODO This will break if it is out of index
        # elif highest_tile <= 10:  # Do this if highest tile is 1024 or below
        #     pass
        # else:
        #     pass

        board_copy = copy.deepcopy(board)
        points = 0
        high_spots = self.find_highest_spots(board_copy)
        highest_tile = high_spots[0]
        highest_spots = high_spots[1]
        # print(highest_spots)
        if highest_tile <= 8:  # Do this if highest tile is 256 or below
            if (3, 3) in highest_spots:
                points += self.scoring[2][0]
                # board_copy[3][3] = 0
                for pos in highest_spots:
                    board_copy[pos[0]][pos[1]] = 0
                highest_spots = self.find_highest_spots(board_copy)[1]
            if (3, 2) in highest_spots:
                points += self.scoring[2][1]
        elif highest_tile <= 10:
            # Do this if highest tile is 1024 or below
            if (3, 3) in highest_spots:
                points += self.scoring[3][0]
                # board_copy[3][3] = 0
                for pos in highest_spots:
                    board_copy[pos[0]][pos[1]] = 0
                highest_spots = self.find_highest_spots(board_copy)[1]
            if (3, 2) in highest_spots:
                points += self.scoring[3][1]
                # board_copy[3][2] = 0
                for pos in highest_spots:
                    board_copy[pos[0]][pos[1]] = 0
                highest_spots = self.find_highest_spots(board_copy)[1]
            if (3, 1) in highest_spots:
                points += self.scoring[3][2]
        else:  # Do this if highest tile is 2048 or more
            if (3, 3) in highest_spots:
                points += self.scoring[4][0]
                # board_copy[3][3] = 0
                for pos in highest_spots:
                    board_copy[pos[0]][pos[1]] = 0
                highest_spots = self.find_highest_spots(board_copy)[1]
            if (3, 2) in highest_spots:
                points += self.scoring[4][1]
                # board_copy[3][2] = 0
                for pos in highest_spots:
                    board_copy[pos[0]][pos[1]] = 0
                highest_spots = self.find_highest_spots(board_copy)[1]
            if (3, 1) in highest_spots:
                points += self.scoring[4][2]
                # board_copy[3][1] = 0
                for pos in highest_spots:
                    board_copy[pos[0]][pos[1]] = 0
                highest_spots = self.find_highest_spots(board_copy)[1]
            if (3, 0) in highest_spots:
                points += self.scoring[4][3]
                # TODO IS THIS ACTUALLY WORKING? TRY IT WITH OTHER POSSIBILITIES!
                # LATER NOTE: NO IT'S NOT WORKING, MUST MAKE ARRAY OF ARRAY WITH TUPLES OF POS'
                # board_copy[3][0] = 0
                for pos in highest_spots:
                    board_copy[pos[0]][pos[1]] = 0
                highest_spots = self.find_highest_spots(board_copy)[1]
                if (2, 0) in highest_spots:
                    points += self.scoring[4][4]
                # for pos in highest_spots:
                #     board_copy[pos[0]][pos[1]] = 0
                # highest_spots = self.find_highest_spots(board_copy)[1]
        return points

    def is_in(self, ls, pos, amt):
        minimum = -len(ls)
        return (pos in ls[max(amt - 1, minimum)] or
                pos in ls[max(amt - 2, minimum)])

    def find_highest_spots(self, board):
        # TODO Rewrite this algorithm to return a sorted list
        # of lists of the points EX [[(2,3), (0,2)],[(3,3), (3,2)]]
        # sorted_tile_amts = []

        # for x in range(len(board)):
        #     for y in range(len(board[0])):
        #         if board[x][y] > 0 and board[x][y] not in sorted_tile_amts:
        #             sorted_tile_amts.append(board[x][y])
        # sorted_tile_amts.sort()  # TODO Maybe I don't need this
        # positions = [[] for i in range(len(sorted_tile_amts))]

        # for x in range(len(board)):
        #     for y in range(len(board[0])):
        #         if board[x][y] > 0:
        #             index = sorted_tile_amts.index(board[x][y])
        #             positions[index].append((x, y))
        # return (sorted_tile_amts[-1], positions)

        highest = -1
        highest_spots = []
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] >= highest:
                    highest = board[x][y]
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == highest:
                    highest_spots.append((x, y))
        return (highest, highest_spots)

    def move(self, direction, board):
        fixed_dir = (direction + 3) % 4
        new_board = copy.deepcopy(board)
        if direction == RIGHT:
            moved = self.move_right(new_board)
            new_board = moved[0]
            fitness_gained = moved[1]
        else:
            new_board = self.rotate_2d(fixed_dir, new_board)
            moved = self.move_right(new_board)
            new_board = moved[0]
            fitness_gained = moved[1]
            new_board = self.rotate_2d((fixed_dir + 2) % 4, new_board)

        if board != new_board:
            # If there is a change, update it and add a tile
            # self.board = new_board
            self.add_tile(new_board)
            return [True, new_board, fitness_gained]
        else:
            return False

    def add_tile(self, board):
        available_positions = []
        for x in range(4):
            for y in range(4):
                if board[x][y] == 0:
                    available_positions.append((x, y))
        if len(available_positions) > 0:
            index = random.randint(0, len(available_positions)-1)
            chosen_position = available_positions[index]
            amt = 1 if random.random() < .9 else 2
            board[chosen_position[0]][chosen_position[1]] = amt

    def rotate_2d(self, direction, board):
        new_board = make_2d(4, 4, 0)
        if direction == RIGHT:  # Right
            for x in range(len(board)):
                for y in range(len(board[0])):
                    new_board[y][3 - x] = board[x][y]
        elif direction == UP or direction == DOWN:  # Up/Down
            new_board[0] = flip_arr(board[3])
            new_board[1] = flip_arr(board[2])
            new_board[2] = flip_arr(board[1])
            new_board[3] = flip_arr(board[0])
        elif direction == LEFT:  # Left
            for x in range(len(board)):
                for y in range(len(board[0])):
                    new_board[3-y][x] = board[x][y]
        return new_board

    def move_right(self, board):
        fitness_gained = 0
        new_board = make_2d(4, 4, 0)
        for x in range(len(board)):
            prev = -1
            lvl = 3
            tiles_found = 0
            i = len(board[0]) - 1
            while i >= 0:
                # print(f'I: {i}')
                current = board[x][i]
                if current > 0:
                    tiles_found += 1
                    if prev == -1:  # Find the lowest (position-wise) tile
                        # print("Set previous")
                        prev = current
                        i -= 1
                        if i == -1 and tiles_found == 1:
                            # If the only tile is on top row
                            new_board[x][lvl] = current
                            lvl -= 1
                    else:
                        if current == prev:  # Do we have a match?
                            new_board[x][lvl] = current + 1
                            fitness_gained += 2 ** (current + 1)
                            board[x][i] = 0
                            lvl -= 1
                            prev = -1
                            i -= 1
                            tiles_found -= 2
                            # print("Match")
                        else:
                            new_board[x][lvl] = prev  # No match!
                            prev = current
                            lvl -= 1
                            prev = -1
                            tiles_found -= 2
                            # print("Not a Match")
                else:
                    if i == 0 and tiles_found == 1:  # We only found one tile!
                        new_board[x][lvl] = prev
                        lvl -= 1
                    i -= 1
            # print("-----------------------------------------")
        return (new_board, fitness_gained)


def make_2d(w, h, val):
    arr = []
    for i in range(w):
        tempArr = []
        for j in range(h):
            tempArr.append(val)
        arr.append(tempArr)
    return arr


def flip_arr(arr):
    new_arr = []
    for i in range(len(arr)-1, -1, -1):
        new_arr.append(arr[i])
    return new_arr

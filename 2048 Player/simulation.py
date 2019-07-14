import random
import numpy as np
import brain
DOWN = 0  # Left
RIGHT = 1
UP = 2
LEFT = 3  # UP


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


class Game:
    def __init__(self):
        self.board = make_2d(4, 4, 0)
        self.alive = True
        self.add_tile()
        self.add_tile()
        self.fitness = 0
        # self.prob = 0
        # self.add_tile()
        # self.add_tile()  # Two starting tiles

    def add_tile(self):
        available_positions = []
        for x in range(4):
            for y in range(4):
                if self.board[x][y] == 0:
                    available_positions.append((x, y))
        if len(available_positions) > 0:
            index = random.randint(0, len(available_positions)-1)
            chosen_position = available_positions[index]
            amt = 1 if random.random() < .9 else 2
            self.board[chosen_position[0]][chosen_position[1]] = amt
        else:
            self.alive = False

    # def crossover(self, other_game):
    #     # Brain.crossover returns weights list, so does mutate
    #     return self.brain.mutate(self.brain.crossover(other_game.brain))

    def reset(self):
        print(f"Fitness: {self.fitness}")
        self.board = make_2d(4, 4, 0)
        self.alive = True
        self.fitness = 0
        self.add_tile()
        self.add_tile()  # Two starting tiles

    def set_board(b):
        self.board = b

    def move_by_list(self, directions):
        # results = self.brain.predict(self.board)
        sorted_results = np.sort(directions)
        # results =
        # Try probabilites in descending order
        if not self.move(directions.index(sorted_results[3])):
            if not self.move(directions.index(sorted_results[2])):
                if not self.move(directions.index(sorted_results[1])):
                    if not self.move(directions.index(sorted_results[0])):
                        self.alive = False

    def move(self, direction):
        fixed_dir = (direction + 3) % 4
        new_board = self.board.copy()
        if direction == RIGHT:
            new_board = self.move_right(new_board)
        else:
            new_board = self.rotate_2d(fixed_dir, new_board)
            new_board = self.move_right(new_board)
            new_board = self.rotate_2d((fixed_dir + 2) % 4, new_board)

        if self.board != new_board:
            # If there is a change, update it and add a tile
            self.board = new_board
            self.add_tile()
            return True
        else:
            return False

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
                            self.fitness += 2 ** (current + 1)
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
        return new_board

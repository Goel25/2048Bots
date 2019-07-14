import brain
import random
import numpy as np
DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3


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


class Board:
    def __init__(self):
        self.board = make_2d(4, 4, 0)
        self.alive = True
        self.fitness = 0
        self.moves_survived = 0
        self.add_tile()
        self.add_tile()

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

    # def reset(self):
    #     self.board = make_2d(4, 4, 0)
    #     self.alive = True
    #     self.fitness = 0
    #     self.add_tile()
    #     self.add_tile()

    def move_AI(self, results):
        if self.alive:
            # results = self.brain.predict(board, 12)
            # print(results)
            # results[DOWN] += .5
            # results[RIGHT] += .5
            sorted_results = np.sort(results)
            results = results.tolist()
            # Try probabilites in descending order
            if not self.move(self.board,
                             results.index(sorted_results[3])):
                if not self.move(self.board,
                                 results.index(sorted_results[2])):
                    if not self.move(self.board,
                                     results.index(sorted_results[1])):
                        if not self.move(self.board,
                                         results.index(sorted_results[0])):
                            self.alive = False
            if self.alive:
                self.moves_survived += 1

    def move(self, board, direction):
        new_board = board.copy()
        if direction == DOWN:
            new_board = self.move_down(new_board)
        else:
            new_board = self.rotate_2d((direction + 2) % 4, new_board)
            new_board = self.move_down(new_board)
            new_board = self.rotate_2d(direction, new_board)

        if board != new_board:
            # If there is a change, update it and add a tile
            self.board = new_board
            self.add_tile()
            # print("MOVE")
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

    def move_down(self, board):
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


class Game:
    def __init__(self, weights, boards_amt=32):
        self.boards_amt = boards_amt
        self.alive_boards = []
        for i in range(boards_amt):
            self.alive_boards.append(Board())
        # self.amt_alive = boards_amt
        self.fitness = 0
        self.prob = 0
        self.total_moves_survived = 0
        self.weights = weights
        print("Game created")

    # def crossover(self, other_game):
    #     # Brain.crossover returns weights list, so does mutate
    #     return self.brain.mutate(self.brain.crossover(other_game.brain))

    def reset(self, weights):
        self.alive_boards = []
        for i in range(self.boards_amt):
            self.alive_boards.append(Board())
        # self.amt_alive = boards_amt
        self.fitness = 0
        self.prob = 0
        self.weights = weights
        self.total_moves_survived = 0
        # self.add_tile()
        # self.add_tile()  # Two starting tiles

    def move_all(self, b):
        # Will return the list of predictions
        # boards_list = [self.boards[i].board for i in range(
        #     len(self.boards)) if self.boards[i].alive]
        inp_list = [self.alive_boards[i].board for i in range(
            len(self.alive_boards))]
        results = b.predict(inp_list, 12)
        amt = len(self.alive_boards)
        for i in range(amt - 1, -1, -1):
            if self.alive_boards[i].alive:
                self.alive_boards[i].move_AI(results[i])
                if not self.alive_boards[i].alive:
                    self.fitness += self.alive_boards[i].fitness
                    self.total_moves_survived +=  \
                        self.alive_boards[i].moves_survived
                    del self.alive_boards[i]
                    # self.move_AI(self.boards[i], results[i])

    def mutate(self):  # Mutates this pair of weights
        return brain.mutate_all(self.weights).copy()

    # Takes in another pair of weights
    def crossover_mutate(self, other_weights):
        final_weights = list(map(list, self.weights))
        for i in range(len(final_weights)):
            if i % 2 == 0:
                final_weights[i] = brain.crossover_2d(
                    final_weights[i], other_weights[i])
            else:
                final_weights[i] = brain.crossover_list(
                    final_weights[i], other_weights[i])
        final_weights = brain.mutate_all(list(map(list, final_weights)))
        return final_weights

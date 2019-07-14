import simulation as sim
import brain
import random
import time  # TODO REMOVE THIS


def pick_index(list):
    index = -1
    r = random.random()
    while r > 0:
        index += 1
        r -= list[index].prob
    return index


class GA:
    def __init__(self, pop_size):
        self.generation = 0
        self.brain = brain.Brain()
        self.current_member = 0
        self.pop_size = pop_size
        self.population = []
        self.games_per_member = 6
        for i in range(pop_size):
            # Create initial population!
            weights = self.brain.get_rand_weights()
            # print(weights[0][0][0])
            self.population.append(sim.Game(weights, self.games_per_member))
        self.highscore = 0
        curr_member = self.population[self.current_member]
        self.brain.set_weight(curr_member.weights)
        # self.best_model = self.population[0].brain.model

    # def save_best(self):
    #     self.best_model.save("2048Bot/models/Best model.h5")

    # def load(self):
    #     self.population[0].brain.load_best()

    def evolve(self):
        st = time.time()
        # 1. Evaluate fitness
        total_fit = 0
        for i in range(self.pop_size):
            # Make the fitness function squared
            # if self.population[i].fitness > self.highscore:
            #     self.highscore = self.population[i].fitness
            # TODO READD BEST MODEL
            #     self.best_model = self.population[i].brain.model
            # self.population[i].fitness *= self.population[i].fitness * \
            #     self.population[i].fitness
            avg_moves = (
                self.population[i].total_moves_survived/100) ** 3  # / \
            # self.games_per_member
            self.population[i].fitness = avg_moves * avg_moves
            total_fit += self.population[i].fitness
        for g in self.population:
            g.prob = g.fitness / total_fit

        st = time.time()

        # 2. Selection
        # Keep best in every gen
        weights_list = []  # self.best_model.get_weights()]
        st = time.time()
        for i in range(self.pop_size):  # - 1):
            # if random.random() > .5:  # 95% of pop is crossover
            parent_A = self.population[pick_index(self.population)]
            parent_B = self.population[pick_index(self.population)]
            tries = 0
            while parent_A == parent_B:
                parent_B = self.population[pick_index(self.population)]
                tries += 1
                if tries >= 250:
                    print("Duplicate found! :O")
                    break
            st = time.time()
            # 3. Crossover / Mutation
            # The crossover returns a mutated child weights
            weights_list.append(parent_A.crossover_mutate(parent_B.weights))
            st = time.time()
            # else:  # 5% of pop is random
            #     # print("Rand member added!")
            #     rand_weights = weights_list[0].copy()
            #     weights_list.append(brain.mutate_all(rand_weights, 1))

        for i in range(self.pop_size):
            self.population[i].reset(weights_list[i])
        # print(f"Population set in {time.time() - st}")
        st = time.time()
# TODO BUG LIST
# WHEN CROSSED OVER, THE WEIGHTS OF PARENT_A ARE CHANGED BC COPY IS
# CORRECTLY MADE!
# The first member of the next generation also doesn't have the correct weights
#

    def step(self):
        curr_member = self.population[self.current_member]
        try:
            # avg_score = curr_member.fitness / \
            #     (curr_member.boards_amt - len(curr_member.alive_boards))
            avg_score = curr_member.total_moves_survived / \
                (curr_member.boards_amt - len(curr_member.alive_boards))
        except:
            avg_score = -1
        if len(curr_member.alive_boards) > 0:  # Run all of the current boards
            curr_member.move_all(self.brain)
        elif self.current_member < self.pop_size - 1:
            # Then move onto the next member
            g = self.generation
            c = self.current_member
            print(
                f"Gen: {g} Mem: {c} Avg Score: {round(avg_score)}")
            self.current_member += 1
            curr_member = self.population[self.current_member]
            self.brain.set_weight(curr_member.weights)
        else:  # If all members boards have been finished, evolve!
            g = self.generation
            # fitness_list = [mem.fitness for mem in self.population]
            fitness_list = [
                mem.total_moves_survived for mem in self.population]
            total_avg = sum(fitness_list) / \
                (self.pop_size * self.games_per_member)
            print(
                f"-----Gen Complete: {g} Avg Score: {round(total_avg)}-----")
            self.evolve()
            self.current_member = 0
            self.generation += 1
            curr_member = self.population[self.current_member]
            self.brain.set_weight(curr_member.weights)
        return avg_score, len(curr_member.alive_boards)

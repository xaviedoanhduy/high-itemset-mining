from collections import defaultdict
from chromosome_node import ChromosomeNode
from hui import HUI
from pair import Pair
import random
import time
import psutil


class HUIGeneticAlgorithm:
    """Genetic algorithm for finding high utility itemsets."""

    def __init__(self, dataset_path, min_util):
        self.population = []
        self.population_size = 100
        self.generations = 10
        self.sub_population = []
        self.hui_sets = set()
        self.percentage = []
        self.min_utility = min_util
        self.mutation_probability = 0.1
        self.database, self.item_to_twu, self.item_to_twu_0, self.twu_pattern = self.process_dataset(dataset_path)

    def process_dataset(self, input_path):
        database = []
        item_to_twu = defaultdict(int)
        item_to_twu_0 = defaultdict(int)
        twu_patterns = set()

        with open(input_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith(("#", "%", "@")):
                    split = line.split(":")
                    items = split[0].split()
                    transaction_utility = int(split[1])
                    for item in items:
                        item = int(item)
                        twu = item_to_twu.get(item, 0) + transaction_utility
                        twu0 = item_to_twu_0.get(item, 0) + transaction_utility
                        item_to_twu[item] = twu
                        item_to_twu_0[item] = twu0

        with open(input_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith(("#", "%", "@")):
                    split = line.split(":")
                    items = [int(item) for item in split[0].split()]
                    utility_values = [int(value) for value in split[2].split()]

                    revised_transaction = []
                    pattern = []
                    for item, utility in zip(items, utility_values):
                        pair = Pair(item, utility)

                        if item_to_twu.get(pair.item, 0) >= self.min_utility:
                            revised_transaction.append(pair)
                            pattern.append(pair.item)
                        else:
                            item_to_twu_0.pop(pair.item, None)

                    database.append(revised_transaction)
                    twu_patterns.update(pattern)

        return database, item_to_twu, item_to_twu_0, sorted(list(twu_patterns))

    def select_parents(self):
        length = len(self.population)
        half_length = length // 2
        return random.randint(0, half_length - 1), random.randint(half_length, length - 1)

    def get_random_number(self):
        return random.randint(0, len(self.twu_pattern) - 1)

    def select_position(self):
        rand_num = random.random()
        for i, p in enumerate(self.percentage):
            if i == 0:
                if 0 <= rand_num <= p:
                    return i
            elif self.percentage[i - 1] < rand_num <= p:
                return i

    def calculate_fitness(self, chromosome, k):
        if k == 0:
            return 0

        fitness = 0
        for p in range(len(self.database)):
            i, j, q = 0, 0, 0
            temp, sum_util = 0, 0

            while j < k and q < len(self.database[p]) and i < len(chromosome):
                if chromosome[i] == 1:
                    if self.database[p][q].item < self.twu_pattern[i]:
                        q += 1
                    elif self.database[p][q].item == self.twu_pattern[i]:
                        sum_util += self.database[p][q].utility
                        j += 1
                        q += 1
                        temp += 1
                        i += 1
                    else:
                        j += 1
                        i += 1
                else:
                    i += 1
            if temp == k:
                fitness += sum_util

        return fitness

    def calculate_r_fitness(self):
        total_sum = sum(node.fitness for node in self.population) or 1
        temp_sum = 0
        for node in self.population:
            temp_sum += node.fitness
            node.r_fitness = temp_sum / total_sum

    def mutation(self):
        for i in range(self.population_size):
            if random.random() < self.mutation_probability:
                mutation_point = self.get_random_number()

                new_chromosome = 1 - self.sub_population[i].chromosome[mutation_point]
                self.sub_population[i].chromosome[mutation_point] = new_chromosome

                k = sum(self.sub_population[i].chromosome)
                self.sub_population[i].fitness = self.calculate_fitness(
                    self.sub_population[i].chromosome, k
                )

                if self.sub_population[i].fitness >= self.min_utility:
                    self.insert(self.sub_population[i])

        return self.sub_population

    def insert(self, chromosome_node):
        itemset = " ".join(
            str(self.twu_pattern[i])
            for i in range(len(self.twu_pattern))
            if chromosome_node.chromosome[i] == 1
        )

        self.hui_sets.add(HUI(itemset, chromosome_node.fitness))

    def crossover(self, parent_1, parent_2):
        child_1 = []
        child_2 = []
        k_child_1 = 0
        k_child_2 = 0
        position = self.get_random_number()

        for i in range(len(self.twu_pattern)):
            if i <= position:
                child_1.append(self.population[parent_1].chromosome[i])
                if child_1[-1] == 1:
                    k_child_1 += 1

                child_2.append(self.population[parent_2].chromosome[i])
                if child_2[-1] == 1:
                    k_child_2 += 1

            else:
                child_1.append(self.population[parent_2].chromosome[i])
                if child_1[-1] == 1:
                    k_child_1 += 1

                child_2.append(self.population[parent_1].chromosome[i])
                if child_2[-1] == 1:
                    k_child_2 += 1

        chromosome_node = ChromosomeNode(len(self.twu_pattern))
        chromosome_node.chromosome = child_1
        chromosome_node.fitness = self.calculate_fitness(child_1, k_child_1)

        self.sub_population.append(chromosome_node)

        if chromosome_node.fitness >= self.min_utility:
            self.insert(chromosome_node)

        chromosome_node.chromosome = child_2
        chromosome_node.fitness = self.calculate_fitness(child_2, k_child_2)

        if chromosome_node.fitness >= self.min_utility:
            self.insert(chromosome_node)

    def roulette_percent(self):
        percentage = []
        total_sum = sum(self.item_to_twu.values())
        temp_sum = 0
        for item in self.twu_pattern:
            temp_sum += self.item_to_twu[item]
            percentage.append(temp_sum / total_sum)
        return percentage

    def generate_population(self):
        self.percentage = self.roulette_percent()

        for _ in range(self.population_size):
            chromosome_node = ChromosomeNode(len(self.twu_pattern))
            print(chromosome_node)
            # k = self.get_random_number()
            #
            # for j in range(k):
            #     pos = self.select_position()
            #     # pos = random.randint(0, len(self.twu_pattern) - 1)
            #     if pos is not None and chromosome_node.chromosome[pos] == 0:
            #         chromosome_node.chromosome[pos] = 1
            #
            # chromosome_node.fitness = self.calculate_fitness(
            #     chromosome_node.chromosome,
            #     k
            # )
            # self.population.append(chromosome_node)
            #
            # if chromosome_node.fitness >= self.min_utility:
            #     self.insert(chromosome_node)

    def run_algorithm(self):
        self.generate_population()

        # for _ in range(self.generations):
        #     self.percentage = self.roulette_percent()
        #     self.calculate_r_fitness()
        #
        #     while len(self.sub_population) < self.population_size:
        #         parent_1, parent_2 = self.select_parents()
        #
        #         self.crossover(parent_1, parent_2)
        #
        #     self.sub_population = self.mutation()
        #     self.sub_population.extend(self.population)
        #
        #     self.population = self.sub_population[: self.population_size]
        #
        #     self.sub_population = []

    def write_out(self, output_path):
        with open(output_path, "w") as file:
            buffer = []
            for hui in self.hui_sets:
                buffer.append(f"{hui.itemset} #UTIL: {hui.fitness}")
            file.write("\n".join(buffer) + "\n")


if __name__ == "__main__":
    data_path = "db_utility.txt"
    min_utility = 22

    ga_algo = HUIGeneticAlgorithm(data_path, min_utility)

    time_s = time.time()
    process_start = psutil.Process()
    memory_start_info = process_start.memory_info()
    cur_memory_start = memory_start_info.rss / 1024 / 1024

    ga_algo.run_algorithm()

    ga_algo.write_out("output.txt")

    process_end = psutil.Process()
    memory_end_info = process_end.memory_info()
    cur_memory_end = memory_end_info.rss / 1024 / 1024

    time_e = time.time()
    total_time = time_e - time_s
    max_memory = cur_memory_end - cur_memory_start
    print(f"> Total time: ~ {total_time:.3f} s")
    print(f"> Max memory (mb) ~ {max_memory} mb")
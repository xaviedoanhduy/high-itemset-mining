from pair import Pair
from chromosome_node import ChromosomeNode
from hui import HUI
import random
import time
import psutil


def calculate_mutation_rates(m, n):
    if m > n:
        p_min = 1 / m
        p_max = 1 / n
    else:
        p_min = 1 / n
        p_max = 1 / m
    return p_max, p_min


def select(percentage):
    rand_num = random.random()
    for i, p in enumerate(percentage):
        if i == 0:
            if 0 <= rand_num <= p:
                return i
        elif percentage[i - 1] < rand_num <= p:
            return i


def rank_data(temp_pop):
    for i in range(len(temp_pop) - 1):
        p = i

        for j in range(i + 1, len(temp_pop)):
            if temp_pop[p].fitness < temp_pop[j].fitness:
                p = j

        if i != p:
            temp_pop[i], temp_pop[p] = temp_pop[p], temp_pop[i]

        temp_pop[i].rank = i + 1

    temp_pop[-1].rank = len(temp_pop)


class AlgoHUIMGA:
    def __init__(self):
        self.max_memory = 0
        self.total_time = 0.0
        self.pop_size = 100
        self.generations = 10
        self.item_to_twu = {}
        self.item_to_twu0 = {}
        self.twu_pattern = []
        self.writer = None
        self.population = []
        self.sub_population = []
        self.hui_sets = set()
        self.database = []
        self.percentage = []

    def run_algorithm(self, input_path, output_path, min_utility):
        start_timestamp = time.time()

        process_start = psutil.Process()
        memory_start_info = process_start.memory_info()
        cur_memory_start = memory_start_info.rss / 1024 / 1024

        self.writer = open(output_path, "w")

        with open(input_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith(("#", "%", "@")):
                    split = line.split(":")
                    items = split[0].split()
                    transaction_utility = int(split[1])
                    for item in items:
                        item = int(item)
                        twu = self.item_to_twu.get(item, 0) + transaction_utility
                        twu0 = self.item_to_twu0.get(item, 0) + transaction_utility
                        self.item_to_twu[item] = twu
                        self.item_to_twu0[item] = twu0

        with open(input_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith(("#", "%", "@")):
                    split = line.split(":")
                    items = [int(item) for item in split[0].split()]
                    utility_values = [int(value) for value in split[2].split()]

                    revised_transaction = []
                    pattern = []
                    for i in range(len(items)):
                        pair = Pair(items[i], utility_values[i])

                        if self.item_to_twu.get(pair.item, 0) >= min_utility:
                            revised_transaction.append(pair)
                            pattern.append(pair.item)
                        else:
                            self.item_to_twu0.pop(pair.item, None)

                    self.database.append(revised_transaction)

        self.twu_pattern = sorted(list(self.item_to_twu0.keys()))

        if self.twu_pattern:
            p_max, p_min = calculate_mutation_rates(
                len(self.database), len(self.twu_pattern)
            )

            self.generate_population(min_utility)

            for i in range(self.generations):
                self.percentage = self.roulette_percent()
                self.calculate_r_fitness()
                while len(self.sub_population) < self.pop_size:
                    temp_1 = self.select_chromosome()
                    temp_2 = self.select_chromosome()

                    while temp_1 == temp_2:
                        temp_2 = self.select_chromosome()

                    self.crossover(temp_1, temp_2, min_utility)

                self.sub_population = self.ranked_mutation(p_max, p_min, i, min_utility)
                self.sub_population.extend(self.population)

                rank_data(self.sub_population)
                self.population = self.sub_population[: self.pop_size]

                self.sub_population = []

        self.write_out()
        self.writer.close()

        end_timestamp = time.time()

        process_end = psutil.Process()
        memory_end_info = process_end.memory_info()
        cur_memory_end = memory_end_info.rss / 1024 / 1024

        self.total_time = end_timestamp - start_timestamp
        self.max_memory = cur_memory_end - cur_memory_start

    def generate_population(self, min_utility):
        i = 0
        self.percentage = self.roulette_percent()

        while i < self.pop_size:
            temp_node = ChromosomeNode(len(self.twu_pattern))
            k = random.randint(0, len(self.twu_pattern))
            for j in range(k):
                temp = select(self.percentage)
                if temp is not None and temp_node.chromosome[temp] == 0:
                    temp_node.chromosome[temp] = 1

            temp_node.fitness = self.fit_calculate(temp_node.chromosome, k)
            temp_node.rank = 0
            self.population.append(temp_node)
            if temp_node.fitness >= min_utility:
                self.insert(temp_node)
            i += 1

    def roulette_percent(self):
        percentage = []
        total_sum = sum(self.item_to_twu.values())
        temp_sum = 0
        for item in self.twu_pattern:
            temp_sum += self.item_to_twu[item]
            percentage.append(temp_sum / total_sum)
        return percentage

    def crossover(self, temp_1, temp_2, min_utility):
        temp_a = 0
        temp_b = 0
        temp_1_chro = []
        temp_2_chro = []

        position = random.randint(0, len(self.twu_pattern) - 1)
        for i in range(len(self.twu_pattern)):
            if i <= position:
                temp_1_chro.append(self.population[temp_2].chromosome[i])
                if temp_1_chro[-1] == 1:
                    temp_a += 1
                temp_2_chro.append(self.population[temp_1].chromosome[i])
                if temp_2_chro[-1] == 1:
                    temp_b += 1
            else:
                temp_1_chro.append(self.population[temp_1].chromosome[i])
                if temp_1_chro[-1] == 1:
                    temp_a += 1
                temp_2_chro.append(self.population[temp_2].chromosome[i])
                if temp_2_chro[-1] == 1:
                    temp_b += 1

        temp_node = ChromosomeNode(len(self.twu_pattern))
        temp_node.chromosome = temp_1_chro
        temp_node.fitness = self.fit_calculate(temp_1_chro, temp_a)
        temp_node.rank = 0
        self.sub_population.append(temp_node)

        if temp_node.fitness >= min_utility:
            self.insert(temp_node)

        temp_node.chromosome = temp_2_chro
        temp_node.fitness = self.fit_calculate(temp_2_chro, temp_b)
        temp_node.rank = 0
        self.sub_population.append(temp_node)

        if temp_node.fitness >= min_utility:
            self.insert(temp_node)

    def get_rank(self):
        rank = []
        for i in range(len(self.sub_population)):
            temp = sum(
                1
                for j in range(len(self.sub_population))
                if i != j
                and self.sub_population[i].fitness <= self.sub_population[j].fitness
            )
            rank.append(temp + 1)
        return rank

    def ranked_mutation(self, p_max, p_min, current_iteration, min_utility):
        record = self.get_rank()
        for i in range(self.pop_size):
            pm = (
                (p_max - (p_max - p_min) * current_iteration / self.generations)
                * record[i]
                / self.pop_size
            )
            rank_num = random.random()

            if rank_num < pm:
                temp = random.randint(0, len(self.twu_pattern) - 1)
                self.sub_population[i].chromosome[temp] = (
                    1 - self.sub_population[i].chromosome[temp]
                )

                k = sum(self.sub_population[i].chromosome)
                self.sub_population[i].fitness = self.fit_calculate(
                    self.sub_population[i].chromosome, k
                )

                if self.sub_population[i].fitness >= min_utility:
                    self.insert(self.sub_population[i])

        return self.sub_population

    def insert(self, temp_chro_node):
        itemset = " ".join(
            str(self.twu_pattern[i])
            for i in range(len(self.twu_pattern))
            if temp_chro_node.chromosome[i] == 1
        )

        self.hui_sets.add(HUI(itemset, temp_chro_node.fitness))

    def fit_calculate(self, temp_chro_node, k):
        if k == 0:
            return 0
        fitness = 0
        for p in range(len(self.database)):
            i = j = q = temp = sum = 0
            while j < k and q < len(self.database[p]) and i < len(temp_chro_node):
                if temp_chro_node[i] == 1:
                    if self.database[p][q].item < self.twu_pattern[i]:
                        q += 1
                    elif self.database[p][q].item == self.twu_pattern[i]:
                        sum += self.database[p][q].utility
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
                fitness += sum
        return fitness

    def calculate_r_fitness(self):
        total_sum = sum(node.fitness for node in self.population) or 1
        temp_sum = 0
        for node in self.population:
            temp_sum += node.fitness
            node.r_fitness = temp_sum / total_sum

    def select_chromosome(self):
        rand_num = random.random()
        for i, node in enumerate(self.population):
            if i == 0:
                if 0 <= rand_num <= node.r_fitness:
                    return i
            elif self.population[i - 1].r_fitness < rand_num <= node.r_fitness:
                return i

    def write_out(self):
        buffer = []
        for hui in self.hui_sets:
            buffer.append(f"{hui.itemset} #UTIL: {hui.fitness}")
        self.writer.write("\n".join(buffer) + "\n")

    def print_result(self):
        print("============= HUI GA ALGORITHM - 0.97e - STATS =============")
        print(f"> High-utility itemsets count: {len(self.hui_sets)}")
        print(f"> Total time: ~ {self.total_time:.3f} s")
        print(f"> Max memory (mb) ~ {self.max_memory} mb")


if __name__ == "__main__":
    input_file = "db_utility.txt"
    output_file = "output.txt"
    min_utility = 20

    algo = AlgoHUIMGA()

    algo.run_algorithm(input_file, output_file, min_utility)

    algo.print_result()

import random
from bitarray import bitarray
import time
import multiprocessing as mp


class ChromosomeNode:
    def __init__(self, chromosome_bits):
        self.chromosome = chromosome_bits
        self.fitness = 0    # fitness value of chromosome
        self.r_fitness = 0.0


class HUI:
    def __init__(self, itemset, fitness):
        self.itemset = itemset
        self.fitness = fitness

    def __hash__(self):
        return hash(self.itemset)

    def __eq__(self, other):
        return self.itemset == other.itemset


class Transaction:
    def __init__(self, tran_bits, value_items, length=0):
        bits = bitarray(length)
        bits.setall(0)
        self.tran_bits = tran_bits if tran_bits else bits
        self.value_items = value_items if value_items else {}


def generate_random_bitarray(size):
    random_bits = [random.choice([0, 1]) for _ in range(size)]

    random_bitarray = bitarray(random_bits)

    return random_bitarray


class HUIGeneticAlgorithm:
    def __init__(self, dataset_path, min_util):
        self.population = []
        self.population_size = 50
        self.generations = 10
        self.sub_population = []
        self.hui_sets = set()
        self.percentage = []
        self.min_utility = min_util
        self.mutation_probability = 0.1
        self.database, self.item_to_twu, self.t_ids, self.twu_pattern = self.process_dataset(dataset_path)

    def process_dataset(self, input_path):
        database = []
        item_to_twu = {}
        item_to_twu_0 = {}
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
            t_ids = []
            for line in file:
                line = line.strip()
                if line and not line.startswith(("#", "%", "@")):
                    split = line.split(":")
                    items = [int(item) for item in split[0].split()]
                    utility_values = [int(value) for value in split[2].split()]

                    revised_transaction = {}

                    pattern = []
                    t_id = []
                    for item, utility in zip(items, utility_values):
                        t_id.append(item)
                        if item_to_twu.get(item, 0) >= self.min_utility:
                            revised_transaction[item] = utility
                            pattern.append(item)

                        else:
                            item_to_twu_0.pop(item, None)

                    database.append(revised_transaction)
                    twu_patterns.update(pattern)

                t_ids.append(t_id)

            t_ids_bits = []
            for t_id in t_ids:
                t_bit = bitarray(len(list(twu_patterns)))
                t_bit.setall(0)
                for item in t_id:
                    t_bit[item - 1] = 1

                t_ids_bits.append(t_bit)
        print(t_ids_bits)
        return database, item_to_twu, t_ids_bits, sorted(list(twu_patterns))

    def calculate_fitness(self, chromosome):
        fitness = 0
        bit_ones = [i for i, bit in enumerate(chromosome) if bit]

        for i, t_id in enumerate(self.t_ids):
            if (t_id & chromosome) == chromosome:
                for j in bit_ones:
                    fitness += self.database[i].get(self.twu_pattern[j], 0)
        print(chromosome, ":", fitness)
        return fitness

    def calculate_fitness_parallel(self):
        pool = mp.Pool(mp.cpu_count())
        results = pool.map(self.calculate_fitness, self.population)
        pool.close()
        pool.join()

        for i, chromosome in enumerate(self.population):
            chromosome.fitness = results[i]

    def calculate_r_fitness(self):
        total_sum = 0
        for node in self.population:
            total_sum += node.fitness
        if total_sum == 0:
            total_sum = 1
        temp_sum = 0
        for node in self.population:
            temp_sum += node.fitness
            node.r_fitness = temp_sum / total_sum

    def generate_population(self):
        for _ in range(self.population_size):
            chromosome_bits = generate_random_bitarray(len(self.twu_pattern))
            chromosome_node = ChromosomeNode(chromosome_bits)
            chromosome_node.fitness = self.calculate_fitness(chromosome_bits)

    def run_algorithm(self):
        self.generate_population()
        self.calculate_fitness_parallel()


if __name__ == "__main__":
    data_path = "chainstore.txt"
    min_utility = 20

    ga_algo = HUIGeneticAlgorithm(data_path, min_utility)

    time_s = time.time()

    ga_algo.run_algorithm()

    time_e = time.time()
    total_time = time_e - time_s
    print(f"> Total time: ~ {total_time:.3f}s")

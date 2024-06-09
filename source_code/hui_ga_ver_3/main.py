from bitarray import bitarray
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
import random


class ChromosomeNode:
    def __init__(self, length=0):
        bits = bitarray(length)
        bits.setall(0)
        self.chromosome = bits
        self.fitness = 0    # fitness value of chromosome


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


class HUIGeneticAlgorithm:
    def __init__(self, dataset_path, min_util):
        self.population = []
        self.population_size = 10
        self.generations = 10
        self.sub_population = []
        self.hui_sets = set()
        self.percentage = []
        self.min_utility = min_util
        self.mutation_probability = 0.1
        self.crossover_probability = 0.8
        self.max_item = 0
        self.database, self.item_to_twu, self.transactions, self.twu_pattern = self.process_dataset(dataset_path)

    def process_dataset(self, input_path):
        database = []
        item_to_twu = {}
        item_to_twu_0 = {}
        twu_patterns = set()

        print("Processing dataset...")

        with open(input_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith(("#", "%", "@")):
                    split = line.split(":")
                    items = split[0].split()
                    transaction_utility = int(split[1])

                    if len(items) > self.max_item:
                        self.max_item = len(items)

                    for item in items:
                        item = int(item)
                        twu = item_to_twu.get(item, 0) + transaction_utility
                        twu0 = item_to_twu_0.get(item, 0) + transaction_utility
                        item_to_twu[item] = twu
                        item_to_twu_0[item] = twu0

        with open(input_path, "r") as file:
            t_ids = []
            transactions = []
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

                    tran = self.create_transaction(items, utility_values, item_to_twu_0)
                    transactions.append(tran)

                    database.append(revised_transaction)
                    twu_patterns.update(pattern)

                t_ids.append(t_id)

        print("Data is processed.")

        return database, item_to_twu, transactions, sorted(list(twu_patterns))

    def create_transaction(self, items, utility_values, item_to_twu_0):
        # transactions = []
        t_bit = bitarray(self.max_item)
        t_bit.setall(0)

        dic_t = {}
        for i in range(len(items)):
            if items[i] in item_to_twu_0:
                t_bit[items[i] - 1] = 1
                dic_t[items[i]] = utility_values[i]

        tran = Transaction(t_bit, dic_t)
        # transactions.append(tran)

        # print("Done getting transaction")
        # return transactions
        # print(f"tran {tran.tran_bits}: {tran.value_items}")
        return tran

    def calculate_fitness(self, chromosome):
        fitness = 0
        for tran in self.transactions:
            if (tran.tran_bits & chromosome) == chromosome:
                for pos in chromosome.search(bitarray("1")):
                    fitness += tran.value_items.get(pos + 1)

        return fitness

    def select_parents(self):
        length = len(self.population)
        half_length = length // 2
        parent_1 = self.population[random.randint(0, half_length - 1)]
        parent_2 = self.population[random.randint(half_length, length - 1)]
        return parent_1, parent_2

    def crossover(self, parent_1, parent_2):
        if random.random() > self.crossover_probability:
            return parent_1, parent_2

        child_1 = parent_1.chromosome.copy()
        child_2 = parent_2.chromosome.copy()

        crossover_point = random.randint(1, len(child_1) - 2)

        child_1[crossover_point:] = parent_2.chromosome[crossover_point:]
        child_2[crossover_point:] = parent_1.chromosome[crossover_point:]

        child_1_fitness = self.calculate_fitness(child_1)
        child_2_fitness = self.calculate_fitness(child_2)

        if child_1_fitness < parent_1.fitness:
            child_node_1 = parent_1

        else:
            child_node_1 = ChromosomeNode(len(child_1))
            child_node_1.chromosome = child_1
            child_node_1.fitness = child_1_fitness

        if child_2_fitness < parent_2.fitness:
            child_node_2 = parent_2

        else:
            child_node_2 = ChromosomeNode(len(child_2))
            child_node_2.chromosome = child_2
            child_node_2.fitness = child_2_fitness

        return child_node_1, child_node_2

    def mutate(self, chromosome_node):
        if random.random() > self.mutation_probability:
            return chromosome_node

        mutated_chromosome = chromosome_node.chromosome.copy()
        one_bit_positions = [pos for pos in mutated_chromosome.search(bitarray("1"))]
        if one_bit_positions:
            position_to_mutate = random.choice(one_bit_positions)

            mutated_chromosome[position_to_mutate] = 0

            mutated_fitness = self.calculate_fitness(mutated_chromosome)

            if mutated_fitness < chromosome_node.fitness:
                return chromosome_node

            chromosome_node.chromosome = mutated_chromosome
            chromosome_node.fitness = mutated_fitness

        return chromosome_node

    def generate_population(self):
        chromosome_nodes = []

        for _ in range(self.population_size):
            chromosome_length = len(self.twu_pattern)
            chromosome_bits = bitarray(chromosome_length)

            for i in range(chromosome_length):
                chromosome_bits[i] = random.randint(0, 1)

            chromosome_node = ChromosomeNode(chromosome_length)
            chromosome_node.chromosome = chromosome_bits
            chromosome_nodes.append(chromosome_node)

        num_workers = multiprocessing.cpu_count()
        segment_size = len(chromosome_nodes) // num_workers
        futures = []

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            for i in range(num_workers):
                start = i * segment_size
                end = None if i == num_workers - 1 else (i + 1) * segment_size
                segment = chromosome_nodes[start:end]
                futures.extend(
                    executor.submit(
                        self.calculate_fitness, node.chromosome
                    )
                    for node in segment
                )

            fitness_values = [future.result() for future in as_completed(futures)]

        sorted_population = sorted(
            zip(chromosome_nodes, fitness_values),
            key=lambda x: x[1],
            reverse=True
        )

        for node, _ in sorted_population[:self.population_size]:
            self.population.append(node)

        # for individual in self.population:
        #     print(f"{individual.chromosome}: {individual.fitness}")

    def run_algorithm(self, dataset_path):
        self.generate_population()

        for i in range(self.generations):
            print(f"Generation: {i + 1}")
            while len(self.sub_population) < self.population_size:
                parent_1, parent_2 = self.select_parents()
                child_1, child_2 = self.crossover(parent_1, parent_2)

                mutated_child_1 = self.mutate(child_1)
                mutated_child_2 = self.mutate(child_2)
                self.sub_population.append(mutated_child_1)
                self.sub_population.append(mutated_child_2)

            self.sub_population.extend(self.population)

            sorted_population = sorted(
                self.sub_population,
                key=lambda x: x.fitness,
                reverse=True
            )

            self.population = sorted_population[:self.population_size]

            self.sub_population = []

            print(f"Population: {len(self.population)}")
            for individual in self.population:
                print(f"{individual.chromosome}: {individual.fitness}")

            # print(f"Sub Population: {len(self.sub_population)}")
            # print("================================================")

            # for individual in self.sub_population:
            #     print(f"{individual.chromosome}: {individual.fitness}")


if __name__ == "__main__":
    data_path = "db_utility.txt"
    min_utility = 20

    ga_algo = HUIGeneticAlgorithm(data_path, min_utility)

    ga_algo.run_algorithm(data_path)

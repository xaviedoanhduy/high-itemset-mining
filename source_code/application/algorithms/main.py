from .parallel import ParallelCalculateFitness
from .transaction_utility import TransactionUtilities
from .chromosome_node import ChromosomeNode
from bitarray import bitarray
from bitarray.util import ba2int

import random
import time
import psutil


class HUIGeneticAlgorithm:
    def __init__(self, dataset_path, min_utility=0, population_size=100, generations=10, crossover_probability=0.8, mutation_probability=0.1):
        self.dataset_path = dataset_path
        self.population = []
        self.population_size = population_size
        self.generations = generations
        self.hui_sets = set()
        self.min_utility = min_utility
        self.support_rate = 0
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.biggest_item = 0
        self.avg_len = 0
        self.transactions = []
        self.writer = None
        self.existing_chromosomes = set()

    def get_transaction(self):
        print("* Processing dataset...")
        start_time = time.time()
        items_list = []
        utility_values_list = []
        transactions = []
        total_tran_values = 0
        total_number_items = 0
        with open(self.dataset_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith(("#", "%", "@")):
                    split = line.split(":")
                    items = [int(item) for item in split[0].split()]
                    total_tran_values += int(split[1])
                    utility_values = [int(value) for value in split[2].split()]
                    items_list.append(items)
                    utility_values_list.append(utility_values)
                    total_number_items += len(items)
                    for item in items:
                        if item > self.biggest_item:
                            self.biggest_item = item

            for i in range(len(items_list)):
                tran = self.create_transaction(items_list[i], utility_values_list[i])
                transactions.append(tran)
        self.avg_len = total_number_items // len(transactions)
        total_time = time.time() - start_time
        print(f"* Data is processed: ~ {total_time:.3f} s")
        return transactions

    def create_transaction(self, items, utility_values):
        t_bit = bitarray(self.biggest_item)
        t_bit.setall(0)

        dic_t = {}
        for i in range(len(items)):
            t_bit[items[i] - 1] = 1
            dic_t[items[i]] = utility_values[i]

        transaction = TransactionUtilities(t_bit, dic_t)

        return transaction

    def check_exists(self, chromosome_bits):
        int_bit = ba2int(chromosome_bits)
        if int_bit in self.existing_chromosomes:
            return True
        self.existing_chromosomes.add(int_bit)
        return False

    def calculate_fitness(self, chromosome_bits):
        parallel_calculate_fitness = ParallelCalculateFitness(self.transactions, chromosome_bits)
        result = parallel_calculate_fitness.parallel_calculate_fitness()
        return result

    def select_parents(self):
        remaining_population = self.population[self.population_size // 2:]
        length = len(remaining_population)
        half_length = length // 2
        parent_1 = remaining_population[random.randint(0, half_length - 1)]
        parent_2 = remaining_population[random.randint(half_length, length - 1)]
        return parent_1, parent_2

    def crossover_two_point(self, parent_1, parent_2):
        parent_1_bits = parent_1.bits
        parent_2_bits = parent_2.bits

        # "For crossover one point"
        # crossover_point = random.randint(1, len(parent_1_bits) - 1)
        # child_1_bits = parent_1_bits[:crossover_point] + parent_2_bits[crossover_point:]
        # child_2_bits = parent_2_bits[:crossover_point] + parent_1_bits[crossover_point:]

        "For crossover two point"
        s = random.randint(1, self.biggest_item // 2)   # start point
        e = random.randint(s + 1, self.biggest_item - 1)   # end point

        child_1_bits = parent_1_bits[:s] + parent_2_bits[s:e] + parent_1_bits[e:]
        child_2_bits = parent_2_bits[:s] + parent_1_bits[s:e] + parent_2_bits[e:]

        child_1_fitness = self.calculate_fitness(child_1_bits)
        child_2_fitness = self.calculate_fitness(child_2_bits)

        child_node_1 = ChromosomeNode(child_1_bits, child_1_fitness)

        child_node_2 = ChromosomeNode(child_2_bits, child_2_fitness)

        if child_node_1.fitness >= self.min_utility:
            self.insert_hui_set(child_node_1)

        if child_node_2.fitness >= self.min_utility:
            self.insert_hui_set(child_node_2)

        return child_node_1, child_node_2

    def mutate(self, chromosome_node):
        mutated_chromosome_bits = chromosome_node.bits

        random_pos = random.choice(mutated_chromosome_bits)
        mutated_chromosome_bits[random_pos] = 1 - mutated_chromosome_bits[random_pos]

        mutated_fitness = self.calculate_fitness(mutated_chromosome_bits)
        chromosome_node.bits = mutated_chromosome_bits
        chromosome_node.fitness = mutated_fitness

        if mutated_fitness >= self.min_utility:
            self.insert_hui_set(chromosome_node)

        return chromosome_node

    def generate_population(self):
        print("* Generating population...")

        while len(self.population) < self.population_size:
            chromosome_bits = bitarray(self.biggest_item)

            chromosome_bits.setall(0)
            n = random.randint(1, self.avg_len)

            arr = random.sample(range(1, self.biggest_item + 1), n)
            for item in arr:
                chromosome_bits[item - 1] = 1

            fitness = self.calculate_fitness(chromosome_bits)
            chromosome_node = ChromosomeNode(chromosome_bits, fitness)

            int_bit = ba2int(chromosome_node.bits)
            self.existing_chromosomes.add(int_bit)
            self.population.append(chromosome_node)

            if chromosome_node.fitness >= self.min_utility:
                self.insert_hui_set(chromosome_node)

    def insert_hui_set(self, chromosome_node):
        itemset = " ".join(
            str(i + 1)
            for i in range(self.biggest_item)
            if chromosome_node.bits[i] == 1
        )

        utility = chromosome_node.fitness
        self.hui_sets.add((itemset, utility))

    def write_out(self):
        buffer = []
        sorted_hui_sets = sorted(
            self.hui_sets,
            key=lambda x: x[1],
            reverse=True
        )
        for hui in sorted_hui_sets:
            buffer.append(f"{hui[0]} #UTIL: {hui[1]}")
        self.writer.write("\n".join(buffer) + "\n")

    def run_algorithm(self, output_result="output.txt"):
        start_time = time.time()

        self.writer = open(output_result, "w")

        # create transactions list
        self.transactions = self.get_transaction()

        # initial population
        self.generate_population()
        print(f"* Population is generated: ~ {time.time() - start_time:.3f} s")

        for i in range(self.generations):
            # sub_population = []
            sub_population = self.population[:self.population_size // 2]
            start_gen_time = time.time()
            print(f"+ Generation: {i + 1}:", end=" ")

            while len(sub_population) < self.population_size:
                parent_1, parent_2 = self.select_parents()

                # Crossover
                if random.random() < self.crossover_probability:
                    child_1, child_2 = self.crossover_two_point(parent_1, parent_2)

                    if not self.check_exists(child_1.bits):
                        sub_population.append(child_1)

                    if not self.check_exists(child_1.bits):
                        sub_population.append(child_2)
                else:
                    sub_population.extend([parent_1, parent_2])

                # Mutation
                child_to_mutate, child_to_add = self.select_parents()

                if random.random() < self.mutation_probability:
                    mutated_child = self.mutate(child_to_mutate)

                    if not self.check_exists(child_to_mutate.bits):
                        sub_population.append(mutated_child)
                else:
                    sub_population.extend([child_to_mutate, child_to_add])

            sub_population.extend(self.population)
            self.existing_chromosomes.clear()

            self.population = sub_population

            print(f"~ {time.time() - start_gen_time:.3f} s")

        self.write_out()
        self.writer.close()


if __name__ == "__main__":
    data_path = "dataset/chess.txt"
    min_utility = 1000
    pop_size = 500
    generations = 10
    crossover_probability = 0.8
    mutation_probability = 0.1
    output_path = "output.txt"

    ga_algo = HUIGeneticAlgorithm(
        data_path,
        min_utility,
        pop_size,
        generations,
        crossover_probability,
        mutation_probability
    )
    ga_algo.run_algorithm(output_path)

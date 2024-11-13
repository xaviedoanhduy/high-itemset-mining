from bitarray import bitarray
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing as cpu

class Individual:
    def __init__(self, bits, fitness=0):
        self.bits = bits
        self.fitness = fitness

class Transaction:
    def __init__(self, tran_bits, value_items, length):
        bits = bitarray(length)
        bits.setall(0)
        self.tran_bits = tran_bits if tran_bits else bits
        self.value_items = value_items if value_items else {}

class TransactionProcessor:
    def __init__(self):
        self.biggest_item = 0

    def load_transactions(self, input):
        items_list = []
        utility_values_list = []
        transactions = []

        with open(input, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith(("#", "%", "@")):
                    split = line.split(":")
                    items = [int(item) for item in split[0].split()]
                    utility_values = [int(value) for value in split[2].split()]
                    items_list.append(items)
                    utility_values_list.append(utility_values)
                    for item in items:
                        self.biggest_item = max(self.biggest_item, item)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_transaction, items_list[i], utility_values_list[i]) for i in range(len(items_list))]
            for future in futures:
                transactions.append(future.result())
        return transactions

    def create_transaction(self, items, utility_values):
        tran_bits = bitarray(self.biggest_item)
        tran_bits.setall(0)
        value_items = {item: value for item, value in zip(items, utility_values)}
        for item in items:
            tran_bits[item - 1] = 1
        return Transaction(tran_bits, value_items, len(tran_bits))

class FitnessCalculator:
    def __init__(self, transactions, Individual_bits):
        self.transactions = transactions
        self.Individual_bits = Individual_bits
        self.num_workers = cpu.cpu_count() // 2

    def calc_fitness(self, transaction):
        fitness = 0
        mask = transaction.tran_bits & self.Individual_bits
        if mask == self.Individual_bits:
            for pos in range(len(self.Individual_bits)):
                if self.Individual_bits[pos] == 1:
                    fitness += transaction.value_items.get(pos + 1, 0)
        return fitness

    def calculate(self):
        segment_size = (len(self.transactions) + self.num_workers - 1) // self.num_workers
        futures = []

        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            for i in range(self.num_workers):
                start = i * segment_size
                end = None if i == self.num_workers - 1 else (i + 1) * segment_size
                segment = self.transactions[start:end]
                futures.append(executor.submit(self.process_segment, segment))

            total_fitness = sum(future.result() for future in as_completed(futures))

        return total_fitness

    def process_segment(self, segment):
        total_fitness = 0
        for transaction in segment:
            total_fitness += self.calc_fitness(transaction)
        return total_fitness

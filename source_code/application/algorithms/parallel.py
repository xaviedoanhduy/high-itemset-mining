from concurrent.futures import ThreadPoolExecutor, as_completed
from bitarray import bitarray
import multiprocessing


class ParallelCalculateFitness:
    def __init__(self, transactions, chromosome_bits):
        self.transactions = transactions
        self.chromosome_bits = chromosome_bits
        num_workers = multiprocessing.cpu_count()
        self.num_workers = num_workers if num_workers else 4

    def calculate_fitness(self, segment):
        fitness = 0
        for element in segment:
            mask = element.tran_bits & self.chromosome_bits
            if mask == self.chromosome_bits:
                for pos in self.chromosome_bits.search(bitarray("1")):
                    fitness += element.value_items.get(pos + 1)
        return fitness

    def parallel_calculate_fitness(self):
        segment_size = (len(self.transactions) + self.num_workers - 1) // self.num_workers
        futures = []

        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            for i in range(self.num_workers):
                start = i * segment_size
                end = None if i == self.num_workers - 1 else (i + 1) * segment_size
                segment = self.transactions[start:end]
                futures.append(executor.submit(self.calculate_fitness, segment))

            total_fitness = sum(future.result() for future in as_completed(futures))

        return total_fitness

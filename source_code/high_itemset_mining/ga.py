from __future__ import annotations

import random
import time
from collections.abc import Callable
from pathlib import Path

import psutil
from bitarray import bitarray

from .fitness import calculate_fitness
from .loader import calculate_twu, load_transactions
from .models import Individual, Transaction

HuiSet = set[tuple[tuple[bool, ...], int]]
CrossoverFn = Callable[[Individual, Individual], tuple[Individual, Individual]]


class GeneticAlgorithm:
    def __init__(
        self,
        dataset_path: Path | str,
        min_utility: int,
        population_size: int,
        generations: int,
        crossover_prob: float,
        mutation_prob: float,
        output: Path | str,
    ) -> None:
        self.dataset_path = Path(dataset_path)
        self.output = Path(output)
        self.min_utility = min_utility
        self.population_size = population_size
        self.generations = generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob

        self.population: list[Individual] = []
        self.hui_sets: HuiSet = set()
        self.transactions: list[Transaction] = []
        self.biggest_item: int = 0
        self.avg_len: int = 0
        self.valid_positions: list[int] = []
        self.p_max: float = 0.0
        self.p_min: float = 0.0
        self.total_time: float = 0.0
        self.total_memory: int = 0

    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------

    def load_transactions(self) -> None:
        """Load dataset, apply TWU pruning, and compute adaptive mutation bounds."""
        print("* Loading Transactions...")
        start = time.time()

        valid_items = calculate_twu(self.dataset_path, self.min_utility)
        self.transactions, self.biggest_item = load_transactions(self.dataset_path)

        self.valid_positions = sorted(item - 1 for item in valid_items if item <= self.biggest_item)
        self.avg_len = (
            sum(t.tran_bits.count() for t in self.transactions) // len(self.transactions) if self.transactions else 0
        )

        m, n = len(self.transactions), len(self.valid_positions)
        if m > 0 and n > 0:
            self.p_max = 1 / min(m, n)
            self.p_min = 1 / max(m, n)

        self._log_time(start, "Loaded Successful")

    # -------------------------------------------------------------------------
    # Fitness & HUI tracking
    # -------------------------------------------------------------------------

    def _fitness(self, bits: bitarray) -> int:
        return calculate_fitness(self.transactions, bits)

    def _track_hui(self, individual: Individual) -> None:
        if individual.fitness >= self.min_utility:
            self.hui_sets.add((tuple(individual.bits), individual.fitness))

    def _exists(self, bits: bitarray) -> bool:
        return any(ind.bits == bits for ind in self.population)

    # -------------------------------------------------------------------------
    # Population generation
    # -------------------------------------------------------------------------

    def generate_initial_population(self) -> None:
        """Generate the initial population using only TWU-valid item positions."""
        print("* Generating Initial Population...")
        start = time.time()

        max_bits = max(1, min(self.avg_len, len(self.valid_positions)))
        while len(self.population) < self.population_size:
            bits = bitarray(self.biggest_item)
            bits.setall(0)
            for pos in random.sample(self.valid_positions, random.randint(1, max_bits)):
                bits[pos] = 1

            individual = Individual(bits=bits, fitness=self._fitness(bits))
            if not self._exists(bits):
                self._track_hui(individual)
                self.population.append(individual)

        self.population.sort(key=lambda x: x.fitness, reverse=True)
        self._log_time(start, "Generated Population")

    # -------------------------------------------------------------------------
    # Selection
    # -------------------------------------------------------------------------

    def _tournament_selection(self) -> Individual:
        k = random.randint(1, len(self.population))
        return max(random.sample(self.population, k), key=lambda x: x.fitness)

    def _roulette_wheel_selection(self) -> Individual:
        total = sum(ind.fitness for ind in self.population)
        if total == 0:
            return random.choice(self.population)
        weights = [ind.fitness / total for ind in self.population]
        return self.population[random.choices(range(len(self.population)), weights=weights, k=1)[0]]

    def _rank_selection(self) -> Individual:
        ranked = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        n = len(ranked)
        total_ranks = n * (n + 1) // 2
        weights = [(n - rank + 1) / total_ranks for rank in range(1, n + 1)]
        return ranked[random.choices(range(n), weights=weights, k=1)[0]]

    def _select_parents(self) -> tuple[Individual, Individual]:
        selectors: list[Callable[[], Individual]] = [
            self._tournament_selection,
            self._roulette_wheel_selection,
            self._rank_selection,
        ]
        parent_1 = random.choice(selectors)()
        parent_2 = parent_1
        while parent_2 is parent_1:
            parent_2 = random.choice(selectors)()
        return parent_1, parent_2

    # -------------------------------------------------------------------------
    # Crossover
    # -------------------------------------------------------------------------

    def _single_point_crossover(self, p1: Individual, p2: Individual) -> tuple[Individual, Individual]:
        s = random.randint(1, self.biggest_item // 2)
        e = random.randint(s + 1, self.biggest_item - 1)
        b1 = p1.bits[:s] + p2.bits[s:e] + p1.bits[e:]
        b2 = p2.bits[:s] + p1.bits[s:e] + p2.bits[e:]
        return Individual(b1, self._fitness(b1)), Individual(b2, self._fitness(b2))

    def _multi_point_crossover(self, p1: Individual, p2: Individual) -> tuple[Individual, Individual]:
        points = sorted(random.sample(range(self.biggest_item), self.biggest_item // 2))
        b1, b2 = p1.bits[: points[0]], p2.bits[: points[0]]
        for i in range(len(points) - 1):
            seg = slice(points[i], points[i + 1])
            if i % 2 == 0:
                b1 += p2.bits[seg]
                b2 += p1.bits[seg]
            else:
                b1 += p1.bits[seg]
                b2 += p2.bits[seg]
        # Continue the alternating pattern: even segment index → swap (b1=p2), odd → same (b1=p1)
        # Tail segment index = len(points)-1; it's even when len(points) is odd
        if len(points) % 2 == 0:
            b1 += p1.bits[points[-1] :]
            b2 += p2.bits[points[-1] :]
        else:
            b1 += p2.bits[points[-1] :]
            b2 += p1.bits[points[-1] :]
        return Individual(b1, self._fitness(b1)), Individual(b2, self._fitness(b2))

    def _uniform_crossover(self, p1: Individual, p2: Individual) -> tuple[Individual, Individual]:
        b1, b2 = bitarray(self.biggest_item), bitarray(self.biggest_item)
        for i in range(self.biggest_item):
            if random.random() < 0.5:
                b1[i], b2[i] = p1.bits[i], p2.bits[i]
            else:
                b1[i], b2[i] = p2.bits[i], p1.bits[i]
        return Individual(b1, self._fitness(b1)), Individual(b2, self._fitness(b2))

    def _crossover(self, p1: Individual, p2: Individual) -> tuple[Individual, Individual]:
        method: CrossoverFn = random.choice([
            self._single_point_crossover,
            self._multi_point_crossover,
            self._uniform_crossover,
        ])
        return method(p1, p2)

    # -------------------------------------------------------------------------
    # Mutation
    # -------------------------------------------------------------------------

    def _mutate(self, individual: Individual) -> Individual:
        """Return a new individual with one TWU-valid bit flipped."""
        if not self.valid_positions:
            return individual
        new_bits = individual.bits.copy()
        pos = random.choice(self.valid_positions)
        new_bits[pos] = not new_bits[pos]
        return Individual(bits=new_bits, fitness=self._fitness(new_bits))

    def _ranked_mutation(self, population: list[Individual], generation: int) -> None:
        """Adaptive mutation: rate decreases over generations, proportional to rank.
        Lower-fitness individuals (higher rank index) mutate more often.
        """
        if not self.valid_positions or self.p_max == 0:
            return
        n = len(population)
        for rank, individual in enumerate(population, 1):
            pm = (self.p_max - (self.p_max - self.p_min) * generation / self.generations) * rank / n
            if random.random() < pm:
                individual.bits[random.choice(self.valid_positions)] ^= True
                individual.fitness = self._fitness(individual.bits)
                self._track_hui(individual)

    # -------------------------------------------------------------------------
    # Evolution
    # -------------------------------------------------------------------------

    def _handle_crossover(self, p1: Individual, p2: Individual, pool: list[Individual]) -> None:
        child_1, child_2 = self._crossover(p1, p2)
        for child in (child_1, child_2):
            if not self._exists(child.bits):
                self._track_hui(child)
                pool.append(child)

    def _handle_mutation(self, pool: list[Individual]) -> None:
        for _ in range(len(pool) // 8):
            mutated = self._mutate(random.choice(pool))
            if not self._exists(mutated.bits):
                self._track_hui(mutated)
                pool.append(mutated)

    def _generate_offspring(self, pool: list[Individual]) -> None:
        while len(pool) < self.population_size:
            p1, p2 = self._select_parents()
            if random.random() < self.crossover_prob:
                self._handle_crossover(p1, p2, pool)
            if random.random() < self.mutation_prob:
                self._handle_mutation(pool)

    def evolve_population(self) -> None:
        """Evolve the population over all generations."""
        print("* Evolving Population...")
        for generation in range(self.generations):
            start = time.time()
            print(f"\t> Completed Generation {generation + 1} in:", end=" ")

            pool = self.population[: self.population_size // 2]
            self._generate_offspring(pool)
            self._ranked_mutation(pool, generation)

            pool.sort(key=lambda x: x.fitness, reverse=True)
            self.population = pool[: self.population_size]

            self._log_time(start)

    # -------------------------------------------------------------------------
    # Reporting & output
    # -------------------------------------------------------------------------

    def report_performance(self) -> None:
        self.total_memory = psutil.Process().memory_info().rss
        print(f"* Results for: {self.dataset_path.stem}")
        print(f"\t> High-utility itemsets found: {len(self.hui_sets)}")
        print(f"\t> Total time:   ~ {self.total_time:.3f} s")
        print(f"\t> Total memory: ~ {self.total_memory / 1024 / 1024:.3f} MB")

    def save_results(self) -> None:
        with self.output.open("w") as f:
            f.write(f"Genetic Algorithm Result For Database: {self.dataset_path.stem}\n")
            f.write(f"Total time: {self.total_time:.3f} s\n")
            f.write(f"Total memory used: ~ {self.total_memory / 1024 / 1024:.3f} MB\n")
            f.write(f"Total High-utility item-sets found: {len(self.hui_sets)}\n\n")
            for bits, fitness in self.hui_sets:
                items_str = " ".join(str(i + 1) for i, b in enumerate(bits) if b)
                f.write(f"{items_str} #UTIL: {fitness}\n")

    def execute(self) -> None:
        self.load_transactions()
        self.generate_initial_population()
        self.evolve_population()
        self.report_performance()
        self.save_results()

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _log_time(self, start: float, label: str = "") -> None:
        elapsed = time.time() - start
        self.total_time += elapsed
        suffix = f"~ {elapsed:.3f} s"
        print(suffix if not label else f"\t> {label}: {suffix}")

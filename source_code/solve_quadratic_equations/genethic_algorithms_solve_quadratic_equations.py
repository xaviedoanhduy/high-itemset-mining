import random


POPULATION_SIZE = 100
CHROMOSOME_LENGTH = 8
MUTATION_RATE = 0.05
GENERATIONS = 100


def decode_chromosome(chromosome):
    x = int("".join(map(str, chromosome)), 2)
    return x


def fitness(x, a, b, c):
    return abs(a * x**2 + b * x + c)


def generate_population(population_size, chromosome_length):
    """
    Khởi tạo danh sách các bit giá trị ngẫu nhiên 0 và 1 
    với kích thước là chromosome_length
    """
    population = [
        [random.randint(0, 1) for _ in range(chromosome_length)]
        for _ in range(population_size)
    ]

    return population


def selection(population, a, b, c):
    population_with_fitness = [
        (chromosome, fitness(decode_chromosome(chromosome), a, b, c))
        for chromosome in population
    ]

    sorted_population = sorted(
        population_with_fitness,
        key=lambda x: x[1]
    )

    return [
        chromosome for chromosome, _ in sorted_population[:len(population) // 2]
    ]


def crossover(parent_1, parent_2):
    crossover_point = random.randint(1, len(parent_1) - 1)
    child_1 = parent_1[:crossover_point] + parent_2[crossover_point:]
    child_2 = parent_2[:crossover_point] + parent_1[crossover_point:]
    return child_1, child_2


def mutation(chromosome, mutation_rate):
    new_child = [
        bit if random.random() > mutation_rate else 1 - bit
        for bit in chromosome
    ]
    return new_child


def genetic_algorithm(
    population_size, chromosome_length, 
    generations, mutation_rate, a, b, c
):
    populations = generate_population(
        population_size,
        chromosome_length
    )

    for generation in range(generations):
        populations_with_fitness = selection(populations, a, b, c)

        new_population = []

        for _ in range(population_size):
            parent_1, parent_2 = random.sample(populations_with_fitness, 2)

            child_1, child_2 = crossover(parent_1, parent_2)

            new_population.append(mutation(child_1, mutation_rate))
            new_population.append(mutation(child_2, mutation_rate))

        populations = new_population

    best_chromosome = min(
        populations,
        key=lambda chromosome: fitness(decode_chromosome(chromosome), a, b, c)
    )

    return decode_chromosome(best_chromosome)


if __name__ == "__main__":
    a = 1
    b = -2
    c = 1

    solution = genetic_algorithm(
        POPULATION_SIZE,
        CHROMOSOME_LENGTH,
        GENERATIONS,
        MUTATION_RATE,
        a,
        b,
        c
    )

    print(f"x = {solution}")

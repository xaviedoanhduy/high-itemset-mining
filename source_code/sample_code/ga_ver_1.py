import random

def generate_random_population(population_size, chromosome_length):
    return [
        [random.randint(0, 1) for _ in range(chromosome_length)]
        for _ in range(population_size)
    ]

def fitness(chromosome, window_size, sequence):
    count = 0
    for i in range(len(sequence) - window_size + 1):
        window = sequence[i:i + window_size]
        if all(
            chromosome[j] == 1 and window[j] == 1
            for j in range(len(chromosome))
        ):
            count += 1
    return count

def selection(population, window_size, sequence):
    population_with_fitness = [
        (chromosome, fitness(chromosome, window_size, sequence))
        for chromosome in population
    ]
    population_with_fitness.sort(key=lambda x: x[1], reverse=True)
    return [
        chromosome for chromosome, _ in population_with_fitness[:len(population) // 2]
    ]

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutation(chromosome, mutation_rate):
    return [bit if random.random() > mutation_rate else 1 - bit for bit in chromosome]

def genetic_algorithm(
    population_size,
    chromosome_length,
    generations,
    window_size,
    sequence,
    mutation_rate,
):
    population = generate_random_population(population_size, chromosome_length)

    for _ in range(generations):
        population = selection(population, window_size, sequence)

        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population[:population_size]

    return population

if __name__ == "__main__":
    sequence = [0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
    window_size = 4
    population_size = 10
    chromosome_length = window_size
    generations = 100
    mutation_rate = 0.01

    result = genetic_algorithm(
                    population_size, chromosome_length,
                    generations, window_size,
                    sequence, mutation_rate
                )

    print("Các tập phổ biến:")
    for chromosome in result:
        print([sequence[i] for i in range(len(sequence))])

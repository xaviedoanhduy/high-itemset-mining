from ga import GeneticAlgorithm

if __name__ == '__main__':
    dataset_path = 'db_utility.txt'
    generations = 10
    population_size = 50
    crossover_prob = 0.8
    mutation_prob = 0.2
    min_utility = 10
    output = "output.txt"

    ga = GeneticAlgorithm(dataset_path, min_utility, population_size, generations, crossover_prob, mutation_prob, output)
    ga.execute()

class ChromosomeNode:
    def __init__(self, length=0):
        self.chromosome = [0] * length  # the chromosome
        self.fitness = 0    # fitness value of chromosome
        self.r_fitness = 0.0


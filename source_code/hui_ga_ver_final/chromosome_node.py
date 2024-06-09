from bitarray import bitarray


class ChromosomeNode:
    def __init__(self, bits, fitness=0):
        """
        Chromosome Node of Population
        :param length: Length of the transaction bits
        """
        self.bits = bits
        self.fitness = fitness    # fitness value of chromosome


class HUI:
    def __init__(self, itemset, fitness):
        self.itemset = itemset
        self.fitness = fitness

    def __hash__(self):
        return hash(self.itemset)

    def __eq__(self, other):
        return self.itemset == other.itemset

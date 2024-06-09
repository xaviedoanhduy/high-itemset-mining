class Itemset:
    def __init__(self, itemset, utility=0, support=1):
        """
        :param itemset: int[]
        :param utility: long
        :param support: int
        """
        self.utility = utility
        self.itemset = itemset
        self.support = support

    def __str__(self):
        return f"{self.itemset} utility: {self.utility}"

    @property
    def get_itemset(self):
        return self.itemset or []

    @property
    def get_utility(self):
        return self.utility or 0

    @property
    def get_support(self):
        return self.support or 1



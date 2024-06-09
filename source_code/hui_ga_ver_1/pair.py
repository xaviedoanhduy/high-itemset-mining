
class Pair:
    """This class represent an item and its utility in a transaction"""
    def __init__(self, item=0, utility=0):
        self.item = item
        self.utility = utility

    def __str__(self):
        return f"{self.item}: {self.utility}"

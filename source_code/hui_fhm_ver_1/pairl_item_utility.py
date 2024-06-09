class PairItemUtility:
    def __init__(self, item=0, utility=0):
        """

        :param item: the item (Integer)
        :param utility: (Integer)
        :return:
        """
        self.item = item
        self.utility = utility

    def __str__(self):
        return f"[{self.item}: {self.utility}]"

    @property
    def get_item(self):
        return self.item

    @property
    def get_utility(self):
        return self.utility

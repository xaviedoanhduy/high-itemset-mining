class UtilityList:
    def __init__(self, item, sum_item_utility=0, sum_rutils=0, elements=None):
        """
        :param item: int
        :param elements: List
        :param sum_item_utility: int
        :param sum_rutils: int
        """

        if elements is None:
            elements = []
        self.item = item
        self.sum_item_utility = sum_item_utility
        self.sum_rutils = sum_rutils
        self.elements = elements

    @property
    def get_item(self):
        return self.item or None

    @property
    def get_sum_item_utility(self):
        return self.sum_item_utility or 0

    @property
    def get_sum_rutils(self):
        return self.sum_rutils or 0

    @property
    def get_elements(self):
        return self.elements or []

    @property
    def get_support(self):
        return len(self.elements)

    def __str__(self):
        elements = []
        for element in self.get_elements:
            elements.append(
                f"[tid = {element.tid}, iutils = {element.iutils}, rutils = {element.rutils}]"
            )

        return f"Item: {self.get_item},\nSum Utility: {self.get_sum_item_utility},\n" \
            f"Sum Rutils: {self.get_sum_rutils}, \nElements: {elements}\n" \
            f"--------------------------------------------------------------------------------------"

    def add_element(self, element):
        """
        To add an element to this utility list and update the sums at the same time.
        :param element:
        :return:
        """
        self.sum_item_utility += element.iutils
        self.sum_rutils += element.rutils
        self.elements.append(element)


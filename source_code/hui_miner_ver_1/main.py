class Element:
    def __init__(self, tid, iutil, rutil):
        self.tid = tid  # transaction id
        self.iutil = iutil  # item utility
        self.rutil = rutil  # remaining utility


class UtilityList:
    def __init__(self, item):
        self.item = item
        self.elements = []
        self.sum_iutil = 0  # sum of item utilities
        self.sum_rutil = 0  # sum of remaining utilities

    def add_element(self, element):
        self.elements.append(element)
        self.sum_iutil += element.iutil
        self.sum_rutil += element.rutil


def construct_utility_list(transactions, item_to_twu, item):
    ul = UtilityList(item)
    for tid, transaction in enumerate(transactions):
        if item in transaction:
            iutil = transaction[item]
            rutil = sum(transaction[itm] for itm in transaction if itm > item)
            ul.add_element(Element(tid, iutil, rutil))
    return ul


def hui_miner(prefix, ul, min_util, transactions, item_to_twu):
    if ul.sum_iutil >= min_util:
        str_hui = " ".join(str(item) for item in prefix)
        print(f"{str_hui} #HUI: {ul.sum_iutil}")

    for item in sorted(item_to_twu.keys()):
        if item > prefix[-1]:
            new_ul = construct_utility_list(transactions, item_to_twu, item)
            hui_miner(prefix + [item], new_ul, min_util, transactions, item_to_twu)


def run_algorithm(dataset_path, min_util):
    transactions = []
    with open(dataset_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith(("#", "%", "@")):
                split = line.split(":")
                items = [int(item) for item in split[0].split()]
                utility_values = [int(value) for value in split[2].split()]
                transaction = {}
                for i, item in enumerate(items):
                    transaction[item] = utility_values[i]
                    transactions.append(transaction)

    item_to_twu = {}
    for transaction in transactions:
        for item, utility in transaction.items():
            if item in item_to_twu:
                item_to_twu[item] += sum(transaction.values())
            else:
                item_to_twu[item] = sum(transaction.values())

    for item in item_to_twu.keys():
        ul = construct_utility_list(transactions, item_to_twu, item)
        hui_miner([item], ul, min_util, transactions, item_to_twu)


if __name__ == "__main__":
    run_algorithm("db_utility.txt", 40)

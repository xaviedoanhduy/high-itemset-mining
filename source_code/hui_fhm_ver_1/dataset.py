
class Dataset:
    def __init__(self, dataset_path, support=1):
        self.transactions = []
        self.max_item = 0
        self.max_num = 0
        self.support = support

        with open(dataset_path) as f:
            for line in f:
                if line.strip() in ["", "#", "%", "@"]:
                    continue

                t = self._create_transaction(line)
                if len(t) > self.max_item:
                    self.max_item = len(t)

                self.transactions.append(t)

    def _create_transaction(self, line):
        items_string = line.split()

        items = []
        for item_string in items_string:
            try:
                n = int(item_string)
                if n > self.max_num:
                    self.max_num = n

                items.append(n)
                
            except ValueError:
                pass

        return items

    @property
    def get_transactions(self):
        return self.transactions

    @property
    def get_max_item(self):
        return self.max_item

    @property
    def get_max_num(self):
        return self.max_num

    @property
    def get_support(self):
        return self.support
    
    def count_support_of_candidate(self, candidate):
        count = 0
        for transaction in self.get_transactions:
            if set(candidate).issubset(set(transaction)):
                count += 1
                
        return count

    def generate_candidates(self):
        frequent_item_sets = []

        all_items = [item for sublist in self.get_transactions for item in sublist]
        candidates = [[item] for item in set(all_items)]

        for candidate in candidates:
            support = self.count_support_of_candidate(candidate)
            if support >= self.get_support:
                frequent_item_sets.append(candidate[0])

        return frequent_item_sets


if __name__ == "__main__":
    print("Done..!")

    data_path = "../ga_frequent_patterns/datasets/test_dataset.txt"
    support_count = 3

    database = Dataset(data_path, support_count)

    data = database.get_transactions
    individual_size = database.get_max_item
    max_num = database.get_max_num

    print("data: ", data)

    candidates = database.generate_candidates()
    print("candidates:", candidates)

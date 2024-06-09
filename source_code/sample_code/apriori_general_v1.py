def load_data(file_path):
    data = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            string_list = line.strip().split(', ')
            data.append([int(num) for num in string_list])
    return data

    # return [
    #     [1, 7, 8],
    #     [1, 2, 6, 7, 8],
    #     [1, 2, 6, 7],
    #     [1, 7, 8],
    #     [3, 4, 5, 6, 8],
    #     [1, 4, 5]
    # ]
    # return [
    #     ['a', 'b', 'e', 'g'],
    #     ['a', 'c', 'd', 'f'],
    #     ['a', 'b', 'g'],
    #     ['b', 'c', 'd', 'e', 'g'],
    #     ['a', 'c', 'e', 'f'] 
    # ]
    
def create_candidates(prev_candidates, k):
    candidates = []
    n = len(prev_candidates)

    for i in range(n):
        for j in range(i + 1, n):
            # Kết hợp hai tập hợp nếu các phần tử đầu tiên (k-2) của chúng giống nhau
            if prev_candidates[i][:k-2] == prev_candidates[j][:k-2]:
                candidate = list(set(prev_candidates[i]) | set(prev_candidates[j]))
                candidate.sort()
                candidates.append(candidate)

    return candidates

def support_count(dataset, candidate):
    count = 0
    for data in dataset:
        if set(candidate).issubset(set(data)):
            count += 1
    return count/len(dataset)

def apriori(dataset, min_support):
    candidates = []
    frequent_itemsets = []
    k = 1

    while True:
        if k == 1:
            candidates = [[item] for item in set(item for sublist in dataset for item in sublist)]
        else:
            candidates = create_candidates(candidates, k)
        print('C',k,'= ',candidates)
        print('**********')
        frequent_candidates = []
        for candidate in candidates:
            support = support_count(dataset, candidate)
            if support >= min_support:
                frequent_itemsets.append((candidate, round(support, 2)))
                frequent_candidates.append(candidate)

        if not frequent_candidates:
            break
        print('L',k,'= ',frequent_candidates)
        print('****************')
        candidates = frequent_candidates
        k += 1

    return frequent_itemsets

#=====================================================
from itertools import chain, combinations

def powerset(s):
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))

def generate_frequent_strong_rules(frequent_itemsets, min_confidence, dataset):
    strong_rules = []# set()

    for itemset, _ in frequent_itemsets:
        subsets = powerset(itemset)
        print(subsets)
        for antecedent in subsets:
            consequent = set(itemset) - set(antecedent)
            if not consequent: continue
            confidence = calculate_confidence(itemset, antecedent, dataset)

            if confidence >= min_confidence:
                strong_rules.append((antecedent,consequent))#((frozenset(antecedent), frozenset(consequent)))

    return strong_rules

def calculate_confidence(itemset, antecedent, dataset):
    # Assume some function to calculate support for itemset, antecedent, and consequent
    support_itemset = support_count(dataset, itemset )
    support_antecedent = support_count(dataset, antecedent)
    return support_itemset / support_antecedent

if __name__ == "__main__":
    # dataset = [
    #     [1, 7, 8],
    #     [1, 2, 6, 7, 8],
    #     [1, 2, 6, 7],
    #     [1, 7, 8],
    #     [3, 4, 5, 6, 8],
    #     [1, 4, 5]
    # ]
    dataset = load_data("./ga_frequent_patterns/datasets/test_dataset.txt")
    min_support = 0.3
    frequent_itemsets = apriori(dataset, min_support)

    print("Frequent itemsets with minimum support count of", min_support)
    for itemset, support in frequent_itemsets:
        print(itemset, ":", support)

    
    min_confidence = 0.6
    strong_rules= generate_frequent_strong_rules(frequent_itemsets, min_confidence, dataset)
    for antecedent, consequent in strong_rules:
        print(antecedent, "->", consequent)


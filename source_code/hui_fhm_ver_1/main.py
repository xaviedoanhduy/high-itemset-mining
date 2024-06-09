from collections import defaultdict
from element import Element
from utility_list import UtilityList
from pairl_item_utility import PairItemUtility
import time
import psutil


def find_element_with_tid(ulist, t_id):
    elements = ulist.elements
    first = 0
    last = len(elements) - 1

    while first <= last:
        middle = (first + last) // 2

        if elements[middle].t_id < t_id:
            first = middle + 1

        elif elements[middle].t_id > t_id:
            last = middle - 1

        else:
            return elements[middle]

    return None


class HUIMinerAlgo:

    def __init__(self, min_utility=10):
        self.min_utility = min_utility
        self.total_time = 0.0
        self.max_memory = 0.0
        self.hui_count = 0
        self.candidate_count = 0
        self.map_item_to_twu = {}
        self.writer = None
        self.map_fmap = defaultdict(lambda: defaultdict(int))
        self.ENABLE_LA_PRUNE = True

    def run_algorithm(self, input_file, output_file="output.txt"):
        start_timestamp = time.time()

        process_start = psutil.Process()
        memory_start_info = process_start.memory_info()
        cur_memory_start = memory_start_info.rss / 1024 / 1024

        self.writer = open(output_file, 'w')

        # Scan the database to calculate the TWU of each item
        try:
            with open(input_file, "r") as file:
                for line in file:
                    if line.strip() and not line.startswith(("#", "%", "@")):
                        split = line.split(':')
                        items = split[0].split()
                        transaction_utility = int(split[1])
                        for item in items:
                            item_int = int(item)
                            self.map_item_to_twu[item_int] = self.map_item_to_twu.get(item_int, 0) + transaction_utility
        except Exception as e:
            print(f"Error reading input file: {e}")

        # Create a list to store the utility list of items with TWU >= min_utility
        utility_lists = []
        map_item_to_utility_list = {}
        for item, twu in self.map_item_to_twu.items():
            if twu >= self.min_utility:
                utility_list = UtilityList(item)
                map_item_to_utility_list[item] = utility_list
                utility_lists.append(utility_list)

        # Sort the list of high TWU items in ascending order
        utility_lists.sort(key=lambda x: x.item)

        # Second database pass to construct the utility lists of 1-itemsets with TWU >= min_utility
        try:
            with open(input_file, "r") as file:
                tid = 0
                for line in file:
                    if line.strip() and not line.startswith(("#", "%", "@")):
                        split = line.split(":")
                        items = [int(item) for item in split[0].split()]
                        utility_values = [int(value) for value in split[2].split()]

                        remaining_utility = 0
                        new_twu = 0
                        revised_transaction = []
                        for item, utility in zip(items, utility_values):
                            if self.map_item_to_twu.get(item, 0) >= self.min_utility:
                                pair = PairItemUtility()
                                pair.item = item
                                pair.utility = utility
                                revised_transaction.append(pair)
                                remaining_utility += utility
                                new_twu += utility

                        revised_transaction.sort(key=lambda x: x.item)

                        for i in range(len(revised_transaction)):
                            pair = revised_transaction[i]
                            remaining_utility -= pair.utility

                            utility_list_of_item = map_item_to_utility_list[pair.item]
                            element = Element(tid, pair.utility, remaining_utility)
                            utility_list_of_item.add_element(element)

                            for j in range(i + 1, len(revised_transaction)):
                                pair_after = revised_transaction[j]
                                self.map_fmap[pair.item][pair_after.item] += new_twu

                        tid += 1
        except Exception as e:
            print(f"Error reading input file: {e}")

        self._fhm([], 0, None, utility_lists)

        self.writer.close()
        end_timestamp = time.time()

        process_end = psutil.Process()
        memory_end_info = process_end.memory_info()
        cur_memory_end = memory_end_info.rss / 1024 / 1024

        self.total_time = end_timestamp - start_timestamp
        self.max_memory = cur_memory_end - cur_memory_start

    def _fhm(self, prefix, prefix_length, p_ul, uls):
        for i in range(len(uls)):
            x = uls[i]

            if x.sum_item_utility >= self.min_utility:
                self._write_out(prefix, prefix_length, x.item, x.sum_item_utility)

            if x.sum_item_utility + x.sum_rutils >= self.min_utility:
                ex_uls = []
                for j in range(i + 1, len(uls)):
                    y = uls[j]
                    map_twu_f = self.map_fmap[x.item]
                    twu_f = map_twu_f.get(y.item, 0)
                    if twu_f >= self.min_utility:
                        self.candidate_count += 1
                        temp = self.construct(p_ul, x, y)
                        if temp is not None:
                            ex_uls.append(temp)

                new_prefix = prefix + [x.item]
                self._fhm(new_prefix, prefix_length + 1, x, ex_uls)

    def construct(self, p, px, py):
        pxy_ul = UtilityList(py.item)
        total_utility = px.sum_item_utility + px.sum_rutils

        for ex in px.elements:
            ey = find_element_with_tid(py, ex.t_id)
            if ey is None:
                if self.ENABLE_LA_PRUNE:
                    total_utility -= (ex.iutils + ex.rutils)
                    if total_utility < self.min_utility:
                        return None
                continue

            if p is None:
                exy = Element(ex.t_id, ex.iutils + ey.iutils, ey.rutils)
                pxy_ul.add_element(exy)
            else:
                e = find_element_with_tid(p, ex.t_id)
                if e is not None:
                    exy = Element(ex.t_id, ex.iutils + ey.iutils - e.iutils, ey.rutils)
                    pxy_ul.add_element(exy)

        return pxy_ul

    def _write_out(self, prefix, prefix_length, item, utility):
        self.hui_count += 1
        output_str = " ".join(map(str, prefix)) + f"{item} #UTIL:{utility}"
        self.writer.write(output_str + "\n")

    def print_result(self):
        print("============= FHM ALGORITHM - SPMF 0.97e - STATS =============")
        print(f"> High-utility itemsets count: {self.hui_count}")
        print(f"> Candidate count: {self.candidate_count}")
        print(f"> Total time: ~ {self.total_time:.3f} s")
        print(f"> Max memory (mb): {self.max_memory} mb")


if __name__ == "__main__":
    min_utility = 500
    input_file = "dataset/chess.txt"
    output_file = "output.txt"
    print("****DOING****")
    algo = HUIMinerAlgo(min_utility)
    algo.run_algorithm(input_file, output_file)
    algo.print_result()
    print("****Done****")

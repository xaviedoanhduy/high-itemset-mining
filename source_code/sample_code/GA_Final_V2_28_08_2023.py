import psutil
import random
from Dataset import Dataset
import time
from CreateCandidate import candidate

# Số lượng thế hệ
generations = 20
# Xác suất lai ghép
crossover_probability = 0.8
# Xác suất đột biến
mutation_probability = 0.2


# Hàm tính mức độ phổ biến của ỨNG VIÊN
def exists(transaction, candidate, item_candidate):
    i = 0
    n = len(candidate)
    m = len(transaction)
    while i < n and candidate[i] == 0:
        i += 1  # tìm nhiễm sắc thể đầu tiên = 1
    if i == n:
        return False  # nếu không tìm thấy
    j = 0  # duyệt từ đầu transaction
    while i < n:  # duyệt trên candidate
        ##print(i)
        while j < m and transaction[j] != item_candidate[i]:
            j += 1
            # trong khi chưa có xuất hiện ở transaction
        ##print(j)
        if j == m:
            return False  # nếu không tìm thấy
        i += 1
        j += 1  # qua phần tử kế
        while i < n and candidate[i] == 0:
            i += 1
    return True


def fitness_function(dataset, candidate, item_candidate):
    count = 0
    for data in dataset:
        ###print(data); ##print(candidate); ##print(item_candidate); input()
        if exists(data, candidate, item_candidate):
            count += 1
            ##print('có')
    ###print(count); #input()
    return count


# Hàm lai ghép hai cá thể để tạo ra con cái
def crossover(parent1, parent2):
    crossover_point1 = random.randint(1, len(parent1) // 2)
    crossover_point2 = random.randint(crossover_point1 + 1, len(parent1) - 1)
    child1 = (
        parent1[:crossover_point1]
        + parent2[crossover_point1:crossover_point2]
        + parent1[crossover_point2:]
    )
    child2 = (
        parent2[:crossover_point1]
        + parent1[crossover_point1:crossover_point2]
        + parent2[crossover_point2:]
    )
    return child1, child2


# Hàm đột biến một cá thể
def mutate(individual, next_generation):
    mutation_point = random.randint(0, len(individual) - 1)
    individual[mutation_point] = (
        1 - individual[mutation_point]
    )  # Đổi giá trị 0 thành 1 hoặc 1 thành 0


# Chuyển từ transaction sang mảng bit
def converttoBit(individual, individual_size):
    BitArr = [0 for _ in range(individual_size)]
    for i in individual:
        BitArr[i - 1] = 1
    return BitArr


# Khởi tạo quần thể ban đầu
def KhoiTaoQuanThe(population_size, individual_size, dataset):
    datasetCopy = dataset.copy()
    population = []
    for _ in range(population_size):
        vt = random.randint(0, len(datasetCopy) - 1)
        individual = datasetCopy[vt]
        population.append(converttoBit(individual, individual_size))
        datasetCopy.remove(individual)
    return population


def convertbittotransaction(individual):
    transaction = []
    for i in range(len(individual)):
        if individual[i] == 1:
            transaction.append(i + 1)
    return transaction


def find_frequent_itemsets(population, dataset, support_count, item_candidate):
    fitness_scores = [
        fitness_function(dataset, individual, item_candidate)
        for individual in population
    ]
    frequent_itemsets = []
    for i in range(len(fitness_scores)):
        if fitness_scores[i] >= support_count:
            frequent_itemsets.append(
                (convertbittotransaction(population[i]), fitness_scores[i])
            )
    return frequent_itemsets


def Select(population, fitness_scores, support_count):
    selected = []
    for i in range(len(fitness_scores)):
        if fitness_scores[i] >= support_count:
            selected.append(population[i])
    return selected


def randomSelected(selected_parents):
    l = len(selected_parents)
    vt = random.randint(0, l // 2)
    parent1 = selected_parents[vt]
    vt = random.randint(l // 2 + 1, l - 1)
    parent2 = selected_parents[vt]
    return parent1, parent2


# kiểm tra trùng
def kiemTraTrung(child, next_generation):
    for individual in next_generation:
        if individual == child:
            return True
    return False


# Khởi tạo quần thể 0,1 ngẫu nhiên
def KhoiTaoBitArr(population_size, item_candidate):
    population = []
    i = 0
    maxNumber = len(item_candidate)
    while i < population_size:
        individual = []
        for _ in range(maxNumber):
            individual.append(random.randint(0, 1))
        if sum(individual) == 0:
            continue
        if kiemTraTrung(individual, population) == False:
            population.append(individual)
            i += 1
    return population


def TaoQuanThe_BitArr(population_size, item_candidate):
    population = []
    for i in range(1, population_size + 1):
        r = random.randint(1, item_candidate)
        binary_string = format(r, f"0{item_candidate}b")
        # print(binary_string)  # Output: '00001010'
        individual = []
        for c in binary_string:
            if c == "1":
                individual.append(1)
            else:
                individual.append(0)
        population.append(individual)
    return population


def PrintPopulation(population):
    for individual in population:
        print(convertbittotransaction(individual))


def CopyPopulation(population):
    new_population = []
    for individual in population:
        new_population.append(individual)
    return new_population


# Tiến hành tối ưu hóa HÀM GA
def GA(generations, population_size, dataset, support_count):
    item_candidate = candidate(dataset, support_count)
    population = TaoQuanThe_BitArr(population_size, len(item_candidate))
    for generation in range(generations):
        # Đánh giá mức độ phổ biến của các cá thể
        fitness_scores = [
            fitness_function(dataset, individual, item_candidate)
            for individual in population
        ]
        # Lựa chọn các cá thể tốt nhất để lai ghép và tái sinh
        selected_parents = Select(population, fitness_scores, support_count)
        # Lai ghép và tái sinh
        next_generation = CopyPopulation(selected_parents)
        while len(next_generation) < population_size:
            parent1, parent2 = randomSelected(selected_parents)
            if random.random() < crossover_probability:
                child1, child2 = crossover(parent1, parent2)
                next_generation.append(child1)
                next_generation.append(child2)
        # Đột biến ngẫu nhiên
        for individual in next_generation:
            if random.random() < mutation_probability:
                mutate(individual, next_generation)
        # Cập nhật quần thể mới
        population = CopyPopulation(next_generation)
    frequent_itemsets = find_frequent_itemsets(
        population, dataset, support_count, item_candidate
    )
    return frequent_itemsets


# Thuật toán chính
def GV_Slide(transactions, population_size, window_size, support_count, batch):
    all_frequent_itemsets = []
    for i in range(0, len(transactions) - window_size + 1, batch):
        window_data = transactions[i : i + window_size]
        frequent_itemsets = GA(generations, population_size, window_data, support_count)
        all_frequent_itemsets.extend(frequent_itemsets)
    return all_frequent_itemsets


# Đọc dữ liệu từ file
dataset = "D:\personal\graduation-essay\source_code\ga_frequent_patterns\datasets\mushroom.txt"
print("****LOADING****")
database = Dataset(dataset)
data = database.getTransactions()
individual_size = database.getMaxItem()
maxNum = database.getMaxNum()
# for r in data:
# print(r)
##print(maxNum)
window_size = 1000  # len(data) #1600
min_support = 0.06
confidence = 0.5
batch = 500
population_size = 100  # pow(2, len(item_candidate)-1) // 10
min_s = 0.25
support_count = min_s * window_size  # window_size * min_support * confidence
print("****DOING****")
# Lấy thông tin về bộ nhớ hiện tại
process = psutil.Process()
memory_info = process.memory_info()
cur_memory0 = memory_info.rss / 1024 / 1024  # Đổi từ byte sang megabyte
# print("Bộ nhớ hiện tại của chương trình: {:.2f} MB".format(cur_memory0))

s = time.time()
all_frequent_itemsets = GA(
    generations, population_size, dataset, support_count
)
e = time.time()
print("*********")
print("Min sup: ", min_s)
print("> Total Time ~", (e - s))

# Lấy thông tin về bộ nhớ hiện tại
process = psutil.Process()
memory_info = process.memory_info()
cur_memory1 = memory_info.rss / 1024 / 1024  # Đổi từ byte sang megabyte
# print("Bộ nhớ hiện tại của chương trình: {:.2f} MB".format(cur_memory1))
print("> Max memory (mb):", cur_memory1 - cur_memory0)

# print("Kết quả: ")
# print(all_frequent_itemsets)

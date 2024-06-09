import numpy as np
import random
from Dataset import Dataset
import time
from CreateCandidate import candidate
#from bitset import Bitset
from bitarray import bitarray
# Số lượng thế hệ
generations = 10
# Xác suất lai ghép
crossover_probability = 0.8
# Xác suất đột biến
mutation_probability = 0.1

def create_BitArrayFromInt(number, so_bit=5):  
    # Chuyển số nguyên thành chuỗi nhị phân và loại bỏ '0b' ở đầu
    binary_string = bin(number)[2:]
    #print(number)
    #print(binary_string)
    # Tạo một bitarray với số bit ban đầu là 5
    bit_array = bitarray(so_bit)
    bit_array.setall(0)
    #print(bit_array)
    
    for i in range(len(binary_string)):
        bit_array[i] = int(binary_string[i])

    # In ra bitarray
    #print(bit_array)
    return bit_array


def fitness_function(dataset, candidate):
    count = 0; #print('*****')
    for data in dataset:
        if candidate & data == candidate:
            count += 1
    return count


### Hàm lai ghép hai cá thể để tạo ra con cái
def crossover(parent1, parent2, num):
    crossover_point1 = random.randint(1, num//2)
    crossover_point2 = random.randint(crossover_point1+1, num - 1)
    child1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
    child2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[crossover_point2:]
    return child1, child2

# Hàm đột biến một cá thể
def mutate(individual,next_generation, mutation_rate = 0.1):
    if random.random() < mutation_rate:
        mutation_point = random.randint(0, len(individual) - 1)
        individual[mutation_point] = 1 - individual[mutation_point]  # Đổi giá trị 0 thành 1 hoặc 1 thành 0
    return individual
    #if kiemTraTrung(individual, next_generation):
    #    individual[mutation_point] = 1 - individual[mutation_point]

def convertbittotransaction(individual):
    transaction=[]
    for i in range(len(individual)):
        if individual[i]==1:
            transaction.append(i+1)
    return transaction 

def find_frequent_itemsets(population, dataset, support_count,item_candidate):
    fitness_scores = [fitness_function(dataset, individual) for individual in population]
    print(fitness_scores)
    frequent_itemsets=[]
    for i in range(len(fitness_scores)):
        if  fitness_scores[i]>=support_count:
            frequent_itemsets.append((convertbittotransaction(population[i]),fitness_scores[i]))         
    return frequent_itemsets

def Select(population, fitness_scores, support_count ):
    new_population = []
    selected = []
    for i in range(len(fitness_scores)):
        if  fitness_scores[i]>=support_count:
            selected.append(population[i])
            new_population.append(population[i])
    return selected, new_population

def randomSelected(selected_parents):
    l = len(selected_parents)
    print(l)
    vt = random.randint(0, l//2)
    print(vt)
    parent1 = selected_parents[vt]
    vt = random.randint(l//2+1, l-1)
    parent2 = selected_parents[vt]
    return parent1,parent2

def InitArr(maxNum):
    n = pow(2, maxNum)-1
    print(n)
    Arr = []
    for i in range(n):
        Arr.append(i)
    return Arr

def InitPopulation_BitArray(population_size,maxNum):
    population = []
    #Arr = InitArr(maxNum)
    for i in range(population_size):
        #j = random.randint(0,len(Arr)-1)
        #bit_set = create_BitArrayFromInt(Arr[j]+1,maxNum ) #Bitset(Arr[j]+1, maxNum)
        #print('pop: ',bit_set)
        #population.append(bit_set)
        #del Arr[j]
        # Khởi tạo một mảng numpy ngẫu nhiên gồm các bit 0 và 1
        random_bitarray = np.random.randint(2, size=maxNum)
        # Chuyển đổi mảng numpy thành bitarray
        bit_array = bitarray(random_bitarray.tolist())
        population.append(bit_array)
    return population

def PrintPopulationBitset(population):
    for individual in population:
        print('indi: ',individual)
    

def CopyPopulation(population):
    new_population = []
    for individual in population:
        new_population.append(individual)
    return new_population

#kiểm tra trùng
def kiemTraTrung(child, next_generation):
    for individual in next_generation:
        if individual == child:
            return True
    return False

# Tiến hành tối ưu hóa HÀM GA
def GA(generations, dataset, maxNum,min_support):
    item_candidate = candidate(dataset, window_size, min_support)
    population_size = 100 #(pow(2, maxNum)-1)
    population = InitPopulation_BitArray(population_size, maxNum)
    print('*** Đã tạo xong quần thể ***')
    PrintPopulationBitset(population)
    
    support_count = window_size * min_support
    print('Support count: ',support_count)
    for _ in range(generations):
        # Đánh giá mức độ phổ biến của các cá thể
        fitness_scores = []
        for individual in population:
            fitness_score = fitness_function(dataset, individual)
            fitness_scores.append(fitness_score)
        print(fitness_scores);
        # Lựa chọn các cá thể tốt nhất để lai ghép và tái sinh
        selected_parents, next_generation = Select(population, fitness_scores, support_count )
        print('****Cha mẹ được chọn****')
        PrintPopulationBitset(selected_parents); print('********')
        
        # Lai ghép và tái sinh
        #print('****Thế hệ kế****')
        #PrintPopulationBitset(next_generation); print('********')
        
        while len(next_generation) < population_size:
            parent1, parent2 = randomSelected(selected_parents)
            if random.random() < crossover_probability:
                child1, child2 = crossover(parent1, parent2,maxNum)
                #if sum(child1)>0 and kiemTraTrung(child1, next_generation) == False:
                next_generation.append(child1)
                next_generation.append(child2)
            else:
                mutate_candidate=mutate(parent1, next_generation)
                next_generation.append(mutate_candidate)
                
        # Cập nhật quần thể mới
        population = CopyPopulation(next_generation)
        #print('***Quần thể mới***')
        #printPopulation(population); #print('******')
    frequent_itemsets=find_frequent_itemsets(population, dataset, support_count,item_candidate)
    
    return frequent_itemsets 

#Thuật toán chính
def GV_Slide(transactions, window_size, min_support,batch,maxNum):
    all_frequent_itemsets = []
    #j=1
    for i in range(0,len(transactions) - window_size + 1,batch):
        window_data = transactions[i:i+window_size]
        frequent_itemsets =GA(generations,window_data,maxNum,min_support)
        '''print('Cửa sổ trượt lần %d: '%j);
        j+=1
        for itemset in frequent_itemsets:
            print(itemset)'''
        all_frequent_itemsets.extend(frequent_itemsets)
    return all_frequent_itemsets
    

#Đọc dữ liệu từ file
dataset = "chainstore_out.txt" #"mushroom.txt"#"contextHUIM_out.txt"# # #"contextHUIM_out.txt" #
print("****LOADING****")
database = Dataset(dataset)
data = database.getTransactions()
dataBit = database.getiItemsetNumArr()
individual_size = database.getMaxItem()
maxNum = database.getMaxNum()
print("Số lượng bit: ",maxNum)
for bit_array in dataBit:
##    # Số lượng bit cần thêm vào để đủ maxNum bit
    num_bits_to_add = maxNum - len(bit_array)
##    # Thêm số 0 vào bên phải của bitarray để đủ maxNum bit
    bit_array.extend([False] * num_bits_to_add)
    #print('data: ',bit_array); 
##    #print(format(i, f'0{maxNum}b'))

window_size = len(data)#6
min_support = 0.25
batch = 2
print("****DOING****")
s = time.time()
frequent_itemsets =GA(generations,dataBit,maxNum,min_support)
for i in frequent_itemsets: 
    print(i)
#GV_Slide(dataBit, window_size, min_support,batch, maxNum)
e = time.time()
print("*********")
print("> Total Time ~", (e - s))


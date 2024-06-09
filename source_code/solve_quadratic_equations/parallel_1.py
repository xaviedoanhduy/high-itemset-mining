from concurrent.futures import ThreadPoolExecutor

def independent_function(arg):
    # Công việc độc lập cần thực hiện
    result = arg * arg
    return result

if __name__ == "__main__":
    # Tạo một ThreadPoolExecutor với số lượng worker tương đương số lõi CPU
    with ThreadPoolExecutor() as executor:
        # Dữ liệu đầu vào
        input_data = [1, 2, 3, 4, 5]

        # Áp dụng hàm độc lập cho từng phần tử trong dữ liệu đầu vào
        results = list(executor.map(independent_function, input_data))

        # Kết quả
        print(results)

import concurrent.futures

x = 2

def calculate_square(number):
    """Hàm tính bình phương của một số."""
    return number *x

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    # Sử dụng ThreadPoolExecutor để tính toán song song
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map các số sang kết quả bình phương sử dụng nhiều luồng

        results = executor.map(calculate_square, numbers)

    # In kết quả
    for result in results:
        print(result)

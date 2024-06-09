import matplotlib.pyplot as plt

def format_value(value):
    """Chuyển đổi giá trị lớn hơn hoặc bằng 1000 thành dạng 'k'."""
    if value >= 1000:
        return f"{value}k"
    return str(value)

def plot_memory_usage(compare, huis):
    # Sắp xếp các giá trị của min_utility và compare theo thứ tự giảm dần của min_utility
    sorted_pairs = sorted(zip(huis, compare), reverse=True, key=lambda x: x[0])
    sorted_huis, sorted_compare = zip(*sorted_pairs)
    
    # Chuyển đổi các giá trị trong min_utility đã sắp xếp
    formatted_min_utility = [format_value(value) for value in sorted_huis]

    plt.figure(figsize=(8, 6))
    plt.plot(sorted_huis, sorted_compare, marker='o', color='green', linestyle='-')
    plt.title('Connect - GA')
    plt.ylabel('Run Time (s)')
    
    plt.xlabel('Minimum Utility Threshold')
    # plt.ylabel('Memories (mb)')
    # plt.title('Memory usage and HUIM')
    plt.grid(True)
    
    # Đặt lại nhãn cho trục x bằng các giá trị đã định dạng
    plt.xticks(ticks=sorted_huis, labels=formatted_min_utility)
    
    plt.show()

# Example data
times = [3.323, 3.407, 3.406, 3.524]  # Thời gian
min_utility = [16000, 15000, 14000, 13000]

compare = times
plot_memory_usage(compare, min_utility)

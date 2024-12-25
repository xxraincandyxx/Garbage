import random
import time
import matplotlib.pyplot as plt

# --- Sorting Algorithm Implementations ---

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

def quick_sort(arr):
    if len(arr) < 2:
        return arr
    pivot = arr[0]
    less = [i for i in arr[1:] if i <= pivot]
    greater = [i for i in arr[1:] if i > pivot]
    return quick_sort(less) + [pivot] + quick_sort(greater)

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[i] < arr[left]:
        largest = left

    if right < n and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

# --- Function to generate a random array ---
def generate_random_array(size):
    return [random.randint(1, 1000) for _ in range(size)]

# --- Function to measure the execution time of a sorting algorithm ---
def time_sorting_algorithm(sort_function, arr):
    start_time = time.time()
    sort_function(arr.copy())  # Use arr.copy() to avoid modifying the original array
    end_time = time.time()
    return end_time - start_time

# --- Main execution ---
if __name__ == "__main__":
    array_size = int(input("Enter the size of the array: "))

    # Generate random array
    random_array = generate_random_array(array_size)

    # Sorting algorithms to test
    sorting_algorithms = {
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Bubble Sort": bubble_sort,
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort
    }

    # Time each algorithm
    execution_times = {}
    for name, algorithm in sorting_algorithms.items():
        execution_times[name] = time_sorting_algorithm(algorithm, random_array)

    # --- Plotting the results ---
    plt.figure(figsize=(10, 6))
    plt.bar(execution_times.keys(), execution_times.values(), color='skyblue')
    plt.xlabel("Sorting Algorithms")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Sorting Algorithm Performance Comparison (Array Size: {array_size})")
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()

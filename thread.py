import time
import fetch
import stats
import threading

def benchmark_skiplimit(count, page_size):
    """Benchmark skip-limit pagination."""
    times = []
    run_count = 3
    page_number, items_fetched = 1, 0

    while items_fetched < count:  # Stop when all items are fetched
        start_time = time.time()
        for _ in range(run_count):
            data = fetch.skiplimit(page_size, page_number)
        end_time = time.time()

        if not data:  # No more data to fetch
            break

        # Calculate the number of items to fetch in this iteration
        remaining_items = count - items_fetched
        if len(data) > remaining_items:
            data = data[:remaining_items]  # Trim the excess items
            items_fetched += len(data)
            times.append((end_time - start_time) / run_count)
            break  # Exit the loop since we have fetched the required number of items

        items_fetched += len(data)
        page_number += 1
        times.append((end_time - start_time) / run_count)

    
    assert items_fetched == count, f"Expected {count} items, but fetched {items_fetched} items"
    return times

def benchmark_idlimit(count, page_size):
    """Benchmark cursor-based pagination."""
    times = []
    run_count = 3
    items_fetched = 0
    last_id = None

    while items_fetched < count:  # Stop when all items are fetched
        start_time = time.time()
        for _ in range(run_count):
            data, new_last_id = fetch.idlimit_1(page_size, last_id)
        end_time = time.time()

        # Update the last_id
        last_id = new_last_id

        if not data:  # No more data to fetch
            break

        # Calculate the number of items to fetch in this iteration
        remaining_items = count - items_fetched
        if len(data) > remaining_items:
            data = data[:remaining_items]  # Trim the excess items
            items_fetched += len(data)
            times.append((end_time - start_time) / run_count)
            break  # Exit the loop since we have fetched the required number of items

        items_fetched += len(data)
        times.append((end_time - start_time) / run_count)

 
    assert items_fetched == count, f"Expected {count} items, but fetched {items_fetched} items"
    return times

def print_stats(times, count, page_size, approach):
    """Print statistical metrics."""
    s = stats.all(times)
    print("\"{}\",{},{},{},{},{},{}".format(approach, count, page_size, s['mean'], s['p99'], s['p95'], s['p50']))

def bench(count, page_size):
    """Run benchmarks for both pagination strategies."""
    approach = 'skiplimit'
    times = benchmark_skiplimit(count, page_size)
    print_stats(times, count, page_size, approach)

    approach = 'idlimit'
    times = benchmark_idlimit(count, page_size)
    print_stats(times, count, page_size, approach)

def run_benchmarks(dataset_sizes, page_sizes):
    """Run benchmarks for each combination of dataset size and page size."""
    for count in dataset_sizes:
        for page_size in page_sizes:
            bench(count, page_size)

if __name__ == '__main__':
    # Print the CSV header
    print("\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"".format(
        "Approach", "Count", "Page Size", "Mean (in microseconds)", 
        "p99 (in microseconds)", "p95 (in microseconds)", "p50 (in microseconds)"
    ))

    # Define the dataset sizes and page sizes to test
    dataset_sizes = list(range(1000, 204020, 5000))  # Dataset sizes: 1000 to 200000 with an increment of 5000
    page_sizes = [500]  # Page sizes: 500, 1000, 2000, 5000

    # Split the dataset sizes into 5 chunks for multithreading
    chunk_size = len(dataset_sizes) // 5
    chunks = [dataset_sizes[i:i + chunk_size] for i in range(0, len(dataset_sizes), chunk_size)]

    # Create and start threads
    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=run_benchmarks, args=(chunk, page_sizes))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
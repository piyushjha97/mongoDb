import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into a pandas DataFrame
df = pd.read_csv("results.csv")

# Function to plot response time vs number of data fetched for a specific page size
def plot_response_time_vs_count(df, page_size, metric):
    plt.figure(figsize=(10, 6))
    
    # Filter data for the specified page size
    page_data = df[df["Page Size"] == page_size]
    
    # Filter data for each approach
    skiplimit_data = page_data[page_data["Approach"] == "skiplimit"]
    idlimit_data = page_data[page_data["Approach"] == "idlimit"]
    
    # Plot for skiplimit
    plt.plot(skiplimit_data["Count"], skiplimit_data[metric], label="skiplimit", marker="o")
    
    # Plot for idlimit
    plt.plot(idlimit_data["Count"], idlimit_data[metric], label="idlimit", marker="o")
    
    # Add labels and title
    plt.xlabel("Number of Data Fetched (Count)")
    plt.ylabel(f"{metric} (in microseconds)")
    plt.title(f"Response Time vs Number of Data Fetched (Page Size = {page_size})")
    plt.legend()
    plt.grid(True)
    plt.show()

# List of page sizes to plot
page_sizes = [200, 500, 1000, 2000, 5000]

# List of metrics to plot
metrics = ["Mean (in microseconds)", "p99 (in microseconds)", "p95 (in microseconds)", "p50 (in microseconds)"]

# Generate graphs for each page size and metric
for page_size in page_sizes:
    for metric in metrics:
        plot_response_time_vs_count(df, page_size, metric)
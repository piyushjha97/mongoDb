import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into a pandas DataFrame
df = pd.read_csv("results_0.csv")

# Function to plot the performance metrics
def plot_metrics(df, metric, title):
    plt.figure(figsize=(12, 6))
    
    # Filter data for each approach
    skiplimit_data = df[df["Approach"] == "skiplimit"]
    idlimit_data = df[df["Approach"] == "idlimit"]
    
    # Plot for skiplimit
    plt.plot(skiplimit_data["Page Size"], skiplimit_data[metric], label="skiplimit", marker="o")
    
    # Plot for idlimit
    plt.plot(idlimit_data["Page Size"], idlimit_data[metric], label="idlimit", marker="o")
    
    # Add labels and title
    plt.xlabel("Page Size")
    plt.ylabel(f"{metric} (in microseconds)")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot for Mean
plot_metrics(df, "Mean (in microseconds)", "Mean Response Time vs Page Size")

# Plot for p99
plot_metrics(df, "p99 (in microseconds)", "p99 Response Time vs Page Size")

# Plot for p95
plot_metrics(df, "p95 (in microseconds)", "p95 Response Time vs Page Size")

# Plot for p50
plot_metrics(df, "p50 (in microseconds)", "p50 Response Time vs Page Size")
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into a pandas DataFrame
df = pd.read_csv("results.csv")

# Filter data for the specific page size (e.g., 1000)
page_size = 1000
page_data = df[df["Page Size"] == page_size]

# Filter data for each approach
skiplimit_data = page_data[page_data["Approach"] == "skiplimit"]
idlimit_data = page_data[page_data["Approach"] == "idlimit"]

# Define the x-axis values (dataset sizes)
x_values = sorted(page_data["Count"].unique())

# Create the plot for mean
plt.figure(figsize=(10, 6))

# Plot for skiplimit (mean)
plt.plot(
    skiplimit_data["Count"], 
    skiplimit_data["Mean (in microseconds)"], 
    label="skiplimit (mean)", 
    marker="o", 
    linestyle="-", 
    color="blue", 
    linewidth=2, 
    markersize=8
)

# Plot for idlimit (mean)
plt.plot(
    idlimit_data["Count"], 
    idlimit_data["Mean (in microseconds)"], 
    label="idlimit (mean)", 
    marker="o", 
    linestyle="-", 
    color="orange", 
    linewidth=2, 
    markersize=8
)

# Add labels and title
plt.xlabel("Total number of records in Result Set", fontsize=12)
plt.ylabel("Response Time (in microseconds)", fontsize=12)
plt.title(f"Mean and Count when Page Size is {page_size}", fontsize=14)

# Set x-axis ticks explicitly
plt.xticks(x_values, fontsize=10)

# Adjust y-axis range based on your data
plt.ylim(0, max(df["Mean (in microseconds)"]) * 1.1)  # Adjust this range to fit your data

# Add grid lines
plt.grid(True, linestyle="--", alpha=0.6)

# Add legend
plt.legend(fontsize=12, loc="upper left")

# Show the plot
plt.tight_layout()  # Ensure the layout is not cut off
plt.show()
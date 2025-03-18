import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load CSV file into a DataFrame
df = pd.read_csv("Output.csv")

df = df[["Analysis", "Result", "Unit"]]

df.drop(df[df.Unit != "ppm"].index, inplace=True)
df.drop(df[df.Result == "---"].index, inplace=True)
df['Result'] = df['Result'].str.strip('<')
df = df[["Analysis", "Result"]]
df["Result"] = pd.to_numeric(df["Result"], errors="coerce")

df = df.reset_index(drop=True)

# Summary statistics
print(df.describe())

# Visually pleasant colors
colors = list(plt.get_cmap("tab10").colors)

# The rest of the code is for the visualization functions

def bar_chart(df):
    # Drop rows where "Result" couldn't be converted (optional)
    df = df.dropna(subset=["Result"])

    # Group by "Analysis" and calculate the mean of "Result"
    df_grouped = df.groupby("Analysis")["Result"].mean()
    # Sort the values from most to least (descending order)
    df_grouped = df_grouped.sort_values(ascending=False)

    # Create a bar chart
    plt.figure(figsize=(12, 6))
    df_grouped.plot(kind="bar", color=colors, edgecolor="black")

    # Customize the plot
    plt.xlabel("Element")
    plt.ylabel("Average Concentration (ppm)")
    plt.title("Average Concentration of Elements")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    

    # Show the plot
    plt.tight_layout()
    plt.show()

def heatmap(df):
    # Add a Sample ID to group repeated elements properly
    df["Sample"] = df.groupby("Analysis").cumcount() + 1

    # Pivot the DataFrame to have elements (rows) vs samples (columns)
    df_pivot = df.pivot(index="Analysis", columns="Sample", values="Result")

    # Create the heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(df_pivot, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5)

    # Customize the heatmap
    plt.xlabel("Sample Number")
    plt.ylabel("Element")
    plt.title("Heatmap of Element Concentrations Across Samples")
    plt.xticks(rotation=45, ha="right")

    # Show the plot
    plt.tight_layout()
    plt.show()

def boxplot(df):
    # Create the boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Analysis", y="Result", data=df)

    # Customize the plot
    plt.xticks(rotation=45)
    plt.xlabel("Element")
    plt.ylabel("Concentration (ppm)")
    plt.title("Box & Whisker Plot of Element Concentrations")
    plt.grid(True)

    # Show the plot
    plt.show()

def stacked_bar_chart(df):
    # Drop rows where "Result" couldn't be converted (optional)
    df = df.dropna(subset=["Result"])

    # Pivot the DataFrame to have "Sample" as index and "Analysis" as columns
    df_pivot = df.pivot_table(index="Sample", columns="Analysis", values="Result", aggfunc="mean")

    # Generate random colors for each element
    num_elements = len(df_pivot.columns)
    random_colors = np.random.rand(num_elements, 3)  # RGB format

    # Plot the stacked bar chart
    df_pivot.plot(kind="bar", stacked=True, figsize=(12, 6), color=colors, edgecolor="black")

    # Customize the plot
    plt.xlabel("Sample")
    plt.ylabel("Concentration (ppm)")
    plt.title("Stacked Bar Chart of Element Concentrations per Sample")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Element", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()

bar_chart(df)
heatmap(df)
stacked_bar_chart(df)

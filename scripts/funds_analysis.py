import pandas as pd
import matplotlib.pyplot as plt

def load_fund_data(file_path="data/synthetic_fund_data.csv"):
    """Load fund data from a CSV file."""
    return pd.read_csv(file_path)

def analyze_key_metrics(df):
    """Analyze key metrics (IRR, MOIC) in the dataset."""
    print("Key Metrics Summary:")
    print(df[["IRR (%)", "MOIC"]].describe())
    
def plot_metrics(df):
    """Visualize fund metrics."""
    # IRR Distribution
    plt.figure(figsize=(8, 5))
    df["IRR (%)"].plot(kind="hist", bins=10, alpha=0.7, title="IRR Distribution")
    plt.xlabel("IRR (%)")
    plt.ylabel("Frequency")
    plt.grid()
    plt.show()

    # MOIC vs. Vintage Year
    plt.figure(figsize=(8, 5))
    plt.scatter(df["Vintage Year"], df["MOIC"], alpha=0.7)
    plt.title("MOIC vs. Vintage Year")
    plt.xlabel("Vintage Year")
    plt.ylabel("MOIC")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    file_path = "data/synthetic_fund_data.csv"
    df = load_fund_data(file_path)
    analyze_key_metrics(df)
    plot_metrics(df)

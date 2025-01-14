import pandas as pd
import numpy as np

def generate_synthetic_data(file_path="data/synthetic_fund_data.csv"):
    """Generate synthetic private equity fund data."""
    np.random.seed(42)
    
    # Simulate fund data
    funds = {
        "Fund Name": [f"Fund {i}" for i in range(1, 11)],
        "Vintage Year": np.random.choice(range(2000, 2021), 10),
        "Committed Capital (M)": np.random.uniform(50, 500, 10),
        "IRR (%)": np.random.uniform(5, 25, 10),
        "MOIC": np.random.uniform(1.2, 3.0, 10),
    }
    df = pd.DataFrame(funds)
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    generate_synthetic_data()

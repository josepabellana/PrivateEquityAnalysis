import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def simulate_j_curve(years=10, commitments=100, peak_drawdown_year=2):
    """
    Simulate a J-Curve for private equity cash flows.
    
    :param years: Total duration of the investment (in years).
    :param commitments: Total committed capital.
    :param peak_drawdown_year: Year when drawdowns peak.
    :return: DataFrame containing cash flows and cumulative metrics.
    """
    # Initialize cash flow array
    drawdowns = np.zeros(years)
    distributions = np.zeros(years)

    # Negative cash flows (drawdowns) in early years
    for year in range(peak_drawdown_year):
        drawdowns[year] = -(commitments * (peak_drawdown_year - year) / peak_drawdown_year * 0.5)

    # Positive cash flows (distributions) in later years
    remaining_years = years - peak_drawdown_year
    for year in range(remaining_years):
        distributions[peak_drawdown_year + year] = (
            commitments * (year + 1) / remaining_years * 0.7
        )

    # Combine drawdowns and distributions
    cash_flows = drawdowns + distributions
    cumulative_cash_flow = np.cumsum(cash_flows)

    # Create DataFrame for visualization
    data = pd.DataFrame({
        "Year": np.arange(1, years + 1),
        "Cash Flow": cash_flows,
        "Cumulative Cash Flow": cumulative_cash_flow
    })
    
    return data


def plot_j_curve(data):
    """Plot the J-Curve."""
    plt.figure(figsize=(10, 6))
    plt.plot(data["Year"], data["Cumulative Cash Flow"], label="Cumulative Cash Flow")
    plt.axhline(0, color="grey", linestyle="--")
    plt.title("J-Curve Simulation")
    plt.xlabel("Year")
    plt.ylabel("Cumulative Cash Flow")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    data = simulate_j_curve()
    plot_j_curve(data)

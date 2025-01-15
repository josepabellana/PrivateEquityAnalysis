import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def simulate_j_curve_with_capital_calls(years=10, commitments=100, peak_drawdown_year=4):
    """
    Simulate a J-Curve with capital calls and scenarios.
    
    :param years: Total duration of the investment (in years).
    :param commitments: Total committed capital.
    :param peak_drawdown_year: Year when drawdowns peak.
    :return: DataFrame containing base, optimistic, pessimistic cash flows, and capital calls.
    """
    # Base Scenario
    drawdowns = np.zeros(years)
    distributions = np.zeros(years)
    accumulative_cashflow = np.zeros(years)  # Track capital calls

    # Capital calls in the first few years
    for year in range(peak_drawdown_year):
        accumulative_cashflow[year] = -commitments * 0.25  # Assume 25% of commitments each year
        drawdowns[year] = -accumulative_cashflow[year]

    # Positive cash flows (distributions)
    remaining_years = years - peak_drawdown_year
    for year in range(remaining_years):
        distributions[peak_drawdown_year + year] = (
            commitments * (year + 1) / remaining_years * 0.7
        )
        accumulative_cashflow[year] = accumulative_cashflow[year] +  (commitments * (year + 1) / remaining_years * 0.7)
    base_cash_flow = drawdowns + distributions

    # Optimistic Scenario
    optimistic_distributions = distributions * 1.2
    optimistic_cash_flow = drawdowns + optimistic_distributions

    # Pessimistic Scenario
    pessimistic_distributions = distributions * 0.8
    pessimistic_cash_flow = drawdowns + pessimistic_distributions

    # Combine Scenarios
    data = pd.DataFrame({
        "Year": np.arange(1, years + 1),
        "Base": np.cumsum(base_cash_flow),
        "Optimistic": np.cumsum(optimistic_cash_flow),
        "Pessimistic": np.cumsum(pessimistic_cash_flow),
        "Cumulative Cashflows": np.cumsum(accumulative_cashflow),  # Cumulative capital calls
    })
    
    return data

def plot_j_curve_with_capital_calls_as_bars(data):
    """
    Plot the J-Curve with scenarios and capital calls shown as bars.
    
    :param data: DataFrame containing cumulative cash flow and capital calls.
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot Base Scenario (Line)
    ax1.plot(data["Year"], data["Base"], label="Base Scenario", color="blue", linewidth=2)

    # Add Shaded Area for Scenarios
    ax1.fill_between(
        data["Year"],
        data["Pessimistic"],
        data["Optimistic"],
        color="gray",
        alpha=0.3,
        label="Scenario Range (Optimistic to Pessimistic)"
    )

    # Plot Capital Calls (Bars)
    ax1.bar(
        data["Year"], 
        data["Cumulative Cashflows"], 
        color="orange", 
        alpha=0.6, 
        label="Cumulative Cashflows"
    )

    # Add Break-Even Line
    ax1.axhline(0, color="black", linestyle="--", label="Break-Even")

    # Customize Plot
    ax1.set_title("Private Equity J-Curve with Cumulative Cashflows", fontsize=14)
    ax1.set_xlabel("Year", fontsize=12)
    ax1.set_ylabel("Cumulative Cash Flow", fontsize=12)
    ax1.legend(loc="upper left")
    ax1.grid()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Simulate data
    data = simulate_j_curve_with_capital_calls(years=10, commitments=100, peak_drawdown_year=4)
    
    # Plot the J-Curve with Accumulative Cashflows as bars
    plot_j_curve_with_capital_calls_as_bars(data)
    
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def monte_carlo_j_curve_simulation(
    years=10, commitments=100, peak_drawdown_year=4, capital_call_pattern=None, n_simulations=100
):
    """
    Perform Monte Carlo simulations for the J-Curve.
    
    :param years: Total duration of the investment (in years).
    :param commitments: Total committed capital.
    :param peak_drawdown_year: Number of years for capital calls.
    :param capital_call_pattern: List of percentages for capital calls.
    :param n_simulations: Number of simulations to run.
    :return: DataFrame containing simulation results (mean, percentiles).
    """
    if capital_call_pattern is None:
        capital_call_pattern = [0.4, 0.3, 0.2, 0.1]  # Default pattern

    if len(capital_call_pattern) != peak_drawdown_year:
        raise ValueError("Capital call pattern must match the number of drawdown years.")

    # Prepare capital calls
    capital_calls = np.zeros(years)
    for i, pct in enumerate(capital_call_pattern):
        capital_calls[i] = commitments * pct

    # Store simulation results
    all_simulations = []

    for _ in range(n_simulations):
        # Randomize distributions (e.g., +/- 20%)
        drawdowns = -capital_calls
        distributions = np.zeros(years)
        remaining_years = years - peak_drawdown_year
        for year in range(remaining_years):
            random_factor = np.random.uniform(0.8, 1.2)  # Random variation
            distributions[peak_drawdown_year + year] = (
                commitments * (year + 1) / remaining_years * 0.7 * random_factor
            )
        cash_flow = drawdowns + distributions
        cumulative_cash_flow = np.cumsum(cash_flow)
        all_simulations.append(cumulative_cash_flow)

    # Convert to DataFrame
    simulations_df = pd.DataFrame(all_simulations).T
    simulations_df.columns = [f"Sim_{i+1}" for i in range(n_simulations)]

    # Calculate statistics
    simulations_df["Year"] = np.arange(1, years + 1)
    simulations_df["Mean"] = simulations_df.iloc[:, :-1].mean(axis=1)
    simulations_df["5th Percentile"] = simulations_df.iloc[:, :-1].quantile(0.05, axis=1)
    simulations_df["95th Percentile"] = simulations_df.iloc[:, :-1].quantile(0.95, axis=1)

    return simulations_df


def plot_monte_carlo_simulations(simulations_df):
    """
    Plot Monte Carlo simulations and key percentiles.
    
    :param simulations_df: DataFrame containing simulation results.
    """
    plt.figure(figsize=(10, 6))

    # Plot individual simulations (light gray lines)
    for col in simulations_df.columns[:-4]:  # Exclude stats columns
        plt.plot(simulations_df["Year"], simulations_df[col], color="lightgray", alpha=0.2)

    # Plot mean and percentiles
    plt.plot(simulations_df["Year"], simulations_df["Mean"], label="Mean", color="blue", linewidth=2)
    plt.fill_between(
        simulations_df["Year"],
        simulations_df["5th Percentile"],
        simulations_df["95th Percentile"],
        color="gray",
        alpha=0.3,
        label="5th-95th Percentile Range"
    )

    # Add labels and legend
    plt.title("Monte Carlo Simulations for J-Curve", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Cumulative Cash Flow", fontsize=12)
    plt.axhline(0, color="black", linestyle="--", label="Break-Even")
    plt.legend()
    plt.grid()
    plt.show()

def calculate_irr(cash_flows):
    """
    Calculate the internal rate of return (IRR).
    
    :param cash_flows: List of cash flows over time.
    :return: IRR as a percentage.
    """
    irr = np.irr(cash_flows)  # IRR calculation
    return irr * 100  # Convert to percentage

def calculate_dpi(distributions, capital_calls):
    """
    Calculate the Distributions to Paid-In Capital (DPI).
    
    :param distributions: List of distributions over time.
    :param capital_calls: List of capital calls over time.
    :return: DPI ratio.
    """
    total_distributions = np.sum(distributions)
    total_paid_in = np.sum(capital_calls)
    return total_distributions / total_paid_in

if __name__ == "__main__":
    # Run Monte Carlo Simulations
    simulations_df = monte_carlo_j_curve_simulation(
        years=10, commitments=100, peak_drawdown_year=4, n_simulations=100
    )

    # Plot the Monte Carlo Simulations
    plot_monte_carlo_simulations(simulations_df)

    # Example Cash Flow for Metrics
    sample_cash_flow = [-40, -30, -20, -10, 10, 20, 30, 40, 50, 60]  # Example
    capital_calls = [-cf for cf in sample_cash_flow if cf < 0]
    distributions = [cf for cf in sample_cash_flow if cf > 0]

    # Calculate IRR and DPI
    irr = calculate_irr(sample_cash_flow)
    dpi = calculate_dpi(distributions, capital_calls)

    print(f"IRR: {irr:.2f}%")
    print(f"DPI: {dpi:.2f}")
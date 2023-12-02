import numpy as np

def calculate_information_ratio(portfolio_returns, benchmark_returns, annualization_factor=252):
    """
    Calculate the Information Ratio (IR) of a portfolio compared to a benchmark.

    :param portfolio_returns: A NumPy array of portfolio returns.
    :param benchmark_returns: A NumPy array of benchmark returns. Must be the same length as portfolio_returns.
    :param annualization_factor: Factor to annualize the returns. Default is 252 (trading days in a year).
    :return: The Information Ratio (annualized).
    """
    if len(portfolio_returns) != len(benchmark_returns):
        raise ValueError("Portfolio and benchmark returns must have the same length.")

    # Calculate excess returns
    excess_returns = portfolio_returns - benchmark_returns

    # Calculate the mean and standard deviation of excess returns
    mean_excess_return = np.mean(excess_returns)
    std_excess_return = np.std(excess_returns)

    # Avoid division by zero
    if std_excess_return == 0:
        raise ValueError("Standard deviation of excess returns is zero. Cannot compute Information Ratio.")

    # Calculate and return the Information Ratio
    information_ratio = (mean_excess_return / std_excess_return) * np.sqrt(annualization_factor)
    return information_ratio

# Example usage
# Assuming these are daily returns
portfolio_returns = np.array([0.001, 0.002, 0.0015, 0.0025, -0.001])  # Sample portfolio returns
benchmark_returns = np.array([0.0006, 0.00015, 0.001, 0.002, -0.0005])  # Sample benchmark returns

try:
    ir = calculate_information_ratio(portfolio_returns, benchmark_returns)
    print(f"Information Ratio: {ir:.4f}")
except ValueError as e:
    print(f"Error calculating Information Ratio: {e}")

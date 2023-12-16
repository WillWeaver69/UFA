def calculate_expected_active_return(portfolio_weights, benchmark_weights, expected_excess_returns):
    """
    Calculate the expected active return of a portfolio.

    Parameters:
    portfolio_weights (list of float): The weights of each security in the actively managed portfolio.
    benchmark_weights (list of float): The weights of each security in the benchmark portfolio.
    expected_excess_returns (list of float): The expected excess return of each security over the benchmark.

    Returns:
    float: The expected active return of the portfolio.

    Raises:
    ValueError: If the lengths of the input lists are not equal or if the sum of calculated active weights is not close to zero.
    """

    # Validate input lengths
    if not (len(portfolio_weights) == len(benchmark_weights) == len(expected_excess_returns)):
        raise ValueError("All input lists must be of equal length.")

    # Calculate active weights
    active_weights = [pw - bw for pw, bw in zip(portfolio_weights, benchmark_weights)]

    # Validate that the sum of active weights is close to zero
    if not abs(sum(active_weights)) < 1e-6:
        raise ValueError("The sum of active weights must be close to zero.")

    # Calculate and return the expected active return
    return sum(w * r for w, r in zip(active_weights, expected_excess_returns))

# Example usage
example_portfolio_weights = [0.25, 0.20, 0.30, 0.25]
example_benchmark_weights = [0.20, 0.25, 0.25, 0.30]
example_expected_excess_returns = [0.08, 0.06, 0.10, 0.04]

try:
    active_return = calculate_expected_active_return(example_portfolio_weights, example_benchmark_weights, example_expected_excess_returns)
    print("Expected Active Return:", active_return)
except ValueError as e:
    print("Error:", e)

  

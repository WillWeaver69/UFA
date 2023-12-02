import numpy as np

def capm(risk_free, beta, market_return):
    """
    Function to calculate the required return for equities using the capital asset pricing model (CAPM).
    Supports batch processing and returns formatted results.

    Args:
    risk_free (float or iterable of floats): The risk-free rate, typically annualized short-term government bond yields.
    beta (float or iterable of floats): The level of risk associated with each equity.
    market_return (float or iterable of floats): Mean return on a certain market index.

    Returns:
    np.array: The calculated required returns for the equities as formatted strings.

    Raises:
    ValueError: If any input is invalid.
    """
    
    # Ensure inputs are arrays
    risk_free = np.atleast_1d(risk_free)
    beta = np.atleast_1d(beta)
    market_return = np.atleast_1d(market_return)

    # Validate inputs
    if np.any(risk_free < 0) or np.any(beta < 0) or np.any(market_return < 0):
        raise ValueError("Input values cannot be negative.")

    ke = risk_free + beta * (market_return - risk_free)
    return np.array([f"{x * 100:.2f}%" for x in ke])

# Example usage
try:
    # For single asset calculation
    ke_single = capm(0.04, 0.8, 0.079)
    print(f"Single asset CAPM return: {ke_single[0]}")

    # For multiple assets calculation
    risk_free_rates = [0.03, 0.04, 0.05]
    betas = [0.7, 0.8, 1.0]
    market_returns = [0.07, 0.08, 0.09]
    ke_multiple = capm(risk_free_rates, betas, market_returns)
    print(f"Multiple assets CAPM returns: {ke_multiple}")
except ValueError as e:
    print(f"Error: {e}")

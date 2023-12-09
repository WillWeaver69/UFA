def equity_forward_price_days(S0, r, q, T_days):
    """
    Calculate the forward price of an equity forward contract with continuous dividends,
    with the time to maturity specified in days.

    Parameters:
    S0 (float): The current spot price of the equity.
    r (float): The risk-free interest rate, continuously compounded.
    q (float): The continuous dividend yield.
    T_days (int): The time to maturity of the contract in days.

    Returns:
    float: The calculated forward price of the equity.

    The formula used is:
    FP = S0 * exp((r - q) * T)
    where T is converted from days to years (assuming 365 days in a year),
    and exp() is the exponential function representing e^(x).
    """

    from math import exp

    # Convert days to years
    T_years = T_days / 365

    # Calculate the forward price
    FP = S0 * exp((r - q) * T_years)

    return FP

# Example usage of the function
# Assume a spot price of $1140, risk-free rate of 4.6% (0.046), dividend yield of 2.1% (0.021), and a 140-day contract
forward_price_days = equity_forward_price_days(1140, 0.046, 0.021, 140)
forward_price_days

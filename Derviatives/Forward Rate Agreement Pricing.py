def fra_forward_rate(S_short, T_short, S_long, T_long):
    """
    Calculate the no-arbitrage forward rate for a Forward Rate Agreement (FRA).

    Parameters:
    S_short (float): The shorter period spot rate (e.g., 30-day LIBOR).
    T_short (int): The total time in days for the shorter period.
    S_long (float): The longer period spot rate (e.g., 120-day LIBOR).
    T_long (int): The total time in days for the longer period.

    Returns:
    float: The calculated no-arbitrage forward rate for the FRA.

    The formula used is:
    F = ((1 + S_long * T_long/360) / (1 + S_short * T_short/360)) - 1
    This formula calculates the actual rate for the FRA period.
    """

    # Calculate the forward rate
    forward_rate = ((1 + S_long * T_long/360) / (1 + S_short * T_short/360)) - 1

    # Annualizing the forward rate
    forward_rate_annualized = forward_rate * (360 / (T_long - T_short))

    return forward_rate, forward_rate_annualized

# Example usage of the function
# Assume a 30-day LIBOR of 4% (0.04) and a 120-day LIBOR of 5% (0.05)
fra_rate, fra_rate_annualized = fra_forward_rate(0.04, 30, 0.05, 120)
fra_rate, fra_rate_annualized

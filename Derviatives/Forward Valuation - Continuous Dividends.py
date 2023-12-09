def value_of_equity_index_forward(Spot_Index_Value, r, q, T_days, t_days, Forward_Price_Initiation):
    """
    Calculate the value of a forward contract on an equity index with continuous dividends.

    Parameters:
    Spot_Index_Value (float): The current value of the index.
    r (float): The continuously compounded risk-free rate.
    q (float): The continuous dividend yield.
    T_days (int): The original time to maturity of the contract in days.
    t_days (int): The time elapsed since the initiation of the contract in days.
    Forward_Price_Initiation (float): The forward price at the initiation of the contract.

    Returns:
    float: The value to the long position of the forward contract on the index.

    The formula used is:
    Value = (Spot_Index_Value * exp((r - q) * (T - t))) - (Forward_Price_Initiation * exp(r * (T - t)))
    where T and t are converted from days to years.
    """

    from math import exp

    # Convert days to years
    T_years = T_days / 365
    t_years = t_days / 365
    

    # Calculate the value of the forward contract
    value = (Spot_Index_Value / (exp((q) * (T_years - t_years)))) - (Forward_Price_Initiation / (exp((r) * (T_years - t_years))))

    return value

# Example usage of the function
# Assume an index value of 1025, risk-free rate of 4.6% (0.046), dividend yield of 2.1% (0.021), 
# original contract duration of 140 days, 95 days elapsed, and an initial forward price of 1151
value_of_contract = value_of_equity_index_forward(1025, 0.046, 0.021, 140, 95, 1151)
value_of_contract

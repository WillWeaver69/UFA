def fra_value_at_maturity(notional_principal, market_rate, contract_rate, T):
    """
    Calculate the value of a Forward Rate Agreement (FRA) at maturity.

    Parameters:
    notional_principal (float): The notional principal amount of the FRA.
    market_rate (float): The prevailing market interest rate at the expiration of the FRA.
    contract_rate (float): The interest rate agreed upon in the FRA.
    T (int): The number of days from the settlement date to the end of the loan term.

    Returns:
    float: The value of the FRA at maturity, which is the cash settlement payment.

    The formula used is:
    Value = Notional Principal * (Market Rate - Contract Rate) * (T / 360) * exp(-Market Rate * (T / 360))
    """

    from math import exp

    # Calculate the value of the FRA at maturity
    value = notional_principal * (market_rate - contract_rate) * (T / 360) * exp(-market_rate * (T / 360))

    return value

# Example usage of the function
# Assume a notional principal of $1 million, market rate of 6% (0.06), contract rate of 5.32% (0.0532), and a loan term of 90 days
fra_maturity_value = fra_value_at_maturity(1e6, 0.06, 0.0532, 90)
fra_maturity_value

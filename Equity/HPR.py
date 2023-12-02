def calculate_HPR(initial_price, ending_price, cash_flows):
    """
    Function to calculate the holding period return of an asset as a percentage.
    This version supports multiple cash flows and better input validation.

    Args:
    initial_price (float): The price at which the asset was bought.
    ending_price (float): The price of the asset at the end of the holding period.
    cash_flows (list of floats): A list of cash flows received during the holding period.
                                 Each element represents a cash flow at a specific time.

    Returns:
    float: The calculated holding period return as a percentage.

    Raises:
    ValueError: If initial_price is less than or equal to 0, 
                or if any cash flow is less than 0.
    """
    
    # Validate inputs
    if initial_price <= 0:
        raise ValueError("Initial price must be greater than 0.")
    if any(cf < 0 for cf in cash_flows):
        raise ValueError("Cash flows cannot be negative.")
    
    total_cash_flow = sum(cash_flows)
    HPR = ((ending_price + total_cash_flow) / initial_price - 1) * 100
    return HPR

# Example usage
try:
    hpr_percentage = calculate_HPR(100, 200, [50, 25])  # Multiple cash flows can be passed as a list
    print(f"Holding period return for the asset is {hpr_percentage:.2f}%")
except ValueError as e:
    print(f"Error: {e}")

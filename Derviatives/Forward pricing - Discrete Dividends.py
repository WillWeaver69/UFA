def forward_pricing_discrete_dividends(spot_price, risk_free, term, dividends, days):
    """
    Function to calculate the forward price on an asset that provides discrete dividends over the contract term. Equity stocks are an example of an asset that meets this criteria
    risk_free : the annualised risk-free rate (i.e. the annualised return on a short-term government bond
    term: forward contract term in days
    dividends : series dividends to be paid in the future
    days = series of days representing the number of days from today´s date until each corresponding dividend will be paid
    """
    
    present_value_dividends = 0
    # Loop through each dividend and corresponding day
    for dividend, T in zip(dividends, days):
        present_value = dividend / ((1 + risk_free) ** (T / 365))
        present_value_dividends += present_value

   
    
    forward_price_discrete_dividends = (spot_price - present_value_dividends) * (1 +risk_free)** (term/365)
    return forward_price_discrete_dividends

#Example usage
forward_pricing_discrete_dividends(30, 0.05, 100, [0.4, 0.4], [15, 85])

def forward_pricing(spot_price, risk_free, term):
    """
    Function to calculate the forward price on an asset that costs nothing to store and makes not payments to its owner over the life of the forward contract. A zero-coupon bond meets these criteria.
    spot_price : current market price for the asset
    risk_free : the annualised risk-free rate (i.e. the annualised return on a short-term government bond
    term: forward contract term in years
    """
    forward_price = spot_price * (1 + risk_free)**term
    return forward_price


#Example usage
forward_pricing(500, 0.06, 0.25)

def value_forward_contract_fixed_income(spot_price, risk_free, term, coupon, days, forward_price_fixed_income_security, T):
    
    #Calculate present value of coupons at time T
    present_value_coupons =0
    for coupon, days in zip(coupon,days):
        present_value_coupon = coupon / (1 +risk_free)**((days - T)/365)
        present_value_coupons += present_value_coupon

        
    value_forward_contract = (spot_price - present_value_coupons) - (forward_price_fixed_income_security / (1+risk_free)**((term -T)/365))

    return value_forward_contract

#Example usage
value_forward_contract_fixed_income(1090, 0.06,250,[35],[182],1057.37,100)
    

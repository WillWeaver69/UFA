def calculate_forward_price_fixed_income_security(spot_price, risk_free, term, coupon, days):
    
    present_value_coupons=0
    #calculate present value of coupon
    for coupon, days in zip(coupon,days):
        present_value_coupon = coupon / ((1+risk_free)**(days/365))
        present_value_coupons += present_value_coupon

        
        
    forward_price_fixed_income_security = (spot_price - present_value_coupons) * (1 + risk_free)**(term/365)


    return forward_price_fixed_income_security


#Example usage
calculate_forward_price_fixed_income_security(1050, 0.06, 250, [35],[182])
        

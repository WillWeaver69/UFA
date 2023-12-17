def calculate_expected_dividend(previous_dividend, previous_EPS, future_EPS, target_payout_ratio, number_of_years_dividend_adjustment):
    
    expected_increase_EPS = future_EPS - previous_EPS
    
    adjustment_factor = 1 / number_of_years_dividend_adjustment
    
    expected_dividend = previous_dividend + (expected_increase_EPS * target_payout_ratio * adjustment_factor)
    

    return expected_dividend

#Example usage

calculate_expected_dividend(0.7,3.5,4.5,0.35,5)

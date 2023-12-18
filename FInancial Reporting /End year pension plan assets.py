def calculate_endyear_pension_plan_assets(fair_value_beginning, contributions, actual_return, benefits_paid):
    #Function to calculate the fair value of defined benefit contribution plan at the end of the year
    
    end_year_fair_value = fair_value_beginning + contributions + actual_return - benefits_paid
    
    return end_year_fair_value

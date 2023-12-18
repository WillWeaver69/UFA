def calculate_endyear_pension_plan_assets(beginning_plan_assets, contributions, actual_return, benefits_paid):
    #Function to calculate the fair value of defined benefit contribution plan at the end of the year
    
    ending_plan_assets = beginning_plan_assets + contributions + actual_return - benefits_paid
    
    return ending_plan_assets

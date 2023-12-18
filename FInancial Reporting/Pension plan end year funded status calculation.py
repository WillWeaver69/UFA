def calculate_end_year_funded_status_pension_plan(ending_plan_assets, ending_PBO):
    """Function to calculate the funded status of a pension plan.
    The balance sheet presentation is as follows:
    balance sheet asset (liability) = funded status
    If the funded status is negative it is reported as a liability.
    IF the funded status is positive, it is reported as an asset subject to a ceiling of
    present value of future economic benefits(such as future refunds or reduced contributions)
    """
    
    end_year_funded_status_pension_plan =  ending_plan_assets - ending_PBO
    
    return end_year_funded_status_pension_plan

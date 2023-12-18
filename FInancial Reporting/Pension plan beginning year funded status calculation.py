def calculate_beginning_year_funded_status_pension_plan(beginning_plan_assets, beginning_PBO):
    """Function to calculate the funded status of a pension plan.
    The balance sheet presentation is as follows:
    balance sheet asset (liability) = funded status
    If the funded status is negative it is reported as a liability.
    IF the funded status is positive, it is reported as an asset subject to a ceiling of
    present value of future economic benefits(such as future refunds or reduced contributions)
    """
    
    beginning_year_funded_status_pension_plan =  beginning_plan_assets - beginning_PBO
    
    return beginning_year_funded_status_pension_plan

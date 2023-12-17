def calculate_dividendpayout_residual_dividend(debt_target, equity_target, debtcost_aftertax, retained_earningscost, equitycost, net_income, project_size, project_irr):
    
    """ Function to calculate the dividend to be paid under the residual dividend model. 
    Under this model, dividends are based on earnings less funds the firm retains to finance
    the equity portion of its capital budget. The model is based on the firms'1 1. investment opportunity schedule,
    2. target capital structure, and 3. access to and cost of external capital.
    These steps are followed to dettermine the target payout ratio (dividends per share / earnings per share):
    1. Identify optimal capital budget
    2. Determine the amount of equity needed to finance that capital budget for a given capital structure
    3 Meet equity requirements to the maximum extent possible with retained earnings.
    4. Pay dividends with the residual earnings that are available after the needs of the optimal capital budget are supported. In other words,
    the model implies that dividends are paid out of leftover earnings.
    
    Arguments:
    debt_target : target percentage of debt in the optimal capital structure
    equity_target : target percentage of equity in the optimal capital structure
    debtcost_aftertax : the after-tax cost of debt
    retained_earningscost: the cost of retained earnings
    equity_cost: the cost of equity
    net_income: net income
    project_size: a list of project sizes, in currency that outline for a particular investment opportunity schedule, the investment needed for each project
    project_irr: a list of internal rates of return for the projects in the investment opportunity schedule
    """
    # Calculate the weighted average cost of capital to identify a hurdle rate for investments (each irr must > wacc)
    # Under the pecking order theory, internally generate equity ie retained earnings is most favours and external equity least favoured
    # In this case, the equity proportion of the capital projects can be financed with retained earnings and as such, the cost of retained earnings is apt. rate to use
    wacc = (debt_target * debtcost_aftertax) + (equity_target * retained_earningscost)
    
    #Start the capital budget at 0
    capital_budget = 0
    
    # Identify which projects meet the hurdle rate and if so, include them in the capital budget
    for project_size, irr in zip(project_size,project_irr):
        if irr > wacc:
            capital_budget += project_size
    
    # Calculate the equity portion of the capital budget
    equity_portion_capitalbudget = capital_budget * equity_target
    
    #Calculate the amoount used for the capital budget
    equity_remaining = net_income - equity_portion_capitalbudget
    
    #Calculate the dividend payout ration
    dividend_payout_residual_dividend = equity_remaining / net_income
    
    return dividend_payout_residual_dividend


#Example usage
calculate_dividendpayout_residual_dividend(0.5,0.5,0.08,0.135,0.145,2500,[1000,1200,1200,1200,1000],[0.12,0.115,0.11,0.105,0.1])  

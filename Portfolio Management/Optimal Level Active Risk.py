def calculate_optimal_level_active_risk(information_ratio,sharpe_ratio_benchmark,risk_benchmark):
    
    """
    Function to calculate the optimal level of active risk for an unconstrained portfolio, which is the level of active risk
    that maximises the portfolio's Sharpe ratio
    """
    optimal_level_active_risk = (information_ratio/sharpe_ratio_benchmark)*risk_benchmark
    
    return optimal_level_active_risk

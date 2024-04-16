def calculate_sharpe_ratio_portfolio_optimal_active_risk(sharpe_ratio_benchmark,information_ratio):
    
    import numpy as np
    
    sharpe_ratio_portfolio_optimal_active_risk = np.sqrt((sharpe_ratio_benchmark)*2 + (information_ratio)*2)
    
    return sharpe_ratio_portfolio_optimal_active_risk

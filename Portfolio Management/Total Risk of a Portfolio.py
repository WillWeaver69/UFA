def calculate_total_risk_portfolio(benchmark_risk,active_risk):
    
    import numpy as np
    
    portfolio_risk_squared = ((benchmark_risk)*2 + (active_risk)*2)
    total_risk_portfolio = np.sqrt(portfolio_risk_squared)
    
    return total_risk_portfolio

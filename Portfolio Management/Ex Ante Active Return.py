 def calculate_ex_ante_active_return(portfolio_weights,portfolio_security_returns,benchmark_weights,benchmark_security_returns):
    
    #Calculate the expected return on the active portfolio
    expected_return_active_portfolio = sum(w * r for w, r in zip(portfolio_weights,portfolio_security_returns))
    
    #Calculate the expected return on the benchmark portfolio
    expected_return_benchmark_portfolio = sum(w* r for w, r in zip(benchmark_weights,benchmark_security_returns))
    
    
    return expected_return_active_portfolio - expected_return_benchmark_portfolio

#Example Usage
portfolio_weights =[0.45,0.3,0.25]
portfolio_security_returns=[0.11,0.06,0.14]
benchmark_weights=[0.4,0.3,0.3]
benchmark_security_returns=[0.12,0.05,0.12]

ex_ante_active_return = calculate_ex_ante_active_return(portfolio_weights,portfolio_security_returns,benchmark_weights,benchmark_security_returns)
print ("Expected Active Return:",ex_ante_active_return)

import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_simulation(simulation_function, n_simulations=1000, **kwargs):
    """
    Run a Monte Carlo simulation using a specified simulation function.
    """
    results = []
    for _ in range(n_simulations):
        result = simulation_function(**kwargs)
        results.append(result)
    
    return results

def investment_return_simulation(initial_investment, years, avg_return, std_dev):
    """
    Simulate the future value of an investment with random annual returns.
    """
    annual_returns = np.random.normal(avg_return, std_dev, years)
    end_balance = initial_investment

    for annual_return in annual_returns:
        end_balance *= (1 + annual_return)

    return end_balance

def output_simulation_statistics(simulation_results):
    """
    Output key statistics from the Monte Carlo simulation results.
    """
    mean_result = np.mean(simulation_results)
    median_result = np.median(simulation_results)
    min_result = np.min(simulation_results)
    max_result = np.max(simulation_results)
    percentile_25 = np.percentile(simulation_results, 25)
    percentile_75 = np.percentile(simulation_results, 75)

    print(f"Mean Final Balance: ${mean_result:,.2f}")
    print(f"Median Final Balance: ${median_result:,.2f}")
    print(f"Minimum Final Balance: ${min_result:,.2f}")
    print(f"Maximum Final Balance: ${max_result:,.2f}")
    print(f"25th Percentile: ${percentile_25:,.2f}")
    print(f"75th Percentile: ${percentile_75:,.2f}")

def plot_simulation_results(simulation_results):
    """
    Plot a histogram of the final balances from the Monte Carlo simulation results.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(simulation_results, bins=50, color='blue', alpha=0.7)
    plt.title('Histogram of Final Investment Balances')
    plt.xlabel('Final Balance')
    plt.ylabel('Frequency')
    plt.show()

# Example usage
n_simulations = 10000
initial_investment = 10000  # The amount of money you start with
years = 20                  # The duration of the investment in years
avg_return = 0.07           # The average annual return (e.g., 7%)
std_dev = 0.1               # The standard deviation of the annual return (e.g., 10%)

# Running the Monte Carlo simulation
simulation_results = monte_carlo_simulation(investment_return_simulation, n_simulations, 
                                            initial_investment=initial_investment, 
                                            years=years, 
                                            avg_return=avg_return, 
                                            std_dev=std_dev)

# Outputting the results and plotting the histogram
output_simulation_statistics(simulation_results)
plot_simulation_results(simulation_results)

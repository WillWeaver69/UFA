import numpy as np

def generate_bootstrap_samples(data, n_samples, seed=None):
    """
    Generate bootstrap samples from the original data.

    Parameters:
    data (array-like): Original dataset (numpy array or list).
    n_samples (int): Number of bootstrap samples to generate.
    seed (int, optional): Seed for the random number generator.

    Returns:
    numpy.ndarray: Array containing bootstrap samples.

    Theoretical Underpinning:
    Each bootstrap sample is created by randomly sampling with replacement
    from the original dataset. This process creates samples that are the same
    size as the original dataset but may contain duplicates.
    """
    rng = np.random.default_rng(seed)
    return rng.choice(data, size=(n_samples, len(data)), replace=True)

def calculate_statistic(bootstrap_samples, stat_func):
    """
    Apply a user-defined function to each bootstrap sample to calculate a statistic.

    Parameters:
    bootstrap_samples (numpy.ndarray): Array of bootstrap samples.
    stat_func (function): User-defined function to compute a statistic on each sample.

    Returns:
    numpy.ndarray: Array of calculated statistics for each bootstrap sample.

    Theoretical Underpinning:
    The user-defined function (stat_func) should be capable of taking a sample
    as input and returning a statistic. This function applies the stat_func to
    each bootstrap sample to compute the statistic of interest.
    """
    return np.array([stat_func(sample) for sample in bootstrap_samples])

def estimate_standard_error(statistics):
    """
    Estimate the standard error of the statistic of interest.

    Parameters:
    statistics (numpy.ndarray): Array of calculated statistics for each bootstrap sample.

    Returns:
    float: Estimated standard error of the statistics.

    Theoretical Underpinning:
    The standard error is estimated as the standard deviation of the 
    statistics calculated from the bootstrap samples. This provides a measure
    of the variability of the statistic across different samples.
    """
    return np.std(statistics, ddof=1)

def bootstrap(data, stat_func, n_samples=1000, seed=None):
    """
    Main function to perform the bootstrap process.

    Parameters:
    data (array-like): Original dataset (numpy array or list).
    stat_func (function): Function to compute the statistic of interest.
    n_samples (int, optional): Number of bootstrap samples to generate.
    seed (int, optional): Seed for the random number generator.

    Returns:
    float: Estimated standard error of the statistic.

    Theoretical Underpinning:
    This function integrates the bootstrap process by generating bootstrap
    samples, applying a statistic function on each sample, and then estimating
    the standard error of the computed statistics. It is a general-purpose
    function suitable for a wide range of statistical measures.
    """
    bootstrap_samples = generate_bootstrap_samples(data, n_samples, seed)
    statistics = calculate_statistic(bootstrap_samples, stat_func)
    return estimate_standard_error(statistics)

# Example usage
# Define a sample dataset and a statistic function (e.g., mean)
data = np.random.normal(size=100)  # Sample data
stat_func = np.mean              # Statistic function (mean in this case)

# Perform bootstrap
standard_error = bootstrap(data, stat_func)
print(f"Estimated Standard Error: {standard_error}")

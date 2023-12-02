import numpy as np

def calculate_risk_premium_ibbotson_chen(inflation_expected, real_growth_EPS_expected, changes_PE_ratio_expected, index_yield_expected, risk_free_expected):
    """
    Function to calculate the supply-side estimate of the equity risk premium using the Ibbotson-Chen model.
    Supports batch processing for multiple sets of inputs.

    Args:
    inflation_expected (float or np.array): Expected inflation.
    real_growth_EPS_expected (float or np.array): Expected real growth in earnings per share.
    changes_PE_ratio_expected (float or np.array): Expected changes in the price-to-earnings ratio.
    index_yield_expected (float or np.array): Expected yield on an index.
    risk_free_expected (float or np.array): Expected risk-free rate.

    Returns:
    np.array: Calculated equity risk premiums.

    Raises:
    ValueError: If any input is invalid.
    """

    # Convert inputs to numpy arrays for vectorized operations
    inflation = np.atleast_1d(inflation_expected)
    real_growth_EPS = np.atleast_1d(real_growth_EPS_expected)
    changes_PE_ratio = np.atleast_1d(changes_PE_ratio_expected)
    index_yield = np.atleast_1d(index_yield_expected)
    risk_free = np.atleast_1d(risk_free_expected)

    # Validate inputs
    if np.any(inflation < 0) or np.any(real_growth_EPS < 0) or np.any(index_yield < 0) or np.any(risk_free < 0):
        raise ValueError("Input values cannot be negative.")

    risk_premium = (1 + inflation) * (1 + real_growth_EPS) * (1 + changes_PE_ratio) - 1 + index_yield - risk_free
    return risk_premium

# Example usage
try:
    # For single calculation
    single_premium = calculate_risk_premium_ibbotson_chen(0.05, 0.07, -0.04, 0.08, 0.04)
    print(f"Single calculation risk premium: {single_premium[0]}")

    # For batch calculation
    inflation_rates = [0.03, 0.04, 0.05]
    growth_rates = [0.06, 0.07, 0.08]
    pe_changes = [-0.02, 0.00, 0.02]
    index_yields = [0.07, 0.08, 0.09]
    risk_free_rates = [0.03, 0.035, 0.04]

    batch_premiums = calculate_risk_premium_ibbotson_chen(inflation_rates, growth_rates, pe_changes, index_yields, risk_free_rates)
    print(f"Batch calculation risk premiums: {batch_premiums}")
except ValueError as e:
    print(f"Error: {e}")

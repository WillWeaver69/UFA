import numpy as np

def calculate_risk_premium_fama_french(risk_free, market_return, return_small, return_big, return_HBM, return_LBM, beta_mkt, beta_SMB, beta_HML):
    """
    Function to calculate the required return for a stock using the Fama-French three-factor model.
    Supports batch processing for multiple sets of inputs.

    Args:
    risk_free (float or np.array): Risk-free rate, typically annualized short-term government bond returns.
    market_return (float or np.array): Return on a value-weighted market index.
    return_small (float or np.array): Average return on small-cap portfolios.
    return_big (float or np.array): Average return on large-cap portfolios.
    return_HBM (float or np.array): Average return on high book-to-market portfolios.
    return_LBM (float or np.array): Average return on low book-to-market portfolios.
    beta_mkt (float or np.array): Factor sensitivity to the market return.
    beta_SMB (float or np.array): Factor sensitivity to the small-cap return premium.
    beta_HML (float or np.array): Factor sensitivity to the value return premium.

    Returns:
    np.array: Calculated risk premiums.

    Raises:
    ValueError: If any input is invalid.
    """

    # Convert inputs to numpy arrays for vectorized operations
    risk_free = np.atleast_1d(risk_free)
    market_return = np.atleast_1d(market_return)
    return_small = np.atleast_1d(return_small)
    return_big = np.atleast_1d(return_big)
    return_HBM = np.atleast_1d(return_HBM)
    return_LBM = np.atleast_1d(return_LBM)
    beta_mkt = np.atleast_1d(beta_mkt)
    beta_SMB = np.atleast_1d(beta_SMB)
    beta_HML = np.atleast_1d(beta_HML)

    # Validate inputs
    if np.any(beta_mkt < 0) or np.any(beta_SMB < 0) or np.any(beta_HML < 0):
        raise ValueError("Beta values cannot be negative.")

    risk_premium = risk_free + beta_mkt * (market_return - risk_free) + beta_SMB * (return_small - return_big) + beta_HML * (return_HBM - return_LBM)
    return risk_premium

# Example usage
try:
    # For single calculation
    single_premium = calculate_risk_premium_fama_french(0.03, 0.1, 0.12, 0.08, 0.15, 0.07, 1.2, 0.5, 0.3)
    print(f"Single calculation risk premium: {single_premium[0]}")

    # For batch calculation
    risk_free_rates = [0.03, 0.04]
    market_returns = [0.1, 0.11]
    return_smalls = [0.12, 0.13]
    return_bigs = [0.08, 0.09]
    return_HBMs = [0.15, 0.16]
    return_LBMs = [0.07, 0.08]
    beta_mkts = [1.2, 1.3]
    beta_SMBs = [0.5, 0.6]
    beta_HMLs = [0.3, 0.4]

    batch_premiums = calculate_risk_premium_fama_french(risk_free_rates, market_returns, return_smalls, return_bigs, return_HBMs, return_LBMs, beta_mkts, beta_SMBs, beta_HMLs)
    print(f"Batch calculation risk premiums: {batch_premiums}")
except ValueError as e:
    print(f"Error: {e}")

import numpy as np

def calculate_swap_spreads(swap_rates, treasury_yields, maturities):
    """
    Calculate the swap spreads for multiple swap rates, treasury yields, and maturities, in basis points.
    
    Args:
        swap_rates (list or np.ndarray): List or array of swap rates (%).
        treasury_yields (list or np.ndarray): List or array of treasury yields (%).
        maturities (list or np.ndarray): List or array of maturities (years).
    
    Returns:
        np.ndarray: Array of strings with swap spreads in basis points, rounded to 2 decimal places, 
                    followed by 'bps', and including the maturity.
    """
    # Convert inputs to NumPy arrays for vectorized operations
    swap_rates = np.array(swap_rates)
    treasury_yields = np.array(treasury_yields)
    maturities = np.array(maturities)

    # Calculate swap spreads
    swap_spreads_basis = (swap_rates - treasury_yields) * 10000
    swap_spreads_basis = np.round(swap_spreads_basis, 2)

    # Format results with maturity
    results = np.core.defchararray.add(swap_spreads_basis.astype(str), " bps, Maturity: ")
    results = np.core.defchararray.add(results, maturities.astype(str))
    results = np.core.defchararray.add(results, " years")

    return results

# Example usage with lists of data
swap_rates = [0.0202, 0.025]
treasury_yields = [0.0161, 0.02]
maturities = [2, 5]

result = calculate_swap_spreads(swap_rates, treasury_yields, maturities)
print(result)

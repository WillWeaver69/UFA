import numpy as np

def calculate_i_spreads(risky_bond_yields, swap_rates, maturities):
    """
    Calculate the i-spreads for multiple risky bond yields, swap rates, and maturities, in basis points.
    
    Args:
        risky_bond_yields (list or np.ndarray): List or array of bond yieldds (%).
        swap_rates (list or np.ndarray): List or array of swap rates (%).
        maturities (list or np.ndarray): List or array of maturities (years).
    
    Returns:
        np.ndarray: Array of strings with swap spreads in basis points, rounded to 2 decimal places, 
                    followed by 'bps', and including the maturity.
    """
    # Convert inputs to NumPy arrays for vectorized operations
    risky_bond_yields = np.array(risky_bond_yields)
    swap_rates = np.array(swap_rates)
    maturities = np.array(maturities)

    # Calculate  i-spreads
    i_spreads_basis = (risky_bond_yields - swap_rates) * 10000
    i_spreads_basis = np.round(i_spreads_basis, 2)

    # Format results with maturity
    results = np.core.defchararray.add(i_spreads_basis.astype(str), " bps, Maturity: ")
    results = np.core.defchararray.add(results, maturities.astype(str))
    results = np.core.defchararray.add(results, " years")

    return results

# Example usage with lists of data
risky_bond_yields = [0.0202, 0.025]
swap_rates = [0.0161, 0.02]
maturities = [2, 5]

result = calculate_i_spreads(risky_bond_yields, swap_rates, maturities)
print(result)

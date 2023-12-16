def calculate_beta_nonpublic_company(beta_comparable, debt_comparable, equity_comparable, debt, equity):
    """
    Calculate the beta of a non-public company based on the beta of a comparable public company.

    Parameters:
    beta_comparable (float): Beta of the comparable public company.
    debt_comparable (float): Debt of the comparable public company.
    equity_comparable (float): Equity of the comparable public company.
    debt (float): Debt of the target non-public company.
    equity (float): Equity of the target non-public company.

    Returns:
    float: Estimated beta for the target non-public company.

    Raises:
    ValueError: If any of the financial inputs are negative.

    Example:
    >>> calculate_beta_nonpublic_company(1.2, 5000000, 2000000, 1000000, 55000000)
    0.34909090909090906
    """
    # Validate inputs
    if any(x < 0 for x in [beta_comparable, debt_comparable, equity_comparable, debt, equity]):
        raise ValueError("Financial inputs should not be negative.")

    try:
        # Unlever the beta of the comparable company
        unlevered_beta = beta_comparable / (1 + (debt_comparable / equity_comparable))
        
        # Re-lever the beta for the target company
        beta_target = unlevered_beta * (1 + (debt / equity))
        return beta_target
    except ZeroDivisionError:
        raise ValueError("Equity values must not be zero.")

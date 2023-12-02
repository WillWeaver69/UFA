def calculate_wacc_private(cost_of_equity, cost_of_debt, value_equity, value_debt, tax_rate):
    total_value = value_equity + value_debt
    weight_of_equity = value_equity / total_value
    weight_of_debt = value_debt / total_value
    after_tax_cost_of_debt = cost_of_debt * (1 - tax_rate)

    wacc = (weight_of_equity * cost_of_equity) + (weight_of_debt * after_tax_cost_of_debt)
    return wacc

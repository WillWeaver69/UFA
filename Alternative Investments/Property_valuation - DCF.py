import numpy_financial as npf

class PropertyValuationDCF:
    """
    A class to estimate the value of a property using the Discounted Cash Flow (DCF) method,
    incorporating terminal value.

    Attributes:
    projected_cash_flows (list of floats): The projected annual cash flows from the property.
    discount_rate (float): The annual discount rate used in the DCF calculation.

    Methods:
    calculate_present_value(): Calculates the present value of the projected cash flows and terminal value.
    """

    def __init__(self, projected_cash_flows, discount_rate):
        """
        Initializes the PropertyValuationDCF object with projected cash flows and discount rate.

        Parameters:
        projected_cash_flows (list of floats): The projected annual cash flows from the property.
        discount_rate (float): The discount rate to be used in the DCF calculation.
        """
        self.projected_cash_flows = projected_cash_flows
        self.discount_rate = discount_rate

    def calculate_present_value(self, growth_rate=None, exit_multiple=None):
        """
        Calculates the present value of the projected cash flows using the discount rate,
        including the terminal value calculated either by perpetuity growth model or exit multiple.

        Parameters:
        growth_rate (float): The perpetual growth rate used for terminal value calculation (optional).
        exit_multiple (float): The exit multiple used for terminal value calculation (optional).

        Returns:
        float: The present value of the projected cash flows and terminal value.

        Raises:
        ValueError: If neither a growth rate nor an exit multiple is provided for the terminal value calculation.
        """
        if growth_rate is not None:
            # Perpetuity Growth Model
            terminal_value = self.projected_cash_flows[-1] * (1 + growth_rate) / (self.discount_rate - growth_rate)
        elif exit_multiple is not None:
            # Exit Multiple Method
            terminal_value = self.projected_cash_flows[-1] * exit_multiple
        else:
            raise ValueError("Either growth_rate or exit_multiple must be provided for terminal value calculation.")

        cash_flows_with_terminal = self.projected_cash_flows + [terminal_value]
        present_value = npf.npv(self.discount_rate, cash_flows_with_terminal)
        return present_value

# Example usage
projected_cash_flows = [50000, 52000, 54040, 56121, 58246]  # Example cash flows for 5 years
discount_rate = 0.08  # 8% discount rate
growth_rate = 0.02  # 2% growth rate for terminal value
# Or use an exit multiple, e.g., exit_multiple = 10

valuation_tool = PropertyValuationDCF(projected_cash_flows, discount_rate)
property_value = valuation_tool.calculate_present_value(growth_rate=growth_rate)
# Or use exit_multiple, e.g., property_value = valuation_tool.calculate_present_value(exit_multiple=exit_multiple)
print("Estimated Property Value: ", property_value)


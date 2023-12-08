class PropertyValuation:
    """
    A class to estimate the value of a property using the direct capitalization method.

    The valuation is based on Net Operating Income (NOI) and a capitalization rate. NOI is calculated 
    by subtracting operating expenses and vacancy losses from the potential gross income of the property.

    Attributes:
    property_size (float): The size of the property in square feet.
    rental_income_per_sqft (float): The gross rental income per square foot.
    other_income (float): Income from other sources, such as parking fees or service charges.
    operating_expenses (dict): A dictionary to store various operating expenses.

    Methods:
    add_operating_expense(expense_name, amount): Adds an operating expense to the dictionary.
    calculate_NOI(vacancy_loss_percent): Calculates NOI based on vacancy loss and operating expenses.
    estimate_property_value(cap_rate): Estimates the property value using NOI and the capitalization rate.
    """

    def __init__(self, property_size, rental_income_per_sqft, other_income):
        """
        Initializes the PropertyValuation object with basic property details.

        Parameters:
        property_size (float): Size of the property in square feet.
        rental_income_per_sqft (float): Gross rental income per square foot.
        other_income (float): Additional income sources.
        """
        self.property_size = property_size
        self.rental_income_per_sqft = rental_income_per_sqft
        self.other_income = other_income
        self.operating_expenses = {}

    def add_operating_expense(self, expense_name, amount):
        """
        Adds an operating expense to the property.

        Parameters:
        expense_name (str): The name of the operating expense (e.g., 'property_taxes').
        amount (float): The amount of the expense.
        """
        self.operating_expenses[expense_name] = amount

    def calculate_NOI(self, vacancy_loss_percent):
        """
        Calculates the Net Operating Income (NOI) of the property.

        NOI is computed as the effective gross income (potential gross income minus vacancy loss)
        minus the total operating expenses.

        Parameters:
        vacancy_loss_percent (float): The percentage of potential gross income lost due to vacancies.

        Returns:
        float: The calculated NOI.
        """
        potential_gross_income = (self.property_size * self.rental_income_per_sqft) + self.other_income
        effective_gross_income = potential_gross_income * (1 - vacancy_loss_percent / 100)
        total_operating_expenses = sum(self.operating_expenses.values())
        return effective_gross_income - total_operating_expenses

    def estimate_property_value(self, cap_rate):
        """
        Estimates the property value using the direct capitalization method.

        The method divides the NOI by the capitalization rate (expressed as a percentage) to estimate
        the property's value.

        Parameters:
        cap_rate (float): The capitalization rate used for valuation, expressed as a percentage.

        Returns:
        float: The estimated value of the property.

        Raises:
        ValueError: If the capitalization rate is non-positive.
        """
        if cap_rate <= 0:
            raise ValueError("Capitalization rate must be positive.")
        noi = self.calculate_NOI(vacancy_loss_percent=10)  # Default or adjustable vacancy loss
        return noi / (cap_rate / 100)

# Example usage
valuation_tool = PropertyValuation(10000, 25, 5000)
valuation_tool.add_operating_expense('property_taxes', 5000)
valuation_tool.add_operating_expense('insurance', 2000)
valuation_tool.add_operating_expense('utilities', 3000)
valuation_tool.add_operating_expense('maintenance', 4000)

try:
    estimated_value = valuation_tool.estimate_property_value(5)
    print("Estimated Property Value: ", estimated_value)
except ValueError as e:
    print(e)

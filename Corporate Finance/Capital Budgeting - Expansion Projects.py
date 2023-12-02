def capital_budgeting_expand():
    """
    This function encapsulates the entire capital budgeting process including 
    getting user inputs, calculating cash flows, and discounting those cash flows 
    to calculate the Net Present Value (NPV) of a project.
    """
    import pandas as pd
    import matplotlib.pyplot as plt

    def input_positive_number(prompt):
        """
        Asks the user for a positive number input.
        Parameters:
            prompt (str): The message displayed to the user.
        Returns:
            float: A positive number input by the user.
        """
        while True:
            try:
                value = float(input(prompt))
                if value < 0:
                    raise ValueError("The value must be positive.")
                return value
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def input_number_in_range(prompt, min_value=0, max_value=100):
        """
        Asks the user for input and validates that it is a number within the given range [min_value, max_value].
        Parameters:
            prompt (str): The message displayed to the user.
            min_value (float): The minimum acceptable value.
            max_value (float): The maximum acceptable value.
        Returns:
            float: A number within the specified range input by the user.
        """
        while True:
            try:
                value = float(input(prompt))
                if not min_value <= value <= max_value:
                    raise ValueError(f"The value must be between {min_value} and {max_value}.")
                return value
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def get_user_input():
        """
        Prompts the user for all of the inputs required to calculate the NPV of a project
        and validates the input to ensure that they are correct numeric values.
        Returns:
            user_input (dict): A dictionary containing all the validated user inputs.
        """
        user_input = {
            "years": int(input_positive_number("For how long, (in years), will the proposed project generate cash flows? ")),
            "capex_items": int(input_positive_number("How many distinct pieces of capital expenditure will be required for the project? ")),
            "tax_rate": input_number_in_range("Insert tax rate (0-100) %: ") / 100,
            "cost_of_capital": input_number_in_range("Insert cost of capital (0-100) %: ") / 100,
            "nwc_investment": input_positive_number("Insert net working capital investment: "),
            "sales": input_positive_number("Insert annual sales amount: "),
            "fixed_costs": input_positive_number("Insert fixed annual costs: "),
            "variable_costs_percentage": input_positive_number("Insert variable costs as a percentage of sales: ") / 100
        }

        user_input["capex"] = [input_positive_number(f"Insert amount of Capex for item {i + 1}: ") for i in range(user_input["capex_items"])]
        user_input["depreciation"] = [input_positive_number(f"Insert annual depreciation for year {i + 1}: ") for i in range(user_input["years"])]
        user_input["salvage_value"] = [input_positive_number(f"Insert salvage value for item {i + 1}: ") for i in range(user_input["capex_items"])]
        user_input["book_value"] = [input_positive_number(f"Insert book value for item {i + 1}: ") for i in range(user_input["capex_items"])]

        return user_input

    def calculate_cash_flows(user_input):
        """
        Calculates the annual cash flows and the terminal net operating cash flow (TNOCF)
        for the project based on user inputs.
        Parameters:
            user_input (dict): The dictionary containing all user inputs.
        Returns:
            List[float]: A list of cash flows including initial outlay and TNOCF.
        """
        FCInv = sum(user_input['capex'])
        NWCInv = user_input["nwc_investment"]
        Initial_outlay = FCInv + NWCInv
        S = user_input["sales"]
        Variable_costs = S * user_input["variable_costs_percentage"]
        C = user_input["fixed_costs"] + Variable_costs
        D = user_input["depreciation"]
        T = user_input["tax_rate"]

        Cash_flows = [(S - C) * (1 - T) + (D[year] * T) for year in range(user_input["years"])]

        Salvage_value_total = sum(user_input["salvage_value"])
        Book_value_total = sum(user_input["book_value"])
        TNOCF = Salvage_value_total + NWCInv - (T * (Salvage_value_total - Book_value_total))

        Cash_flows[-1] += TNOCF
        Cash_flows.insert(0, -Initial_outlay)

        return Cash_flows
    
    def cash_flow_table(Cash_flows):
        """
        Creates a dataframe to hold the cash flows calculated elsewhere
        Parameters:
            cash_flows (List[float]): The list of cash flows from the project.

        Returns:
            Dataframe: Dataframe holding cash flows
        """
        import pandas as pd
        import matplotlib.pyplot as plt

        # Creating a DataFrame starting from year 0
        df = pd.DataFrame({'Year': range(0, len(Cash_flows)), 'Cash Flow': Cash_flows})

        # Calculate cumulative cash flows
        df['Cumulative Cash Flow'] = df['Cash Flow'].cumsum()

        # Plotting
        plt.figure(figsize=(12, 6))

        # Plotting individual cash flows
        plt.bar(df['Year'], df['Cash Flow'], color='blue', label='Annual Cash Flow')

        # Plotting cumulative cash flows
        plt.plot(df['Year'], df['Cumulative Cash Flow'], color='red', marker='o', linestyle='-', label='Cumulative Cash Flow')

        # Adding labels and title
        plt.title('Cash Flows Over Time')
        plt.xlabel('Year')
        plt.ylabel('Amount')
        plt.xticks(df['Year'])  # Set x-ticks to be each year
        plt.grid(True)

        # Adding a legend
        plt.legend()

        # Display the plot
        plt.show()

        return df


        
        

    def discount_cash_flows(cash_flows, cost_of_capital):
        """
        Discounts the calculated cash flows to their present value and calculates
        the Net Present Value (NPV) of the project.
        Parameters:
            cash_flows (List[float]): The list of cash flows from the project.
            cost_of_capital (float): The cost of capital rate.
        Returns:
            float: The Net Present Value (NPV) of the project.
        """
        discounted_cash_flows = [cash_flow / ((1 + cost_of_capital) ** index) for index, cash_flow in enumerate(cash_flows)]
        return sum(discounted_cash_flows)

    # Main execution starts here
    user_input = get_user_input()
    cash_flows = calculate_cash_flows(user_input)
    net_present_value = discount_cash_flows(cash_flows, user_input['cost_of_capital'])
    
    cash_flow_table(cash_flows)

    print(f"The Net Present Value (NPV) of the project is: {net_present_value:.2f}")

    return net_present_value

# Call the main function to run the capital budgeting process
capital_budgeting_expand()

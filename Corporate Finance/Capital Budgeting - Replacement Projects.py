def capital_budgeting_replace():
    """
    This function encapsulates the entire capital budgeting process for a replacement project including 
    getting user inputs, calculating cash flows, and discounting those cash flows 
    to calculate the Net Present Value (NPV) of a project.
    """

    def input_positive_number(prompt):
        """
        Asks the user for a positive number input.
        """
        while True:
            try:
                value = float(input(prompt))
                if value < 0:
                    raise ValueError("The value must be positive.")
                print(f"Input received for {prompt}: {value}")
                return value
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def input_number(prompt):
        """
        Asks the user for a number input which can be negative.
        """
        while True:
            try:
                value = float(input(prompt))
                print(f"Input received for {prompt}: {value}")
                return value
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def input_number_in_range(prompt, min_value=0, max_value=100):
        """
        Asks the user for input and validates that it is a number within the given range [min_value, max_value].
        """
        while True:
            try:
                value = float(input(prompt))
                if not min_value <= value <= max_value:
                    raise ValueError(f"The value must be between {min_value} and {max_value}.")
                print(f"Input received for {prompt}: {value}")
                return value
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def get_user_input():
        """
        Prompts the user for all of the inputs required to calculate the NPV of a replacement project
        and validates the input to ensure that they are correct numeric values.
        """
        print("Getting user inputs...")
        user_input = {
            "years": int(input_positive_number("For how long, (in years), will the proposed replacement project generate cash flows? ")),
            "capex_items": int(input_positive_number("How many distinct pieces of capital expenditure will be required for the project? ")),
            "tax_rate": input_number_in_range("Insert tax rate (0-100) %: ", 0, 100) / 100,
            "cost_of_capital": input_number_in_range("Insert cost of capital (0-100) %: ", 0, 100) / 100,
            "salvage_old_now": input_positive_number("What is the market value of the existing asset now? "),
            "salvage_old_years": input_positive_number("What would be the market value of the existing asset at the end of the replacement project lifespan? "),
            "book_old_years": input_positive_number("What would be the book value of the existing asset at the end of the replacement project lifespan? "),
            "book_old": input_positive_number("What is the book value of the existing asset now? "),
            "nwc_investment": input_positive_number("Insert net working capital investment: "),
            "sales_change": input_number("Insert increase/(decrease) in sales: "),
            "operating_costs_change": input_number("Insert increase/(decrease) in operating costs: "),
        }

        # Collecting additional inputs based on the number of capex items and years
        user_input["capex"] = [input_positive_number(f"Insert amount of Capex for item {i + 1}: ") for i in range(user_input["capex_items"])]
        user_input["depreciation_old"] = [input_positive_number(f"Insert annual depreciation for the existing asset for year {i + 1}: ") for i in range(user_input["years"])]
        user_input["depreciation_new"] = [input_positive_number(f"Insert annual depreciation for the new asset for year {i + 1}: ") for i in range(user_input["years"])]
        user_input["salvage_value_new"] = [input_positive_number(f"Insert salvage value for new item {i + 1} at the end of the project: ") for i in range(user_input["capex_items"])]
        user_input["book_value_new"] = [input_positive_number(f"Insert book value for new item {i + 1} at the end of the project: ") for i in range(user_input["capex_items"])]
        
        
        return user_input

    def calculate_cash_flows(user_input):
        """
        Calculates the annual cash flows and the terminal net operating cash flow (TNOCF)
        for the project based on user inputs.
        """
       
        FCInv = sum(user_input['capex'])
        NWCInv = user_input["nwc_investment"]
        S_old_now = user_input["salvage_old_now"]
        S_old_years = user_input["salvage_old_years"]
        B_old = user_input["book_old"]
        B_old_years = user_input["book_old_years"]
        IncrementalSales = user_input["sales_change"]
        IncrementalCosts = user_input["operating_costs_change"]
        D_old = user_input["depreciation_old"]
        D_new = user_input["depreciation_new"]
        Incremental_depreciation = [D_new[year] - D_old[year] for year in range(user_input["years"])]
        T = user_input["tax_rate"]
        
        Initial_outlay = FCInv + NWCInv - S_old_now + (T * (S_old_now - B_old))
        
        
        Incremental_Cash_flows = [(IncrementalSales - IncrementalCosts) * (1 - T) + (Incremental_depreciation[year] * T) for year in range(user_input["years"])]
        
        
        Salvage_value_new_total = sum(user_input["salvage_value_new"])
        Book_value_new_total = sum(user_input["book_value_new"])
        TNOCF = (Salvage_value_new_total - S_old_years) + NWCInv - (T * (Salvage_value_new_total - Book_value_new_total) + (S_old_years - B_old_years))
        
        
        Incremental_Cash_flows[-1] += TNOCF
        Incremental_Cash_flows.insert(0, -Initial_outlay)
        
        
        return Incremental_Cash_flows

    def discount_cash_flows(Incremental_Cash_flows, cost_of_capital):
        """
        Discounts the calculated incremental cash flows to their present value and calculates
        the Net Present Value (NPV) of the project.
        """

        discounted_cash_flows = [cash_flow / ((1 + cost_of_capital) ** index) for index, cash_flow in enumerate(Incremental_Cash_flows)]
        NPV = sum(discounted_cash_flows)
        
        print(f"Net Present Value (NPV) calculated: {NPV}")
        return NPV

    # Main execution starts here
    user_input = get_user_input()
    cash_flows = calculate_cash_flows(user_input)
    net_present_value = discount_cash_flows(cash_flows, user_input['cost_of_capital'])

    print(f"The Net Present Value (NPV) of the project is: {net_present_value:.2f}")

    return net_present_value

# Call the main function to run the capital budgeting process
capital_budgeting_replace()

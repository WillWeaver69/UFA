import pandas as pd

class BaseRevenueModel:
    """
    Attributes:
        time_frame (int): Number of years for the revenue projection.
        revenue_components (list): List to hold different types of revenue components.
    """

    def __init__(self, time_frame):
        """
        Initializes the revenue model with a specified time frame.

        Args:
            time_frame (int): Number of years to project the revenue.
        """
        self.time_frame = time_frame
        self.revenue_components = []

    def add_revenue_type(self, revenue_type):
        """
        Adds a new type of revenue to the model.

        Args:
            revenue_type (object): An instance of a revenue type class.
        """
        self.revenue_components.append(revenue_type)
        
    
    def add_sga_costs(self, sga_costs):
        self.sga_costs = sga_costs

    # Method to calculate overall costs (including SG&A)
    def calculate_overall_costs(self, time_frame):
        # Assuming other costs calculation methods are defined
        sga_costs = self.sga_costs.calculate_total_sga_costs(time_frame)
        # Combine with other costs...
        return combined_costs


        
        
class SubscriptionType:
    """
    Represents a specific type of subscription, holding its pricing, subscriber details, and costs.

    Attributes:
        name (str): Name of the subscription type.
        monthly_fee (float): Monthly fee for this subscription type.
        subscribers (int): Initial number of subscribers.
        churn_rate (float): Expected churn rate (percentage as a decimal).
        growth_rate_drivers (list): List of dictionaries containing growth rate factors per year.
        data_center_cost (float): Monthly cost of data center space.
        software_costs (dict): Monthly costs for software licenses.
        sales_commission_rate (float): Sales commission rate as a percentage.
    """

    def __init__(self, name, monthly_fee, initial_subscribers, churn_rate, growth_rate_drivers, data_center_cost, software_costs, sales_commission_rate):
        self.name = name
        self.monthly_fee = monthly_fee
        self.subscribers = initial_subscribers
        self.churn_rate = churn_rate
        self.growth_rate_drivers = growth_rate_drivers
        self.data_center_cost = data_center_cost
        self.software_costs = software_costs
        self.sales_commission_rate = sales_commission_rate

    def calculate_yearly_growth_rate(self, year_drivers):
        """
        Calculates the growth rate for a year based on provided drivers.

        Args:
            year_drivers (dict): A dictionary containing growth rate drivers for a year.

        Returns:
            float: Calculated growth rate for the year.
        """
        growth_rate = year_drivers["base_growth"] + year_drivers.get("marketing_impact", 0)
        return growth_rate

    def calculate_revenues(self, time_frame):
        """
        Calculates the yearly revenues for this subscription type over the specified time frame.

        Args:
            time_frame (int): Number of years for the revenue projection.

        Returns:
            list: List of revenues for each year.
        """
        yearly_revenues = []
        subscribers = self.subscribers

        for year in range(time_frame):
            if year > 0:
                year_drivers = self.growth_rate_drivers[year - 1] if year - 1 < len(self.growth_rate_drivers) else self.growth_rate_drivers[-1]
                growth_rate = self.calculate_yearly_growth_rate(year_drivers)
                subscribers = subscribers * (1 - self.churn_rate) * (1 + growth_rate)
            revenue = self.monthly_fee * subscribers * 12
            yearly_revenues.append(revenue)

        return yearly_revenues

    def calculate_subscription_costs(self, time_frame):
        """
        Calculates the subscription costs over the specified time frame.

        Args:
            time_frame (int): Number of years for the cost projection.

        Returns:
            list: List of costs for each year.
        """
        yearly_costs = []
        subscribers = self.subscribers

        for year in range(time_frame):
            if year > 0:
                year_drivers = self.growth_rate_drivers[year - 1] if year - 1 < len(self.growth_rate_drivers) else self.growth_rate_drivers[-1]
                growth_rate = self.calculate_yearly_growth_rate(year_drivers)
                subscribers = subscribers * (1 - self.churn_rate) * (1 + growth_rate)
            
            # Calculating total software costs
            total_software_cost = sum([cost for cost in self.software_costs.values()])

            # Calculating sales commission
            sales_commission = self.monthly_fee * subscribers * 12 * self.sales_commission_rate

            # Summing up all costs
            total_cost = self.data_center_cost * 12 + total_software_cost * 12 + sales_commission
            yearly_costs.append(total_cost)

        return yearly_costs

    # Add other methods if necessary


    def component_details(self, time_frame):
        subscriber_counts = [self.subscribers]
        growth_rates = [0]  # No growth in the first year
        churn_rates = [self.churn_rate for _ in range(time_frame)]

        for year in range(1, time_frame):
            year_drivers = self.growth_rate_drivers[year - 1] if year - 1 < len(self.growth_rate_drivers) else self.growth_rate_drivers[-1]
            growth_rate = self.calculate_yearly_growth_rate(year_drivers)
            growth_rates.append(growth_rate)
            subscribers = subscriber_counts[-1] * (1 - self.churn_rate) * (1 + growth_rate)
            subscriber_counts.append(subscribers)

        monthly_fees = [self.monthly_fee for _ in range(time_frame)]
        revenue_subtotal = self.calculate_revenues(time_frame)
        formatted_growth_rates = ["{:.2%}".format(rate) for rate in growth_rates]
        formatted_churn_rates = ["{:.2%}".format(rate) for rate in churn_rates]
        formatted_revenue_subtotal = ["${:<14,.2f}".format(revenue) for revenue in revenue_subtotal]
        return {
            "Monthly Fee": monthly_fees,
            "Subscribers": subscriber_counts, 
            "Churn Rate": formatted_churn_rates, 
            "Growth Rate": formatted_growth_rates,
            "Revenue Subtotal": formatted_revenue_subtotal
        }

class SubscriptionRevenue:
    name = "Subscription"

    def __init__(self, subscription_types, subscription_costs):
        self.subscription_types = subscription_types
        self.subscription_costs = subscription_costs

    def calculate_yearly_revenues(self, time_frame):
        total_yearly_revenues = [0] * time_frame
        for sub_type in self.subscription_types:
            yearly_revenues = sub_type.calculate_revenues(time_frame)
            total_yearly_revenues = [total + year_revenue for total, year_revenue in zip(total_yearly_revenues, yearly_revenues)]
        return total_yearly_revenues

    def component_details(self, time_frame):
        details = {}
        for sub_type in self.subscription_types:
            sub_details = sub_type.component_details(time_frame)
            for key, value in sub_details.items():
                details[f"{sub_type.name} {key}"] = value
        return details



class ProductType:
    """
    Represents a specific type of product, holding its pricing and sales details.

    Attributes:
        name (str): Name of the product type.
        unit_price (float): Price per unit of this product type.
        initial_volume (int): Initial sales volume.
        growth_rate (float): Expected growth rate (percentage as a decimal).
    """

    def __init__(self, name, unit_price, initial_volume, growth_rate):
        """
        Initializes a product type with its details.

        Args:
            name (str): Name of the product type.
            unit_price (float): Price per unit of this product type.
            initial_volume (int): Initial sales volume.
            growth_rate (float): Growth rate (as a decimal).
        """
        self.name = name
        self.unit_price = unit_price
        self.volume = initial_volume
        self.growth_rate = growth_rate

    def calculate_yearly_revenues(self, time_frame):
        """
        Calculates the yearly revenues for this product type over the specified time frame.

        Args:
            time_frame (int): Number of years for the revenue projection.

        Returns:
            list: List of revenues for each year.
        """
        yearly_revenues = []
        volume = self.volume

        for year in range(time_frame):
            revenue = self.unit_price * volume
            yearly_revenues.append(revenue)
            volume *= (1 + self.growth_rate)

        return yearly_revenues
    
    def calculate_yearly_volumes(self, time_frame):
        yearly_volumes = []
        volume = self.volume  # Assuming self.volume is initialized as an integer or float

        for year in range(time_frame):
            yearly_volumes.append(volume)
            volume *= (1 + self.growth_rate)

        return yearly_volumes

    def component_details(self, time_frame):
        """
        Generates detailed information about the product type over the specified time frame.

        Args:
            time_frame (int): Number of years for the revenue projection.

        Returns:
            dict: Detailed information including unit price, volume, and growth rate for each year.
        """
        unit_prices = [self.unit_price for _ in range(time_frame)]
        volumes = [self.volume * (1 + self.growth_rate) ** year for year in range(time_frame)]
        growth_rates = [self.growth_rate for _ in range(time_frame)]
        formatted_growth_rates = ["{:.2%}".format(rate) for rate in growth_rates]
        
        return {
            "Unit Price": unit_prices,
            "Volume": volumes,
            "Growth Rate": formatted_growth_rates
        }
    
class ProductCost:
    """
    Represents the cost structure for a specific type of product.

    Attributes:
        name (str): Name of the product type.
        material_costs (list of MaterialCost): List of material costs for the product.
        labor_cost_per_unit (float): Labor cost per unit produced.
        overhead_cost_per_unit (float): Overhead cost per unit produced.
    """

    def __init__(self, name, material_costs, labor_cost_per_unit, overhead_cost_per_unit):
        self.name = name
        self.material_costs = material_costs
        self.labor_cost_per_unit = labor_cost_per_unit
        self.overhead_cost_per_unit = overhead_cost_per_unit

    def calculate_total_cost_per_unit(self):
        """
        Calculates the total cost per unit for this product type.

        Returns:
            float: Total cost per unit.
        """
        total_material_cost = sum(material_cost.calculate_cost() for material_cost in self.material_costs)
        return total_material_cost + self.labor_cost_per_unit + self.overhead_cost_per_unit



  

        
    
class MaterialCost:
    """
    Represents the cost of a specific material used in a product.

    Attributes:
        name (str): Name of the material.
        cost_per_unit (float): Cost per unit of the material.
        units_needed_per_product (float): Units of the material needed per product unit.
    """

    def __init__(self, name, cost_per_unit, units_needed_per_product):
        self.name = name
        self.cost_per_unit = cost_per_unit
        self.units_needed_per_product = units_needed_per_product

    def calculate_cost(self):
        """
        Calculates the total cost of this material for one unit of product.

        Returns:
            float: Total material cost for one unit of product.
        """
        return self.cost_per_unit * self.units_needed_per_product

class ProductCostStructure:
    """
    Represents the cost structure for a specific type of product.

    Attributes:
        material_costs (list of MaterialCost): List of material costs for the product.
        labor_cost_per_unit (float): Labor cost per unit produced.
        overhead_cost_per_unit (float): Overhead cost per unit produced.
    """

    def __init__(self, material_costs, labor_cost_per_unit, overhead_cost_per_unit):
        self.material_costs = [MaterialCost(*mc) for mc in material_costs]
        self.labor_cost_per_unit = labor_cost_per_unit
        self.overhead_cost_per_unit = overhead_cost_per_unit

    def calculate_total_cost_per_unit(self):
        """
        Calculates the total cost per unit for this product type.

        Returns:
            float: Total cost per unit.
        """
        total_material_cost = sum([mc.calculate_cost() for mc in self.material_costs])
        return total_material_cost + self.labor_cost_per_unit + self.overhead_cost_per_unit

class ProductSalesRevenue:
    """
    Represents the total revenue and cost generated from all product types.

    Attributes:
        product_types (list): List of ProductType instances.
        product_costs (list): List of ProductCost instances.
    """

    name = "Product Sales"

    def __init__(self, product_types, product_costs):
        self.product_types = product_types
        self.product_costs = product_costs

    def calculate_yearly_revenues(self, time_frame):
        """
        Calculates the total yearly revenues for all product types over the specified time frame.

        Args:
            time_frame (int): Number of years for the revenue projection.

        Returns:
            dict: Total yearly revenues for all product types and subtotals for each product type.
        """
        total_yearly_revenues = [0] * time_frame
        product_subtotals = {prod_type.name: [0] * time_frame for prod_type in self.product_types}

        for prod_type in self.product_types:
            yearly_revenues = prod_type.calculate_yearly_revenues(time_frame)
            product_subtotals[prod_type.name] = yearly_revenues
            total_yearly_revenues = [total + year_revenue for total, year_revenue in zip(total_yearly_revenues, yearly_revenues)]

        return total_yearly_revenues, product_subtotals

    def calculate_yearly_costs(self, time_frame):
        """
        Calculates the total yearly costs for all product types over the specified time frame.

        Args:
            time_frame (int): Number of years for the cost projection.

        Returns:
            dict: Total yearly costs for all product types and subtotals for each product type.
        """
        total_yearly_costs = [0] * time_frame
        product_cost_subtotals = {prod_cost.name: [0] * time_frame for prod_cost in self.product_costs}

        for prod_cost in self.product_costs:
            total_cost_per_unit = prod_cost.calculate_total_cost_per_unit()
            for prod_type in self.product_types:
                if prod_cost.name == prod_type.name:
                    yearly_volumes = [volume for volume in prod_type.calculate_yearly_volumes(time_frame)]
                    yearly_costs = [total_cost_per_unit * volume for volume in yearly_volumes]
                    product_cost_subtotals[prod_cost.name] = yearly_costs
                    total_yearly_costs = [total + year_cost for total, year_cost in zip(total_yearly_costs, yearly_costs)]

        return total_yearly_costs, product_cost_subtotals

    def component_details(self, time_frame):
        """
        Generates detailed information about each product type over the specified time frame, including revenues and costs.

        Args:
            time_frame (int): Number of years for the revenue and cost projection.

        Returns:
            dict: Consolidated details from each product type, including subtotals for revenues and costs.
        """
        details = {}
        total_revenues, revenue_subtotals = self.calculate_yearly_revenues(time_frame)
        total_costs, cost_subtotals = self.calculate_yearly_costs(time_frame)

        for prod_type in self.product_types:
            prod_details = prod_type.component_details(time_frame)
            for key, value in prod_details.items():
                details[f"{prod_type.name} {key}"] = value

            # Add revenue and cost subtotals for each product type
            details[f"{prod_type.name} Revenue Subtotal"] = revenue_subtotals[prod_type.name]
            details[f"{prod_type.name} Cost Subtotal"] = cost_subtotals[prod_type.name]

        return details

    
    
class ConsultingCost:
    """
    Represents the costs associated with providing consulting services.
    
    Attributes:
        hourly_cost (float): The cost per hour for a consultant.
        billable_hours (int): Number of billable hours per year.
    """
    def __init__(self, hourly_cost, billable_hours):
        self.hourly_cost = hourly_cost
        self.billable_hours = billable_hours

    def calculate_yearly_costs(self, time_frame):
        """
        Calculates the yearly costs for consulting services over the specified time frame.
        
        Args:
            time_frame (int): Number of years for the cost projection.

        Returns:
            list: List of costs for each year.
        """
        return [self.hourly_cost * self.billable_hours for _ in range(time_frame)]


class ConsultingRevenue:
    name = "Consulting"

    def __init__(self, hourly_rate, billable_hours, growth_rate, hourly_cost):
        self.hourly_rate = hourly_rate
        self.billable_hours = billable_hours
        self.growth_rate = growth_rate
        self.consulting_cost = ConsultingCost(hourly_cost, billable_hours)

    def calculate_yearly_revenues(self, time_frame):
        """
        Calculates the total yearly revenues for consulting services over the specified time frame.

        Args:
            time_frame (int): Number of years for the revenue projection.

        Returns:
            list: Total yearly revenues for consulting services.
        """
        total_yearly_revenues = [0] * time_frame
        total_yearly_costs = self.consulting_cost.calculate_yearly_costs(time_frame)
        for year in range(time_frame):
            revenue = self.hourly_rate * self.billable_hours * (1 + self.growth_rate) ** year
            total_yearly_revenues[year] = revenue - total_yearly_costs[year]
        return total_yearly_revenues

    def component_details(self, time_frame):
        """
        Generates detailed information about consulting services over the specified time frame.

        Args:
            time_frame (int): Number of years for the revenue projection.

        Returns:
            dict: Detailed information including hourly rate, billable hours, growth rate, and costs.
        """
        hourly_rates = [self.hourly_rate * (1 + self.growth_rate) ** year for year in range(time_frame)]
        billable_hours = [self.billable_hours for _ in range(time_frame)]
        growth_rates = [self.growth_rate for _ in range(time_frame)]
        total_costs = self.consulting_cost.calculate_yearly_costs(time_frame)

        formatted_growth_rates = ["{:.2%}".format(rate) for rate in growth_rates]
        formatted_costs = ["${:<14,.2f}".format(cost) for cost in total_costs]

        return {
            "Hourly Rate": hourly_rates,
            "Billable Hours": billable_hours,
            "Growth Rate": formatted_growth_rates,
            "Costs": formatted_costs
        }

class SubscriptionCostStructure:
    """
    Represents the cost structure for a specific type of subscription.

    Attributes:
        data_center_cost (float): Monthly cost of data center space.
        software_licenses (list of tuples): List of software licenses and their costs.
        sales_commissions (float): Sales commission rate as a percentage.
    """

    def __init__(self, data_center_cost, software_licenses, sales_commissions):
        self.data_center_cost = data_center_cost
        self.software_licenses = software_licenses
        self.sales_commissions = sales_commissions

class SGandACost:
    def __init__(self):
        self.cost_components = {}

    def add_cost_component(self, component_name, component):
        self.cost_components[component_name] = component
        
    def add_depreciation(self, depreciation):
        self.depreciation = depreciation    

    def calculate_total_sga_costs(self, time_frame):
        total_sga_costs = [0] * time_frame
        for component_name, component in self.cost_components.items():
            component_costs = component.calculate_total_compensation(time_frame) if isinstance(component, CompensationCost) else component.calculate_cost(time_frame)
            depreciation_costs = self.depreciation.calculate_depreciation("straight_line", time_frame)
        total_sga_costs = [total + dep for total, dep in zip(total_sga_costs, depreciation_costs)]
        return total_sga_costs
        
        
        
class EmployeeType:
    def __init__(self, name, cost_per_employee, initial_employee_count, employee_growth_rate, compensation_growth_rate):
        self.name = name
        self.cost_per_employee = cost_per_employee
        self.employee_count = initial_employee_count
        self.employee_growth_rate = employee_growth_rate
        self.compensation_growth_rate = compensation_growth_rate

    def calculate_annual_compensation(self, year):
        # Adjust employee count and compensation for the year
        adjusted_employee_count = self.employee_count * (1 + self.employee_growth_rate) ** year
        adjusted_cost_per_employee = self.cost_per_employee * (1 + self.compensation_growth_rate) ** year
        return adjusted_employee_count * adjusted_cost_per_employee
    
    
class CompensationCost:
    def __init__(self):
        self.employee_types = []

    def add_employee_type(self, employee_type):
        self.employee_types.append(employee_type)

    def calculate_total_compensation(self, time_frame):
        total_compensation = [0] * time_frame
        for year in range(time_frame):
            yearly_compensation = sum([employee.calculate_annual_compensation(year) for employee in self.employee_types])
            total_compensation[year] = yearly_compensation
        return total_compensation

class Asset:
    def __init__(self, name, purchase_price, useful_life, residual_value=0):
        self.name = name
        self.purchase_price = purchase_price
        self.useful_life = useful_life
        self.residual_value = residual_value

class Depreciation:
    def __init__(self, asset_inventory):
        self.asset_inventory = asset_inventory

    def calculate_depreciation(self, method, time_frame):
        total_depreciation = [0] * time_frame
        for asset in self.asset_inventory:
            if method == "straight_line":
                depreciation = self.straight_line(asset, time_frame)
            elif method == "double_declining":
                depreciation = self.double_declining_balance(asset, time_frame)
            # Add other methods as needed

            total_depreciation = [total + annual for total, annual in zip(total_depreciation, depreciation)]
        return total_depreciation

    def straight_line(self, asset, time_frame):
        annual_depreciation = (asset.purchase_price - asset.residual_value) / asset.useful_life
        return [annual_depreciation] * time_frame

    def double_declining_balance(self, asset, time_frame):
        depreciation = []
        book_value = asset.purchase_price
        rate = (2 / asset.useful_life)
        for year in range(time_frame):
            yearly_depreciation = book_value * rate
            depreciation.append(yearly_depreciation)
            book_value -= yearly_depreciation
            if book_value < asset.residual_value:
                depreciation[-1] -= (book_value - asset.residual_value)
                book_value = asset.residual_value
        return depreciation

class BuildingExpenses:
    def __init__(self, rent, insurance, utilities):
        self.rent = rent
        self.insurance = insurance
        self.utilities = utilities

    def calculate_monthly_expenses(self):
        return self.rent + self.insurance + self.utilities

    def calculate_annual_expenses(self, time_frame):
        monthly_expenses = self.calculate_monthly_expenses()
        return [monthly_expenses * 12 for _ in range(time_frame)]


class MarketingExpenses:
    def __init__(self, num_campaigns, avg_cost_per_campaign, num_events, cost_per_event, additional_event_expenses,
                 monthly_pr_retainer, pr_months, ad_spend, social_media_management_cost, content_creation_cost,
                 content_creation, content_distribution, content_promotion, seo_tools_cost, agency_fees, ppc_budget,
                 staff_salaries, bonuses, external_agency_fees):
        self.num_campaigns = num_campaigns
        self.avg_cost_per_campaign = avg_cost_per_campaign
        self.num_events = num_events
        self.cost_per_event = cost_per_event
        self.additional_event_expenses = additional_event_expenses
        self.monthly_pr_retainer = monthly_pr_retainer
        self.pr_months = pr_months
        self.ad_spend = ad_spend
        self.social_media_management_cost = social_media_management_cost
        self.content_creation_cost = content_creation_cost
        self.content_creation = content_creation
        self.content_distribution = content_distribution
        self.content_promotion = content_promotion
        self.seo_tools_cost = seo_tools_cost
        self.agency_fees = agency_fees
        self.ppc_budget = ppc_budget
        self.staff_salaries = staff_salaries
        self.bonuses = bonuses
        self.external_agency_fees = external_agency_fees

    def calculate_campaign_budget(self):
        return self.num_campaigns * self.avg_cost_per_campaign

    def calculate_events_budget(self):
        return self.num_events * self.cost_per_event + self.additional_event_expenses

    def calculate_pr_budget(self):
        return self.monthly_pr_retainer * self.pr_months

    def calculate_social_media_budget(self):
        return self.ad_spend + self.social_media_management_cost + self.content_creation_cost

    def calculate_content_budget(self):
        return self.content_creation + self.content_distribution + self.content_promotion

    def calculate_seo_budget(self):
        return self.seo_tools_cost + self.agency_fees + self.ppc_budget

    def calculate_staff_and_agency_fees(self):
        return self.staff_salaries + self.bonuses + self.external_agency_fees

    def calculate_total_marketing_expenses(self):
        return (self.calculate_campaign_budget() + self.calculate_events_budget() +
                self.calculate_pr_budget() + self.calculate_social_media_budget() +
                self.calculate_content_budget() + self.calculate_seo_budget() +
                self.calculate_staff_and_agency_fees())

class TravelExpenses:
    def __init__(self, airfare, accommodation, meals_entertainment, ground_transport, miscellaneous, per_diem, number_of_trips, days_per_trip):
        self.airfare = airfare
        self.accommodation = accommodation
        self.meals_entertainment = meals_entertainment
        self.ground_transport = ground_transport
        self.miscellaneous = miscellaneous
        self.per_diem = per_diem
        self.number_of_trips = number_of_trips
        self.days_per_trip = days_per_trip

    def calculate_airfare_total(self):
        return self.airfare * self.number_of_trips

    def calculate_accommodation_total(self):
        return self.accommodation * self.number_of_trips * self.days_per_trip

    def calculate_meals_entertainment_total(self):
        return self.meals_entertainment * self.number_of_trips * self.days_per_trip

    def calculate_ground_transport_total(self):
        return self.ground_transport * self.number_of_trips

    def calculate_miscellaneous_total(self):
        return self.miscellaneous * self.number_of_trips

    def calculate_per_diem_total(self):
        return self.per_diem * self.number_of_trips * self.days_per_trip

    def calculate_total_travel_expenses(self):
        return (self.calculate_airfare_total() + self.calculate_accommodation_total() +
                self.calculate_meals_entertainment_total() + self.calculate_ground_transport_total() +
                self.calculate_miscellaneous_total() + self.calculate_per_diem_total())
    

class ShippingCosts:
    def __init__(self, item_name, shipping_volume, shipping_rate):
        self.item_name = item_name
        self.shipping_volume = shipping_volume
        self.shipping_rate = shipping_rate
    
    def calculate_shipping_costs(self, time_frame):
        yearly_shipping_costs = []
        for year in range(time_frame):
            costs = self.shipping_volume * self.shipping_rate
            yearly_shipping_costs.append(costs)
        return yearly_shipping_costs    
    
# Example usage
abc_revenue_model = BaseRevenueModel(time_frame=5)
time_frame = 5

# Create Employee Types
manager = EmployeeType("Manager", 100000, 10, 0.02, 0.03)
engineer = EmployeeType("Engineer", 80000, 20, 0.03, 0.02)

# Initialize Compensation Cost
compensation_cost = CompensationCost()
compensation_cost.add_employee_type(manager)
compensation_cost.add_employee_type(engineer)


total_compensation_costs = compensation_cost.calculate_total_compensation(time_frame)

# Example values for rent, insurance, and utilities
rent = 10000  # Monthly rent
insurance = 500  # Monthly insurance
utilities = 1000  # Monthly utilities

# Initialize Building Expenses
building_expenses = BuildingExpenses(rent, insurance, utilities)


# Calculate Building Expenses
annual_building_expenses = building_expenses.calculate_annual_expenses(time_frame)

# Initialize data structure
data = {
    'Attribute': [],
}

# Add years as column headers
for year in range(time_frame):
    data[f'Year {year + 1}'] = []

# Add data for each employee type
for employee in compensation_cost.employee_types:
    data['Attribute'].append(f'{employee.name} - Initial Cost per Employee')
    data['Attribute'].append(f'{employee.name} - Initial Number of Employees')
    data['Attribute'].append(f'{employee.name} - Employee Growth Rate')
    data['Attribute'].append(f'{employee.name} - Compensation Growth Rate')
    data['Attribute'].append(f'{employee.name} - Total Compensation')

    for year in range(time_frame):
        adjusted_employee_count = employee.employee_count * (1 + employee.employee_growth_rate) ** year
        adjusted_cost_per_employee = employee.cost_per_employee * (1 + employee.compensation_growth_rate) ** year
        total_compensation = adjusted_cost_per_employee * adjusted_employee_count

        if year == 0:
            data[f'Year {year + 1}'].extend([
                employee.cost_per_employee,
                employee.employee_count,
                employee.employee_growth_rate,
                employee.compensation_growth_rate,
                total_compensation
            ])
        else:
            data[f'Year {year + 1}'].extend([
                adjusted_cost_per_employee,
                adjusted_employee_count,
                '',  # Growth rates are constant, only display in the first year
                '',
                total_compensation
            ])
compensation_df = pd.DataFrame(data)

def format_value(val):
    if isinstance(val, float):
        if val < 1:  # Assuming growth rates are less than 1
            return "{:.2%}".format(val)
        return "${:,.2f}".format(val)
    return val

compensation_df.set_index('Attribute', inplace=True)
compensation_df = compensation_df.applymap(format_value)

# Initialize Marketing Expenses with hypothetical values
marketing_expenses = MarketingExpenses(
    num_campaigns=10,
    avg_cost_per_campaign=2000,
    num_events=5,
    cost_per_event=3000,
    additional_event_expenses=2000,
    monthly_pr_retainer=1500,
    pr_months=12,
    ad_spend=10000,
    social_media_management_cost=2500,
    content_creation_cost=5000,
    content_creation=4000,
    content_distribution=2000,
    content_promotion=3000,
    seo_tools_cost=1200,
    agency_fees=3500,
    ppc_budget=8000,
    staff_salaries=50000,
    bonuses=10000,
    external_agency_fees=6000
)


# Initialize Travel Expenses with hypothetical values
travel_expenses = TravelExpenses(
    airfare=500,
    accommodation=200,
    meals_entertainment=100,
    ground_transport=50,
    miscellaneous=30,
    per_diem=70,
    number_of_trips=10,
    days_per_trip=3
)



# Define different product types
product_1 = ProductType("Product A", 50, 2000, 0.03)
product_2 = ProductType("Product B", 80, 1500, 0.05)
product_3 = ProductType("Product C", 100, 1000, 0.04)

# Define cost structures for each product type

# Define cost structures for Product 1
product_1_costs = ProductCostStructure(material_costs=[("Material1", 1.2, 2), ("Material2", 1.1, 3)], labor_cost_per_unit=50000, overhead_cost_per_unit=10000)


# Define cost structures for Product 2
product_2_costs = ProductCostStructure(material_costs=[("Material1", 1.2, 2), ("Material2", 1.1, 3)], labor_cost_per_unit=50000, overhead_cost_per_unit=10000)


# Define cost structures for Product 3
product_3_costs = ProductCostStructure(material_costs=[("Material1", 1.2, 2), ("Material2", 1.1, 3)], labor_cost_per_unit=50000, overhead_cost_per_unit=10000)



# Aggregate them in ProductSalesRevenue with associated costs
product_sales = ProductSalesRevenue(
    [product_1, product_2, product_3],
    [product_1_costs, product_2_costs, product_3_costs]
)

# Growth rates for subscriptions
basic_sub_drivers = [
    {"base_growth": 0.1, "marketing_impact": 0.02},
    {"base_growth": 0.12, "marketing_impact": 0.03},
    # ... other years' drivers ...
]

premium_sub_drivers = [
    {"base_growth": 0.15, "marketing_impact": 0.04},
    {"base_growth": 0.18, "marketing_impact": 0.05},
    # ... other years' drivers ...
]

data_center_cost = 10000  # Example value
software_costs = {'Software1': 500, 'Software2': 300}  # Example dictionary
sales_commission_rate = 0.05  # Example value


# Correct initialization
basic_subscription = SubscriptionType(
    "Basic", 
    20, 
    1000, 
    0.02, 
    basic_sub_drivers, 
    data_center_cost,  # Assuming you have a value for this
    software_costs,    # Assuming you have a dictionary for this
    sales_commission_rate  # Assuming you have a value for this
)

premium_subscription = SubscriptionType(
    "Premium", 
    50, 
    500, 
    0.01, 
    premium_sub_drivers, 
    data_center_cost,  # Assuming you have a value for this
    software_costs,    # Assuming you have a dictionary for this
    sales_commission_rate  # Assuming you have a value for this
)


# Define subscription costs
subscription_costs = SubscriptionCostStructure(data_center_cost=20000, software_licenses=[("License A", 5000), ("License B", 3000)], sales_commissions=0.05)

# Aggregate subscriptions and their costs
subscription_revenue = SubscriptionRevenue(
    [basic_subscription, premium_subscription],
    subscription_costs
)



# Define consulting revenue and its costs
hourly_cost_example = 100  # Example value for the hourly cost
consulting_revenue = ConsultingRevenue(150, 500, 0.03, hourly_cost_example)

###SG&A



# Initialize SG&A Cost
sga_cost = SGandACost()
sga_cost.add_cost_component("Compensation", compensation_cost)

# Define asset inventory
asset_inventory = [
    Asset("Computer", 1000, 5),
    Asset("Vehicle", 20000, 10, 5000),
    # Add other assets as needed
]

# Initialize Depreciation
depreciation = Depreciation(asset_inventory)

# Calculate yearly depreciation
yearly_depreciation = depreciation.calculate_depreciation("straight_line", time_frame)


# Add Depreciation to SG&A Costs
sga_cost.add_depreciation(depreciation)

# Initialize shipping items
shipping_items = [
    ShippingCosts("Item A", 1000, 1.5),
    ShippingCosts("Item B", 800, 2.0),
    # Add more items as needed
]


# Add to the revenue model
abc_revenue_model.add_revenue_type(product_sales)
abc_revenue_model.add_revenue_type(subscription_revenue)
abc_revenue_model.add_revenue_type(consulting_revenue)
abc_revenue_model.add_sga_costs(sga_cost)




# Assuming the same setup for product types, subscription types, consulting types, product costs, subscription costs, and time frame


# Function todef format_numbers(df):
def format_numbers(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x: "{:,.2f}".format(x) if isinstance(x, (int, float)) else x)
    return df

# Product Revenue Data
product_revenue_rows = []
total_product_revenue_per_year = [0] * time_frame
for product in product_sales.product_types:
    yearly_revenues = product.calculate_yearly_revenues(time_frame)
    details = product.component_details(time_frame)
    total_product_revenue_per_year = [total + rev for total, rev in zip(total_product_revenue_per_year, yearly_revenues)]

    product_revenue_rows.extend([
        [f"{product.name} Revenue"] + yearly_revenues,
        [f"  {product.name} Unit Price"] + details["Unit Price"],
        [f"  {product.name} Volume"] + details["Volume"],
        [f"  {product.name} Growth Rate"] + details["Growth Rate"]
    ])
product_revenue_rows.insert(0, ["Total Product Revenue"] + total_product_revenue_per_year)






# Subscription Revenue Data
subscription_revenue_rows = []
total_subscription_revenue_per_year = [0] * time_frame
for subscription in subscription_revenue.subscription_types:
    yearly_revenues = subscription.calculate_revenues(time_frame)
    details = subscription.component_details(time_frame)
    total_subscription_revenue_per_year = [total + rev for total, rev in zip(total_subscription_revenue_per_year, yearly_revenues)]

    subscription_revenue_rows.extend([
        [f"{subscription.name} Revenue"] + yearly_revenues,
        [f"  {subscription.name} Monthly Fee"] + details["Monthly Fee"],
        [f"  {subscription.name} Subscribers"] + details["Subscribers"],
        [f"  {subscription.name} Churn Rate"] + details["Churn Rate"],
        [f"  {subscription.name} Growth Rate"] + details["Growth Rate"]
    ])
subscription_revenue_rows.insert(0, ["Total Subscription Revenue"] + total_subscription_revenue_per_year)


# Consulting Revenue Data
consulting_revenue_rows = []
total_consulting_revenue_per_year = [0] * time_frame
yearly_revenues = consulting_revenue.calculate_yearly_revenues(time_frame)
details = consulting_revenue.component_details(time_frame)
total_consulting_revenue_per_year = [total + rev for total, rev in zip(total_consulting_revenue_per_year, yearly_revenues)]

consulting_revenue_rows.extend([
    ["Consulting Revenue"] + yearly_revenues,
    ["  Consulting Hourly Rate"] + details["Hourly Rate"],
    ["  Consulting Billable Hours"] + details["Billable Hours"],
    ["  Consulting Growth Rate"] + details["Growth Rate"]
])
consulting_revenue_rows.insert(0, ["Total Consulting Revenue"] + total_consulting_revenue_per_year)


# Product Costs
product_cost_rows = []
total_product_cost_per_year = [0] * time_frame

for product, product_cost_structure in zip(product_sales.product_types, product_sales.product_costs):
    yearly_volumes = product.component_details(time_frame)["Volume"]
    yearly_material_costs = []
    yearly_costs = []  # Define the yearly_costs list here

    for volume in yearly_volumes:
        total_material_cost_per_year = sum([mc.calculate_cost() * volume for mc in product_cost_structure.material_costs])
        yearly_material_costs.append(total_material_cost_per_year)
        total_cost_per_unit = product_cost_structure.calculate_total_cost_per_unit()
        yearly_costs.append(total_cost_per_unit * volume)  # Calculate yearly costs for each product

    product_cost_rows.extend([
        [f"{product.name} Total Cost"] + yearly_costs,
        [f"  {product.name} Material Cost"] + yearly_material_costs,
        [f"  {product.name} Labor Cost"] + [product_cost_structure.labor_cost_per_unit * volume for volume in yearly_volumes],
        [f"  {product.name} Overhead Cost"] + [product_cost_structure.overhead_cost_per_unit * volume for volume in yearly_volumes]
    ])




# Subscription Costs Data
subscription_cost_rows = []
total_subscription_cost_per_year = [0] * time_frame
for subscription in subscription_revenue.subscription_types:
    yearly_costs = subscription.calculate_subscription_costs(time_frame)
    total_subscription_cost_per_year = [total + cost for total, cost in zip(total_subscription_cost_per_year, yearly_costs)]

    subscription_cost_rows.extend([
        [f"{subscription.name} Total Cost"] + yearly_costs,
        [f"  {subscription.name} Data Center Cost"] + [subscription.data_center_cost * 12] * time_frame,
        [f"  {subscription.name} Software Costs"] + [sum(subscription.software_costs.values()) * 12] * time_frame,
        [f"  {subscription.name} Sales Commission"] + [subscription.sales_commission_rate * revenue for revenue in subscription.calculate_revenues(time_frame)]
    ])
subscription_cost_rows.insert(0, ["Total Subscription Costs"] + total_subscription_cost_per_year)


# Consulting Costs Data
consulting_cost_rows = []
total_consulting_cost_per_year = [0] * time_frame
yearly_costs = consulting_revenue.consulting_cost.calculate_yearly_costs(time_frame)
total_consulting_cost_per_year = [total + cost for total, cost in zip(total_consulting_cost_per_year, yearly_costs)]

consulting_cost_rows.extend([
    ["Total Consulting Costs"] + total_consulting_cost_per_year,
    ["  Consulting Hourly Cost"] + [consulting_revenue.consulting_cost.hourly_cost] * time_frame,
    ["  Consulting Billable Hours"] + [consulting_revenue.consulting_cost.billable_hours] * time_frame
])


# Depreciation Data
depreciation_rows = []
depreciation_rows.extend([
    ["Total Depreciation"] + yearly_depreciation
])


# Building Expenses Data
building_expense_rows = [
    ["Rent"] + [rent * 12] * time_frame,
    ["Insurance"] + [insurance * 12] * time_frame,
    ["Utilities"] + [utilities * 12] * time_frame,
    ["Total Building Expenses"] + annual_building_expenses
]

# Travel Expenses Data for DataFrame
travel_expense_rows = [
    ["Airfare"] + [travel_expenses.calculate_airfare_total()] * time_frame,
    ["Accommodation"] + [travel_expenses.calculate_accommodation_total()] * time_frame,
    ["Meals and Entertainment"] + [travel_expenses.calculate_meals_entertainment_total()] * time_frame,
    ["Ground Transport"] + [travel_expenses.calculate_ground_transport_total()] * time_frame,
    ["Miscellaneous"] + [travel_expenses.calculate_miscellaneous_total()] * time_frame,
    ["Per Diem"] + [travel_expenses.calculate_per_diem_total()] * time_frame,
    ["Total Travel Expenses"] + [travel_expenses.calculate_total_travel_expenses()] * time_frame
]

# Marketing Expenses Data for DataFrame
marketing_expense_rows = [
    ["Campaign Budget"] + [marketing_expenses.calculate_campaign_budget()] * time_frame,
    ["Events Budget"] + [marketing_expenses.calculate_events_budget()] * time_frame,
    ["PR Budget"] + [marketing_expenses.calculate_pr_budget()] * time_frame,
    ["Social Media Budget"] + [marketing_expenses.calculate_social_media_budget()] * time_frame,
    ["Content Budget"] + [marketing_expenses.calculate_content_budget()] * time_frame,
    ["SEO Budget"] + [marketing_expenses.calculate_seo_budget()] * time_frame,
    ["Staff and Agency Fees"] + [marketing_expenses.calculate_staff_and_agency_fees()] * time_frame,
    ["Total Marketing Expenses"] + [marketing_expenses.calculate_total_marketing_expenses()] * time_frame
]

# Calculate total shipping costs and create data rows
shipping_cost_rows = [["Total Shipping Costs"]]
total_shipping_cost_per_year = [0] * time_frame

for item in shipping_items:
    item_costs = item.calculate_shipping_costs(time_frame)
    total_shipping_cost_per_year = [total + cost for total, cost in zip(total_shipping_cost_per_year, item_costs)]

    # Add item details to the rows
    shipping_cost_rows.extend([
        [f"  {item.item_name} Volume"] + [item.shipping_volume] * time_frame,
        [f"  {item.item_name} Rate"] + [item.shipping_rate] * time_frame,
        [f"  {item.item_name} Cost"] + item_costs
    ])

# Add the total costs to the first row
shipping_cost_rows[0] += total_shipping_cost_per_year


def format_with_commas(x):
  
    if isinstance(x, (int, float)):
        return "{:,.2f}".format(x)
    return x

# Column headers
columns = ['Attribute'] + [f'Year {i + 1}' for i in range(time_frame)]

# Convert rows to DataFrames


df_product_revenue = pd.DataFrame(product_revenue_rows, columns=columns)
formatted_df_product_revenue = df_product_revenue.applymap(format_with_commas)
print(formatted_df_product_revenue.to_string(index=False))

df_subscription_revenue = pd.DataFrame(subscription_revenue_rows, columns=columns)
formatted_df_subscription_revenue = df_subscription_revenue.applymap(format_with_commas)
print(formatted_df_subscription_revenue.to_string(index=False))

# Convert rows to DataFrame
df_product_costs = pd.DataFrame(product_cost_rows, columns=columns)

# Apply formatting
formatted_df_product_costs = df_product_costs.applymap(format_with_commas)

# Display the DataFrame
print(formatted_df_product_costs.to_string(index=False))

df_product_costs = pd.DataFrame(product_cost_rows, columns = columns)
formatted_df_product_costs = df_product_costs.applymap(format_with_commas)
print(formatted_df_product_costs.to_string(index=False))

df_subscription_costs = pd.DataFrame(subscription_cost_rows, columns=columns)
formatted_df_subscription_costs = df_subscription_costs.applymap(format_with_commas)
print(formatted_df_subscription_costs.to_string(index=False))

df_consulting_costs = pd.DataFrame(consulting_cost_rows, columns=columns)
formatted_df_consulting_costs = df_consulting_costs.applymap(format_with_commas)
print(formatted_df_consulting_costs.to_string(index=False))

print(compensation_df)

# Convert depreciation rows to DataFrame
df_depreciation = pd.DataFrame(depreciation_rows, columns=columns)
formatted_df_depreciation = df_depreciation.applymap(format_with_commas)


# Display the DataFrame
print(formatted_df_depreciation.to_string(index=False))

# Convert building expense rows to DataFrame
df_building_expenses = pd.DataFrame(building_expense_rows, columns=columns)
formatted_df_building_expenses = df_building_expenses.applymap(format_with_commas)

# Display the DataFrame
print(formatted_df_building_expenses.to_string(index=False))



# Convert marketing expense rows to DataFrame

df_marketing_expenses = pd.DataFrame(marketing_expense_rows, columns=columns)
formatted_df_marketing_expenses = df_marketing_expenses.applymap(format_with_commas)

# Display the DataFrame
print(formatted_df_marketing_expenses.to_string(index=False))


# Convert travel expense rows to DataFrame

df_travel_expenses = pd.DataFrame(travel_expense_rows, columns=columns)
formatted_df_travel_expenses = df_travel_expenses.applymap(format_with_commas)

# Display the DataFrame
print(formatted_df_travel_expenses.to_string(index=False))


# Convert shipping costs rows to  DataFrame and apply formatting
df_shipping_costs = pd.DataFrame(shipping_cost_rows, columns=columns)
formatted_df_shipping_costs = df_shipping_costs.applymap(format_with_commas)
print(formatted_df_shipping_costs.to_string(index=False))

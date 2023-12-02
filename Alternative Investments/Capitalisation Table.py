import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


class Security:
    def __init__(self, name, shares, price_per_share, seniority_level=0):
        self.name = name
        self.shares = shares
        self.price_per_share = price_per_share
        self.seniority_level = seniority_level

    def value(self):
        return self.shares * self.price_per_share

    def calculate_payout(self, remaining_exit_value):
        payout = min(self.value(), remaining_exit_value)
        return payout, remaining_exit_value - payout

class CommonStock(Security):
    def __init__(self, name, shares, price_per_share):
        super().__init__(name, shares, price_per_share)

class PreferredStock(Security):
    def __init__(self, name, shares, price_per_share, liquidation_preference, participating=False, cap=None, seniority_level=1):
        super().__init__(name, shares, price_per_share, seniority_level)
        self.liquidation_preference = liquidation_preference
        self.participating = participating
        self.cap = cap

    def calculate_payout(self, remaining_exit_value):
        if remaining_exit_value <= 0:
            return 0, remaining_exit_value

        liquidation_payout = min(self.liquidation_preference * self.shares, remaining_exit_value)
        remaining_after_liquidation = remaining_exit_value - liquidation_payout

        if self.participating:
            if self.cap:
                cap_amount = self.cap * self.shares
                participation_payout = min(remaining_after_liquidation, cap_amount - liquidation_payout)
            else:
                participation_payout = remaining_after_liquidation

            total_payout = liquidation_payout + participation_payout
            return total_payout, remaining_exit_value - total_payout
        else:
            return liquidation_payout, remaining_after_liquidation

class ConvertibleNote(Security):
    def __init__(self, name, principal_amount, conversion_rate, trigger_price, seniority_level=2):
        super().__init__(name, 0, 0, seniority_level)  # Shares and price_per_share are 0 until conversion
        self.principal_amount = principal_amount
        self.conversion_rate = conversion_rate
        self.trigger_price = trigger_price
        self.converted = False

    def convert(self, current_price):
        if current_price >= self.trigger_price:
            self.shares = self.principal_amount / current_price * self.conversion_rate
            self.price_per_share = current_price
            self.converted = True
        else:
            self.shares = 0
            self.converted = False

    def calculate_payout(self, remaining_exit_value):
        if not self.converted or remaining_exit_value <= 0:
            return 0, remaining_exit_value
        return super().calculate_payout(remaining_exit_value)
    
class StockOptionsPool:
    def __init__(self, total_options, price_per_share, vesting_schedule=None):
        self.total_options = total_options
        self.granted_options = 0
        self.price_per_share = price_per_share
        self.vesting_schedule = vesting_schedule or {}
        self.exercised_options = 0

    def grant_options(self, number_of_options, vesting_start_date):
        if self.granted_options + number_of_options > self.total_options:
            raise ValueError("Not enough options available in the pool.")
        self.granted_options += number_of_options
        self.vesting_schedule[vesting_start_date] = self.vesting_schedule.get(vesting_start_date, 0) + number_of_options

    def exercise_options(self, number_of_options):
        if number_of_options > self.exercised_options:
            raise ValueError("Not enough vested options available to exercise.")
        self.exercised_options += number_of_options

    def get_vested_options(self, as_of_date=None):
        as_of_date = as_of_date or datetime.today()
        vested_options = 0
        for vesting_date, options in self.vesting_schedule.items():
            if vesting_date <= as_of_date:
                vested_options += options
        return vested_options

    def exercise_options(self, number_of_options, exercise_date):
        vested_options = self.get_vested_options(as_of_date=exercise_date)
        if number_of_options > vested_options - self.exercised_options:
            raise ValueError("Not enough vested options available to exercise.")
        self.exercised_options += number_of_options
        # Convert exercised options into common stock and add to the cap table
        # Assume 1:1 conversion for simplicity, adjust as needed
        exercised_shares = number_of_options
        return CommonStock("Exercised Options", exercised_shares, self.price_per_share)

class CapTable:
    def __init__(self):
        self.securities = []
        self.stock_options_pool = None
        self.funding_rounds = []

    def add_security(self, security, funding_round=None):
        self.securities.append(security)
        if funding_round:
            self.funding_rounds.append(funding_round)

    def set_stock_options_pool(self, stock_options_pool):
        self.stock_options_pool = stock_options_pool

    def update_for_funding_round(self, funding_round, new_securities):
        # Logic to handle dilution and addition of new securities during a funding round
        self.funding_rounds.append(funding_round)
        for security in new_securities:
            self.add_security(security)

    def apply_stock_split(self, split_ratio):
        # Logic to handle stock splits or reverse splits
        for security in self.securities:
            security.shares *= split_ratio

    def perform_waterfall_analysis(self, exit_value):
        # Enhanced logic to handle various payout scenarios
        sorted_securities = sorted(self.securities, key=lambda x: x.seniority_level, reverse=True)
        payouts = {}
        remaining_exit_value = exit_value

        for security in sorted_securities:
            payout, remaining_exit_value = security.calculate_payout(remaining_exit_value)
            payouts[security.name] = payout

        return payouts
    
    def update_for_funding_round(self, funding_round, new_securities):
        # Dilution effect and addition of new securities during a funding round
        self.funding_rounds.append(funding_round)
        for security in new_securities:
            self.add_security(security)
            # Apply anti-dilution adjustments if applicable
            for existing_security in self.securities:
                if isinstance(existing_security, PreferredStock):
                    existing_security.adjust_for_anti_dilution(security.price_per_share)

    def apply_stock_split(self, split_ratio):
        for security in self.securities:
            security.shares *= split_ratio
            security.price_per_share /= split_ratio

    def handle_option_exercise(self, exercise_date):
        if not self.stock_options_pool:
            raise ValueError("No stock options pool set.")
        exercised_stock = self.stock_options_pool.exercise_options(self.stock_options_pool.exercised_options, exercise_date)
        self.add_security(exercised_stock)

payouts_df = pd.DataFrame(list(payouts.items()), columns=['Security Name', 'Payout Amount'])
print(payouts_df)
plt.figure(figsize=(10, 6))
plt.pie(cap_table_df['Ownership'], labels=cap_table_df['Name'], autopct='%1.1f%%')
plt.title('Cap Table Ownership Structure')
plt.show()
plt.figure(figsize=(12, 6))
plt.bar(payouts_df['Security Name'], payouts_df['Payout Amount'])
plt.xlabel('Security Name')
plt.ylabel('Payout Amount')
plt.title('Waterfall Analysis Payouts')
plt.xticks(rotation=45)
plt.show()


# Example usage
cap_table = CapTable()
cap_table.add_security(CommonStock("Common Stock A", 10000, 1))
cap_table.add_security(PreferredStock("Preferred Stock B", 5000, 2, 10000))  # 10000 is the liquidation preference
cap_table.add_security(ConvertibleNote("Convertible Note C", 10000, 1.1, 1.5))

# Performing waterfall analysis (assuming an exit value)
exit_value = 50000  # Example exit value
payouts = cap_table.perform_waterfall_analysis(exit_value)
print(payouts)

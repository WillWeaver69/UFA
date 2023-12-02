import numpy as np
import matplotlib.pyplot as plt

def generate_binomial_tree(initial_value, up_factor, down_factor, steps):
    """
    Generate a binomial tree.
    :param initial_value: The initial value at the root of the tree.
    :param up_factor: The factor by which the value increases.
    :param down_factor: The factor by which the value decreases.
    :param steps: Number of steps in the tree.
    :return: A NumPy array representing the binomial tree.
    """
    tree = np.zeros((steps + 1, steps + 1))
    for i in range(steps + 1):
        for j in range(i + 1):
            tree[j, i] = initial_value * (up_factor ** (i - j)) * (down_factor ** j)
    return tree

def value_fixed_income_instrument(face_value, coupon_rate, maturity, interest_rate_tree):
    """
    Value a fixed income instrument using a given interest rate tree.
    :param face_value: The face value of the instrument.
    :param coupon_rate: The coupon rate of the instrument.
    :param maturity: The maturity of the instrument in time steps.
    :param interest_rate_tree: A NumPy array representing the interest rate tree.
    :return: A NumPy array representing the valuation tree.
    """
    coupon_payment = face_value * coupon_rate
    steps = interest_rate_tree.shape[1] - 1
    if maturity > steps:
        raise ValueError("Maturity exceeds the number of time steps in the interest rate tree.")
    valuation_tree = np.zeros_like(interest_rate_tree)
    valuation_tree[:, maturity] = face_value + coupon_payment
    for t in range(maturity - 1, -1, -1):
        expected_value = 0.5 * (valuation_tree[:, t + 1][:-1] + valuation_tree[:, t + 1][1:])
        discount_factor = 1 / (1 + interest_rate_tree[:, t][:-1])
        valuation_tree[:, t][:-1] = (coupon_payment + expected_value) * discount_factor
    return valuation_tree

def value_option(S0, strike_price, u, d, r, steps, option_type='call', american=False):
    """
    Value an option using a binomial model.
    :param S0: Initial asset price.
    :param strike_price: Strike price of the option.
    :param u: Up factor for asset price.
    :param d: Down factor for asset price.
    :param r: Risk-free interest rate.
    :param steps: Number of steps in the binomial model.
    :param option_type: Type of the option ('call' or 'put').
    :param american: Boolean indicating if the option is American.
    :return: The value of the option.
    """
    p = (np.exp(r) - d) / (u - d)  # Risk-neutral probability
    asset_tree = generate_binomial_tree(S0, u, d, steps)
    option_tree = np.zeros_like(asset_tree)

    # Calculate option value at final nodes
    if option_type == 'call':
        option_tree[:, -1] = np.maximum(asset_tree[:, -1] - strike_price, 0)
    else:
        option_tree[:, -1] = np.maximum(strike_price - asset_tree[:, -1], 0)

    # Backward induction for option value
    for j in range(steps - 1, -1, -1):
        for i in range(j + 1):
            option_value = np.exp(-r) * (p * option_tree[i, j + 1] + (1 - p) * option_tree[i + 1, j + 1])
            if american:
                if option_type == 'call':
                    option_tree[i, j] = max(option_value, asset_tree[i, j] - strike_price)
                else:
                    option_tree[i, j] = max(option_value, strike_price - asset_tree[i, j])
            else:
                option_tree[i, j] = option_value

    return option_tree[0, 0]

def plot_tree(tree, valuation_tree=None):
    """
    Plot a binomial tree.
    :param tree: A NumPy array representing the binomial tree to plot.
    :param valuation_tree: An optional NumPy array representing a secondary valuation tree.
    """
    steps = tree.shape[1] - 1
    plt.figure(figsize=(10, 6))
    plt.title("Binomial Tree Visualization")
    for i in range(steps + 1):
        for j in range(i + 1):
            plt.scatter(i, tree[j, i], color='blue')
            if valuation_tree is not None:
                plt.text(i, tree[j, i], f"{valuation_tree[j, i]:.2f}", color='red')
            if i < steps:
                plt.plot([i, i + 1], [tree[j, i], tree[j, i + 1]], color='black')
                plt.plot([i, i + 1], [tree[j, i], tree[j + 1, i + 1]], color='black')
    plt.xlabel("Time Step")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()

# User interaction
asset_type = input("Enter the type of asset to value (fixed_income/option): ").lower()

if asset_type == 'fixed_income':
    r0 = float(input("Initial interest rate (as a decimal): "))
    u = float(input("Up factor for interest rate: "))
    d = float(input("Down factor for interest rate: "))
    n = int(input("Number of time steps: "))
    interest_rate_tree = generate_binomial_tree(r0, u, d, n)
    face_value = float(input("Face value of the fixed income instrument: "))
    coupon_rate = float(input("Coupon rate (as a decimal): "))
    maturity = int(input("Maturity of the instrument in time steps: "))
    valuation_tree = value_fixed_income_instrument(face_value, coupon_rate, maturity, interest_rate_tree)
    plot_tree(interest_rate_tree, valuation_tree)

elif asset_type == 'option':
    S0 = float(input("Initial asset price: "))
    strike_price = float(input("Option strike price: "))
    u = float(input("Up factor for asset price: "))
    d = float(input("Down factor for asset price: "))
    r = float(input("Risk-free interest rate (as a decimal): "))
    steps = int(input("Number of time steps: "))
    option_type = input("Type of option (call/put): ").lower()
    is_american = input("Is the option American? (yes/no): ").lower() == 'yes'

    option_valuation = value_option(S0, strike_price, u, d, r, steps, option_type, american=is_american)
    print(f"The estimated value of the {option_type} option is: {option_valuation:.2f}")

    asset_price_tree = generate_binomial_tree(S0, u, d, steps)
    plot_tree(asset_price_tree)

else:
    print("Invalid asset type entered. Please enter either 'fixed_income' or 'option'.")

def calculate_forward__interest_rate(S_T1, S_T2, T1, T2):
    """
    Calculate the forward rate for a FRA.

    Parameters:
    S_T1 (float): The spot rate until time T1.
    S_T2 (float): The spot rate until time T2.
    T1 (float): Time in days until the first period (T1).
    T2 (float): Time in days until the second period (T2).

    Returns:
    float: The forward rate F.
    """
    
    #Unannualise the spot rates
    S_T1_unannualised = S_T1 *(T1/360)
    S_T2_unannualised = S_T2 * (T2/360)
    
    #Calculate the actual i.e. unannualised rate on a loan from T1 until T2
    forward_interest_rate_unannualised = ((1 + S_T2_unannualised) / (1 + S_T1_unannualised)) -1
    
    #Annualise the rate
    forward_interest_rate = forward_interest_rate_unannualised *(360/(t2 -t1))
    return forward_interest_rate

# Example usage
S_T1 = 0.04  # Spot rate for T1 period (e.g., 2%)
S_T2 = 0.05  # Spot rate for T2 period (e.g., 2.5%)
T1 = 30  # 30 days until T1
T2 = 120  # 120 days until T2

forward_rate = calculate_forward_rate(S_T1, S_T2, T1, T2)
formatted_forward_rate = f"{forward_rate:.2%}"
print("The forward rate is:", formatted_forward_rate)


def calculate_endyear_pension_plan_projected_benefit_obligation(beginning_PBO, service_cost, interest_cost, past_service_cost, actuarial_losses_gains, benefits_paid):
    """
    Function to calculate the projected benefit obligation, also known as the 
    present value of defined benefit obligation or PVDBO under IFRS at year end.
    
    PBO is the actuarial present value (at an assumed discount rate) of all future pension benefits
    earned to date, based on expected future salary increases. From one period to the next,
    the PBO changes as a result of current service cost, past service cost, changes in actuarial assumptions, and benefits 
    paid to employees.

    Parameters:
    - beginning_PBO: The PBO at the beginning of the year.
    - service_cost: The cost of benefits earned by employees during the current year.
    - interest_cost: The interest on the PBO at the beginning of the year.
    - past_service_cost: Changes in the pension benefits related to prior years.
    - actuarial_losses_gains: Changes in PBO due to revisions in actuarial assumptions.
    - benefits_paid: The benefits paid out to retirees during the year.

    Returns:
    - ending_PBO: The calculated PBO at the end of the year.
    """

    # Initialize actuarial gain and loss
    actuarial_gain = 0
    actuarial_loss = 0

    # Calculate whether the change in actuarial assumption leads to a gain or a loss
    if actuarial_losses_gains > 0:
        actuarial_gain = actuarial_losses_gains
    else:
        actuarial_loss = -actuarial_losses_gains  # Assuming actuarial_losses_gains is negative for losses

    # Calculate the ending PBO
    ending_PBO = beginning_PBO + service_cost + interest_cost + past_service_cost + actuarial_loss - actuarial_gain - benefits_paid
    
    return ending_PBO

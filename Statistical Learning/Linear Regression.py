import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.graphics.gofplots as smgof

def run_ols_regression(data, independent_vars, dependent_var):
    """
    Performs Ordinary Least Squares (OLS) regression on the provided dataset and returns the model.
    """
    X = data[independent_vars]
    X = sm.add_constant(X)  # Add a constant term for the intercept
    y = data[dependent_var]
    model = sm.OLS(y, X).fit()
    return model

def model_summary(model):
    """
    Prints the summary of the fitted OLS regression model.
    """
    print(model.summary())

def plot_regression_results(data, model, independent_vars, dependent_var):
    """
    Generates plots to visualize the regression results.
    """
    plot_size = (10, 6)

    # Scatter Plots with Regression Lines
    for var in independent_vars:
        fig, ax = plt.subplots(figsize=plot_size)
        sns.regplot(x=var, y=dependent_var, data=data, ax=ax)
        ax.set_title(f'Relationship between {var} and {dependent_var}')
        plt.show()

    # Residual Plot
    predicted_values = model.predict(sm.add_constant(data[independent_vars]))
    residuals = data[dependent_var] - predicted_values
    fig, ax = plt.subplots(figsize=plot_size)
    ax.scatter(predicted_values, residuals)
    ax.axhline(y=0, color='red', linestyle='--')
    ax.set_xlabel('Predicted Values')
    ax.set_ylabel('Residuals')
    ax.set_title('Residual Plot')
    plt.show()

    # QQ Plot
    fig = plt.figure(figsize=plot_size)
    ax = fig.add_subplot(111)
    smgof.qqplot(residuals, line='s', ax=ax)
    ax.set_title('QQ Plot of Residuals')
    plt.show()

    # Coefficient Plot
    coefficients = model.params[1:]  # Exclude the intercept
    conf_int = model.conf_int().loc[coefficients.index]
    errors = conf_int[1] - conf_int[0]
    fig, ax = plt.subplots(figsize=plot_size)
    ax.errorbar(range(len(coefficients)), coefficients, yerr=errors, fmt='o', color='b', ecolor='lightgray', elinewidth=3, capsize=0)
    ax.axhline(y=0, color='red', linestyle='--')
    ax.set_xticks(range(len(coefficients)))
    ax.set_xticklabels(coefficients.index, rotation=45)
    ax.set_title('Regression Coefficients and Confidence Intervals')
    ax.set_ylabel('Coefficients')
    plt.show()

# Example usage
# Load your data into a DataFrame 'data'
# Define your independent and dependent variables
# independent_vars = ['column1', 'column2', ...]  # Replace with your column names
# dependent_var = 'target_column'                # Replace with your target column name
# model = run_ols_regression(data, independent_vars, dependent_var)
# model_summary(model)
# plot_regression_results(data, model, independent_vars, dependent_var)

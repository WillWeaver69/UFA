import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

def basic_info(df):
    print("Basic DataFrame Information")
    print("============================")
    print("Shape of DataFrame: ", df.shape)
    print("\nColumns and Data types:")
    # Using tabulate for better formatting
    print(tabulate(pd.DataFrame(df.dtypes, columns=['Data Type']), headers='keys', tablefmt='psql'))
    print("\n")

def descriptive_stats(df):
    print("Descriptive Statistics for Numerical Columns")
    print("================================================")
    print(df.describe())
    
    # Check for object-type columns
    if 'object' in df.dtypes.values:
        print("\nDescriptive Statistics for Categorical Columns")
        print("=================================================")
        print(df.describe(include=['object']))
    else:
        print("\nNo Categorical Columns to Display")
    
    print("\n")

def missing_data_analysis(df):
    print("Missing Data Analysis")
    print("=======================")
    missing_data = df.isnull().sum()
    missing_percent = (df.isnull().sum() / df.shape[0]) * 100
    missing_df = pd.DataFrame({'Count': missing_data, 'Percentage': missing_percent})
    # Using tabulate to format the output
    print(tabulate(missing_df, headers='keys', tablefmt='psql'))
    print("\n")

def data_distribution(df):
    print("Data Distribution for Numerical Columns")
    print("===========================================")
    df.hist(figsize=(12, 10), bins=20)
    plt.show()

def correlation_analysis(df):
    print("Correlation Analysis")
    print("======================")
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm')
    plt.show()

def main(df):
    basic_info(df)
    descriptive_stats(df)
    missing_data_analysis(df)
    data_distribution(df)
    correlation_analysis(df)

# Example usage (replace 'your_data.csv' with your dataset)
# df = pd.read_csv('your_data.csv')
# main(df)

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from ISLP import load_data, confusion_table

# Load and Prepare Data
def prepare_data(data, predictors, target, split_year):
    """
    Prepares the data for Quadratic Discriminant Analysis.

    Parameters:
    - data: DataFrame, the dataset to be used.
    - predictors: list, the names of columns to be used as predictors.
    - target: str, the name of the target column.
    - split_year: int, the year to split the data into training and testing sets.

    Returns:
    - X_train: DataFrame, training data predictors.
    - X_test: DataFrame, testing data predictors.
    - y_train: Series, training data target.
    - y_test: Series, testing data target.
    """
    # Filter predictor variables and target variable
    X = data[predictors]
    y = data[target]

    # Split data into training and testing sets based on the specified year
    train = data['Year'] < split_year
    X_train, X_test = X[train], X[~train]
    y_train, y_test = y[train], y[~train]

    return X_train, X_test, y_train, y_test

# Main function to run the analysis
def run_qda_analysis(split_year=2005, predictors=['Lag1', 'Lag2']):
    """
    Runs Quadratic Discriminant Analysis on the Smarket dataset.

    Parameters:
    - split_year: int, default 2005. The year to split the training and testing data.
    - predictors: list, default ['Lag1', 'Lag2']. The predictor variables to be used in the analysis.

    Returns:
    - None, but prints out the analysis results.
    """
    # Load the Smarket dataset
    Smarket = load_data('Smarket')

    # Prepare the data
    X_train, X_test, y_train, y_test = prepare_data(Smarket, predictors, 'Direction', split_year)

    # Initialize and train the QDA model
    qda = QDA()
    qda.fit(X_train, y_train)

    # Make predictions and evaluate the model
    predictions = qda.predict(X_test)
    accuracy = np.mean(predictions == y_test)
    print("Accuracy of QDA Model:", accuracy)
    print("Confusion Matrix:")
    print(confusion_table(predictions, y_test))

# Run the analysis
run_qda_analysis()

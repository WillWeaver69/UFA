# Import necessary libraries
import numpy as np
import statsmodels.api as sm
from ISLP import load_data
from ISLP.models import ModelSpec as MS, sklearn_sm, poly
from sklearn.model_selection import train_test_split, cross_validate, KFold, ShuffleSplit

# Function to load and split the dataset
def load_and_split_data(dataset, test_size, random_state):
    """
    Splits a dataset into training and validation sets.
    Training set is used to build the model, and the validation set is used to evaluate its performance.
    This split helps in assessing how the model will perform on unseen data.

    Parameters:
    dataset (DataFrame): Dataset to split.
    test_size (int or float): If int, represents the absolute number of test samples. 
                              If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the test split.
    random_state (int): Controls the shuffling applied to the data before applying the split for reproducibility.

    Returns:
    tuple: A tuple containing the training and validation sets.
    """
    return train_test_split(dataset, test_size=test_size, random_state=random_state)

# Function to evaluate model using Mean Squared Error (MSE)
def evalMSE(terms, response, train, test):
    """
    Evaluates the Mean Squared Error (MSE) of a model.
    MSE is a measure of the quality of an estimator—it is always non-negative, and values closer to zero are better.

    Parameters:
    terms (list): List of terms (predictors) to be used in the model.
    response (str): The response variable in the dataset.
    train (DataFrame): The training dataset.
    test (DataFrame): The testing/validation dataset.

    Returns:
    float: The MSE of the model.
    """
    mm = MS(terms)
    X_train = mm.fit_transform(train)
    y_train = train[response]
    X_test = mm.transform(test)
    y_test = test[response]
    results = sm.OLS(y_train, X_train).fit()
    test_pred = results.predict(X_test)
    return np.mean((y_test - test_pred)**2)

# Load the 'Auto' dataset
Auto = load_data('Auto')

# Load and split the 'Auto' dataset
Auto_train, Auto_valid = load_and_split_data(Auto, test_size=196, random_state=0)

# Evaluate MSE for different degrees of polynomial features
def evaluate_polynomial_models(train, valid, degrees, response='mpg', predictor='horsepower'):
    """
    Evaluates polynomial regression models of various degrees and calculates their MSE.
    Polynomial regression is a form of regression analysis in which the relationship 
    between the independent variable x and the dependent variable y is modeled as an nth degree polynomial.

    Parameters:
    train (DataFrame): The training dataset.
    valid (DataFrame): The validation dataset.
    degrees (int): The maximum degree of polynomial to evaluate.
    response (str): The response variable in the dataset.
    predictor (str): The predictor variable to be used in the polynomial transformation.

    Returns:
    np.array: An array containing the MSE for each polynomial degree.
    """
    MSE = np.zeros(degrees)
    for idx, degree in enumerate(range(1, degrees + 1)):
        MSE[idx] = evalMSE([poly(predictor, degree)], response, train, valid)
    return MSE

# Example usage: Evaluating polynomial models
MSE_values = evaluate_polynomial_models(Auto_train, Auto_valid, 3)

# Printing MSE values with more context
print("MSE for Polynomial Models (Degree 1 to 3):")
for i, mse in enumerate(MSE_values, 1):
    print(f"Degree {i}: MSE = {mse}")

# Function to perform cross-validation
def perform_cross_validation(model, X, Y, cv_method, n_splits=None, test_size=None, random_state=0):
    """
    Performs cross-validation on a given model.
    Cross-validation is a resampling procedure used to evaluate machine learning models on a limited data sample.
    The procedure has a single parameter called k that refers to the number of groups that a given data sample is to be split into.
    This approach avoids the problem of your model being too specific to your training data (overfitting).

    Parameters:
    model (object): The regression model to be evaluated.
    X (DataFrame or ndarray): The features of the dataset.
    Y (Series or ndarray): The response variable of the dataset.
    cv_method (str): The cross-validation method ('kfold' or 'shuffle_split').
    n_splits (int, optional): The number of folds/splits. Required if cv_method is 'kfold'.
    test_size (int or float, optional): The test set size. Required if cv_method is 'shuffle_split'.
    random_state (int): Controls the shuffling for reproducibility.

    Returns:
    dict: A dictionary containing the cross-validation results.
    """
    if cv_method == 'kfold':
        cv = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    elif cv_method == 'shuffle_split':
        cv = ShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=random_state)
    else:
        raise ValueError("Invalid cross-validation method. Choose 'kfold' or 'shuffle_split'.")

    return cross_validate(model, X, Y, cv=cv)

# Example usage of cross-validation
hp_model = sklearn_sm(sm.OLS, MS(['horsepower']))
X, Y = Auto.drop(columns=['mpg']), Auto['mpg']
cv_results = perform_cross_validation(hp_model, X, Y, cv_method='kfold', n_splits=10)

# Formatting Cross-Validation Results
print("\nCross-Validation Results:")
print("Fit Times:", cv_results['fit_time'])
print("Score Times:", cv_results['score_time'])
print("Test Scores (Negative MSE):", cv_results['test_score'])

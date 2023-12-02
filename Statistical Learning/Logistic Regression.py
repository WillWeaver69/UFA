import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
from ISLP import load_data  # Importing from the ISLP package

def prepare_data(data, target_column, drop_columns=None):
    """
    Prepares the dataset for analysis.

    Parameters:
    data (DataFrame): The dataset to be used.
    target_column (str): The name of the target variable in the dataset.
    drop_columns (list of str, optional): Columns to be dropped from the dataset.

    Returns:
    DataFrame: The processed dataset.
    """
    # Drop specified columns if any
    if drop_columns:
        data.drop(columns=drop_columns, inplace=True)

    # Ensure the target column exists
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in the dataset")

    return data

def fit_logistic_regression(data, target_column, test_size=0.3, random_state=None):
    """
    Fits a logistic regression model to the data.

    Parameters:
    data (DataFrame): The dataset to be used.
    target_column (str): The name of the target variable.
    test_size (float): The proportion of the dataset to include in the test split.
    random_state (int, optional): Controls the shuffling applied to the data before applying the split.

    Returns:
    dict: Dictionary containing model, predictions, accuracy, and other relevant information.
    """
    # Splitting the dataset into features and target
    X = data.drop(columns=[target_column])
    y = data[target_column]

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Fitting the logistic regression model
    model = sm.GLM(y_train, X_train, family=sm.families.Binomial())
    results = model.fit()

    # Making predictions on the test set
    predictions = results.predict(X_test)
    predicted_labels = predictions > 0.5

    # Evaluating the model
    conf_matrix = confusion_matrix(y_test, predicted_labels)
    accuracy = accuracy_score(y_test, predicted_labels)

    # Prepare the results
    result_dict = {
        "model": results,
        "predictions": predictions,
        "predicted_labels": predicted_labels,
        "confusion_matrix": conf_matrix,
        "accuracy": accuracy,
        "test_data": (X_test, y_test)
    }

    return result_dict

def plot_confusion_matrix(conf_matrix, labels=["Negative", "Positive"]):
    """
    Plots a confusion matrix.

    Parameters:
    conf_matrix (array-like): The confusion matrix to plot.
    labels (list): The labels for the classes.

    Returns:
    None: The function only creates a plot.
    """
    fig, ax = plt.subplots()
    im = ax.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(conf_matrix.shape[1]),
           yticks=np.arange(conf_matrix.shape[0]),
           xticklabels=labels, yticklabels=labels,
           title='Confusion Matrix',
           ylabel='True label',
           xlabel='Predicted label')

    # Loop over data dimensions and create text annotations.
    fmt = 'd'
    thresh = conf_matrix.max() / 2.
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax.text(j, i, format(conf_matrix[i, j], fmt),
                    ha="center", va="center",
                    color="white" if conf_matrix[i, j] > thresh else "black")
    fig.tight_layout()

def main():
    """
    Main function to run the analysis.
    """
    # Load the Smarket data from the ISLP package
    Smarket = load_data('Smarket')

    # Prepare the data (assuming 'Direction' is the target variable)
    prepared_data = prepare_data(Smarket, 'Direction', drop_columns=['Today', 'Year'])

    # Convert the target variable to binary if it's categorical
    prepared_data['Direction'] = prepared_data['Direction'].apply(lambda x: 1 if x == 'Up' else 0)

    # Fit the logistic regression model
    result = fit_logistic_regression(prepared_data, 'Direction')

    # Print results
    print("Model Summary:\n", result["model"].summary())
    print("\nAccuracy on Test Data:", result["accuracy"])

    # Plot confusion matrix
    plot_confusion_matrix(result["confusion_matrix"], labels=["Down", "Up"])

if __name__ == "__main__":
    main()

import numpy as np
import pandas as pd
from ISLP import load_data, confusion_table
from ISLP.models import ModelSpec as MS
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

def lda_analysis(data, features, target, train_condition, lda_params=None):
    """
    Perform Linear Discriminant Analysis on the given dataset.

    Parameters:
    - data (pd.DataFrame): The dataset to analyze.
    - features (list): List of feature column names to be used for the model.
    - target (str): The name of the target column.
    - train_condition (pd.Series): A boolean Series to split the data into training and test sets.
    - lda_params (dict, optional): Additional parameters for the LDA model. Defaults to None.

    Returns:
    - dict: A dictionary containing the LDA model, predictions, probabilities, and evaluation metrics.
    """

    # Preprocess data: Select columns specified in 'features' and 'target'
    X = data[features]
    y = data[target]

    # Split data: Use 'train_condition' to create training and testing sets
    X_train, X_test = X[train_condition], X[~train_condition]
    y_train, y_test = y[train_condition], y[~train_condition]

    # Initialize and fit the LDA model: Use 'lda_params' for custom model parameters
    lda = LDA(**lda_params) if lda_params else LDA()
    lda.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = lda.predict(X_test)
    prediction_probs = lda.predict_proba(X_test)

    # Evaluate model: Confusion matrix and accuracy to understand model performance
    confusion_matrix = confusion_table(predictions, y_test)
    accuracy = np.mean(predictions == y_test)

    return {
        "model": lda,
        "predictions": predictions,
        "prediction_probs": prediction_probs,
        "confusion_matrix": confusion_matrix,
        "accuracy": accuracy
    }

# Example usage with 'Smarket' dataset
if __name__ == "__main__":
    # Load data: Replace 'Smarket' with any other dataset as required
    Smarket = load_data('Smarket')

    # Define features and target: Change these according to the new dataset
    features = ['Lag1', 'Lag2']
    target = 'Direction'

    # Define training condition: Modify this condition based on the dataset and analysis needs
    train_condition = Smarket['Year'] < 2005

    # Perform LDA analysis: Call the function with the specified parameters
    lda_results = lda_analysis(Smarket, features, target, train_condition)

    # Display results: Outputs the model, confusion matrix, accuracy, and predictions
    print("LDA Model:", lda_results["model"])
    print("Confusion Matrix:\n", lda_results["confusion_matrix"])
    print("Model Accuracy:", lda_results["accuracy"])
    print("Predictions:", lda_results["predictions"])

# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Custom library for loading datasets and handling specific functionalities.
from ISLP import load_data, confusion_table

# Load the dataset. In this example, we are using the 'Caravan' dataset.
# Replace 'Caravan' with any other dataset name as needed.
Caravan = load_data('Caravan')

# Extract the target variable 'Purchase' which we aim to predict.
Purchase = Caravan['Purchase']

# Display the distribution of values in the target variable.
# This helps in understanding the balance of classes in the dataset.
print(Purchase.value_counts())

# Prepare the features dataset by dropping the target variable 'Purchase'.
# This step isolates the features that will be used to train the model.
feature_df = Caravan.drop(columns=['Purchase'])

# Standardize the features using StandardScaler.
# This is crucial for distance-based algorithms like KNN to work effectively.
scaler = StandardScaler()
scaler.fit(feature_df)
X_std = scaler.transform(feature_df)

# Convert the standardized features back to a DataFrame.
# This makes the data easier to work with in the later stages.
feature_std = pd.DataFrame(X_std, columns=feature_df.columns)

# Split the dataset into training and test sets.
# The test_size parameter can be adjusted based on the size of the dataset.
(X_train, X_test, y_train, y_test) = train_test_split(feature_std, Purchase, test_size=1000, random_state=0)

# Initialize the K-Nearest Neighbors classifier with 1 neighbor.
knn1 = KNeighborsClassifier(n_neighbors=1)
knn1.fit(X_train, y_train)

# Make predictions on the test set.
knn1_pred = knn1.predict(X_test)

# Display the error rate and accuracy of the model.
print("Error rate:", np.mean(y_test != knn1_pred))
print("Accuracy:", np.mean(y_test == knn1_pred))

# Generate and display the confusion table using the custom function from ISLP.
print("Confusion Table for K=1:")
print(confusion_table(knn1_pred, y_test))

# Iterate over different values of K to find the optimal number of neighbors.
for K in range(1, 6):
    knn = KNeighborsClassifier(n_neighbors=K)
    knn.fit(X_train, y_train)

    # Make predictions on the test set.
    knn_pred = knn.predict(X_test)

    # Calculate and print the accuracy for each K.
    accuracy = accuracy_score(y_test, knn_pred)
    print(f'K={K}: Accuracy: {accuracy:.2%}')

    # Generate and display the confusion table for each K value.
    # This table provides a detailed breakdown of the prediction results.
    print(f"Confusion Table for K={K}:")
    print(confusion_table(knn_pred, y_test))

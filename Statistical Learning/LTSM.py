class TimeSeriesPreprocessor:
    """
    Preprocesses time series data for LSTM input. This involves scaling the data
    and creating sequences that LSTM models can use for training.
    
    Theoretical Underpinning:
    - LSTM networks require input data in a specific format usually involving sequences of data.
    - Normalizing or standardizing data helps in speeding up the training process and 
      reducing the chances of weight initialization affecting the training significantly.
    """
    def __init__(self, sequence_length=5):
        """
        Args:
            sequence_length (int): The number of time steps in each input sequence.
        """
        self.sequence_length = sequence_length
        self.scaler = StandardScaler()

    def fit_transform(self, data):
        """
        Fits the scaler to the data and transforms the data into sequences.
        Args:
            data (np.array): Time series data.
        Returns:
            X (np.array): Transformed sequences for model input.
            y (np.array): Corresponding labels for each sequence.
        """
        # Scaling
        data_scaled = self.scaler.fit_transform(data.reshape(-1, 1)).flatten()

        # Creating sequences
        X, y = [], []
        for i in range(len(data_scaled) - self.sequence_length):
            X.append(data_scaled[i:(i + self.sequence_length)])
            y.append(data_scaled[i + self.sequence_length])
        return np.array(X), np.array(y)

class CustomLSTM(nn.Module):
    """
    Customizable LSTM model for time series forecasting. 
    
    Theoretical Underpinning:
    - LSTM units are used due to their ability to capture long-term dependencies and 
      handle the vanishing gradient problem common in traditional RNNs.
    - The model can be customized to adjust the capacity (complexity) and control overfitting.
    """
    def __init__(self, input_size, hidden_size, num_layers, dropout):
        """
        Args:
            input_size (int): Number of features in the input.
            hidden_size (int): Number of features in the hidden state.
            num_layers (int): Number of recurrent layers in the LSTM.
            dropout (float): Dropout rate for regularization.
        """
        super(CustomLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, dropout=dropout, batch_first=True)
        self.linear = nn.Linear(hidden_size, 1)

    def forward(self, x):
        """
        Forward pass through the model.
        Args:
            x (Tensor): Input tensor for the LSTM model.
        Returns:
            Tensor: Output tensor from the model.
        """
        lstm_out, _ = self.lstm(x)
        output = self.linear(lstm_out[:, -1, :])
        return output

def train_model(model, train_loader, val_loader=None, num_epochs=10, learning_rate=0.01):
    """
    Train the LSTM model with optional validation.
    
    Theoretical Underpinning:
    - Training involves adjusting model weights to minimize the error on the training dataset.
    - Validation during training helps in monitoring the model's performance and preventing overfitting.
    - The learning rate controls how drastically model weights are updated during training.
    - Epochs determine how many times the model will see the entire dataset.
    """
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        # Training
        model.train()
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

        # Validation
        if val_loader:
            model.eval()
            with torch.no_grad():
                val_loss = sum(criterion(model(inputs), targets).item() for inputs, targets in val_loader)
            val_loss /= len(val_loader)
            print(f'Epoch {epoch+1}/{num_epochs}, Train Loss: {loss.item()}, Val Loss: {val_loss}')

    return model
def forecast_time_series(data, sequence_length=5, hidden_size=50, num_layers=1, dropout=0.2, num_epochs=10, learning_rate=0.01):
    """
    Forecast a time series using a customizable LSTM model.
    
    Theoretical Underpinning:
    - This function encapsulates the entire process from data preprocessing to model training and prediction.
    - It allows customization of the LSTM model and training process to suit different types of time series data.
    """
    # Preprocess the data
    preprocessor = TimeSeriesPreprocessor(sequence_length)
    X, y = preprocessor.fit_transform(data)
    train_size = int(len(X) * 0.8)
    train_data = TensorDataset(torch.from_numpy(X[:train_size]).float(), torch.from_numpy(y[:train_size]).float())
    val_data = TensorDataset(torch.from_numpy(X[train_size:]).float(), torch.from_numpy(y[train_size:]).float())
    train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=64)

    # Initialize and train the LSTM model
    model = CustomLSTM(sequence_length, hidden_size, num_layers, dropout)
    trained_model = train_model(model, train_loader, val_loader, num_epochs, learning_rate)

    # Predictions
    model.eval()
    with torch.no_grad():
        test_predictions = model(torch.from_numpy(X[train_size:]).float()).numpy()
    return preprocessor.inverse_transform(test_predictions)

# Example usage:
# data = np.loadtxt('your_time_series_data.csv')
# predictions = forecast_time_series(data)

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def fetch_gdelt_data(keywords, start_date, end_date):
    """
    Fetches news volume data for the given keywords within a specified date range from the GDELT API.
    Parameters:
    - keywords (str): A string of keywords to search for, formatted for the GDELT API query.
    - start_date (str): The start date for the data query in "YYYYMMDDHHMMSS" format.
    - end_date (str): The end date for the data query in "YYYYMMDDHHMMSS" format.
    Returns:
    - dict: A dictionary containing the JSON response from the GDELT API if the request is successful; None otherwise.
    """
    # GDELT API endpoint for document retrieval.
    url = 'https://api.gdeltproject.org/api/v2/doc/doc'
    # Parameters for the API request.
    params = {
        'query': keywords,
        'mode': 'TimelineVolRaw',
        'format': 'json',
        'startdatetime': start_date,
        'enddatetime': end_date
    }
    # Attempt to fetch data from the GDELT API.
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"HTTP Error: {response.status_code}")
            print("Response content:", response.text)
            return None
    except Exception as e:
        print(f"Request Error: {e}")
        return None

def plot_data(*dataframes, labels=None):
    """
    Plots multiple series of news volume data from given DataFrames using Matplotlib.
    Parameters:
    - *dataframes: A sequence of Pandas DataFrames each with a 'date' column and a 'value' column.
    - labels (list of str): A list of labels for the DataFrames. Must be the same length as dataframes.
    """
    plt.figure(figsize=(10, 6))
    # If labels are not provided or their length doesn't match the number of DataFrames, create default labels.
    if not labels or len(labels) != len(dataframes):
        labels = [f"Series {i+1}" for i in range(len(dataframes))]
    # Plot each DataFrame with its corresponding label.
    for df, label in zip(dataframes, labels):
        plt.plot(df['date'], df['value'], linestyle='-', label=label)
    # Formatting the plot with title, labels, and grid.
    plt.title("GDELT Data Plot Comparison")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    # Rotate the x-axis date labels for better readability.
    plt.xticks(rotation=45)
    # Format the x-axis to display dates properly.
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=15))  # Adjust interval as needed.
    # Display the plot.
    plt.show()

# Example usage:
if __name__ == "__main__":
    # Define your search parameters.
    keywords = "(Inflation OR interest rates)"
    start_date = "20230101010101"
    end_date = "20231217010101"
    # Fetch data from GDELT.
    fetched_data = fetch_gdelt_data(keywords, start_date, end_date)
    # Prepare the DataFrame.
    if fetched_data:
        # Extract the list of data items and create a DataFrame.
        data_items = fetched_data['timeline'][0]['data']
        df = pd.DataFrame(data_items)
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%dT%H%M%SZ')
        # Plot the data.
        # You can add more DataFrames as arguments to the plot_data function.
        # For example, to add another search term, fetch its data, prepare another DataFrame,
        # and add it as another argument to the plot_data function.
        # Ensure you provide a list of labels corresponding to the DataFrames.
        plot_data(df, labels=[f"Volume of News articles that mention{keywords}"])
    else:
        print("No data fetched or unable to parse the data")

import wbgapi as wb

# Function to search indicators based on a query
def search_indicators(query):
    all_indicators = wb.series.list()
    filtered_indicators = {ind['id']: ind['value'] for ind in all_indicators if query.lower() in ind['value'].lower()}
    return filtered_indicators

# Function for the user to select an indicator
def select_indicator():
    while True:
        query = input("Enter keyword to search for indicators: ")
        results = search_indicators(query)

        if not results:
            print("No matching indicators found. Try again.")
            continue

        for i, (code, desc) in enumerate(results.items()):
            print(f"{i + 1}. {desc} [{code}]")

        selection = input("Select an indicator (number): ")
        if selection.isdigit() and 0 < int(selection) <= len(results):
            selected_code = list(results.keys())[int(selection) - 1]
            return selected_code

        print("Invalid selection. Please try again.")

# Function for the user to select a timeframe
def select_timeframe():
    start_year = input("Enter start year (or 'all' for full range): ")
    end_year = input("Enter end year (or 'all' for full range): ")

    if start_year.lower() == 'all' or end_year.lower() == 'all':
        return (None, None)  # Full range

    return (int(start_year), int(end_year))

# Function to fetch data from the World Bank API
def fetch_data(indicator, start, end):
    if start is None or end is None:
        data = wb.data.DataFrame(indicator)
    else:
        data = wb.data.DataFrame(indicator, time=range(start, end + 1))

    return data

# Main execution
selected_indicator = select_indicator()
start_year, end_year = select_timeframe()
data = fetch_data(selected_indicator, start_year, end_year)
print(data)

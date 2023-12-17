def calculate_effectivetaxrate_dividends(taxrate_corporate, taxrate_individual):
    """Since a dollar of earnings distributed as dividends is first taxed at the corporate level, with the after-corporate-tax amount taxed at the individual level, we can calculate the total effective tax rate as per the below
    """"
    effectivetaxrate_dividends = taxrate_corporate + (1 - taxrate_corporate) * (taxrate_individual)
    
    return effectivetaxrate_dividends


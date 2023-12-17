def stockprice_delta_exdividend(dividend, taxrate_dividend, taxrate_capitalgains):
    """In the presence of differential tax rates on dividends and capital gains, investors would be indifferent between receiving $D in dividends or 
    the after - tax dividend (1 - the capital gain tax rat). As such, the expected change in the price of a stock once it goes ex dividend can be computed as below."""
    
    stock_price_delta_exdividend = (dividend * (1 - taxrate_dividend)) / (1 -taxrate_capitalgains)
    return stock_price_delta_exdividend

#Example usage
stockprice_delta_exdividend(12, 0.3, 0.15)
    

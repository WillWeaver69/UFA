def ggm_fundamentalvalue_and_justified_price_earnings_ratio(d0,g,r,earnings):
    """
        Parameters:
        d0: dividend just paid
        g: growth rate
        r: required return
        earnings: Use current period earnings to arrive at the justified trailing P/E ratio, or expected future period earnings to arrive at the justified leading P/E 
        """

    
    
    
    
    def gordon_growth_model(d0,g,r):
        """The Gordon Growth Model (GGM) is a specification of the general dividend discount model (DDM).
        DDMs are a method of equity valuation that define cash flow as the dividends to be received by the shareholders.
        The primary advantage of using dividends as the definition of cash flow is that it is theoretically justified.
        Shareholder's investment today is worth the present value of the future cash flows he expects to receive, and
        ultimately he will be repaid in the form of dividend.
        An additional advantage of using dividends as a measure of cash flow is that dividends are less volatile
        than other measures, and therefore the value estimates derived from DDMs are less volatile and reflect the long-term earning potential of the company.
        Dividends are appropriate as a measure of cash flow in the following cases:
        - The company has a history of dividend payments
        - The dividend policy is clear and related to the earnings of the firm
        - The perspective is that of a minority shareholder
        The GGM assumes that:
        - The firm expectes to pay a dividend D1, in one year
        - Dividends grow indefinitely at a constant rate, g (which may be less than 0)
        - The growth rate, g, is less than the required return, r
        dividends increase at a constant rate indefinitely.
        Parameters:
        d0: dividend just paid
        g: growth rate
        r: required return
        """

        #Calculate D1, the value of the dividend just paid after 1 period of growth
        d1 = d0 * (1+g)

        #Calculate the fundamental terminal value of the stock

        v0 = d1 / (r - g)

        return v0

    def price_to_earnings(v0, earnings, g):
        """ The price to earnings (P/E) ratio is the most commonly used relative valuation indicator.
        The 2 most common forms are the leading P/E, which is based on the earnings forecast for the next
        period, and the trailing P/E, which is based on the earnings for the previous period. Both can
        be derived from the DDM. Taking the Gordon growth model, and dividing both sides by earnings per share, we 
        arrive at the justified price to earnings ratio. By comparing the justified P/E ratio against the
        market P/E ratio, we can have a sense as to whether a stock is correctly valued.
        Params:
        v0: The fundamental value of the stock calculated using the GGM
        earnings: Use current period earnings to arrive at the justified trailing P/E ratio, or expected future period earnings to arrive at the justified leading P/E 
        g: dividend growth rate
        """
        

        price_to_earnings_trailing = v0 / earnings

        price_to_earnings_leading = price_to_earnings_trailing / (1 + g)

        return price_to_earnings_trailing, price_to_earnings_leading
    
    v0 = gordon_growth_model(d0,g,r)
    return price_to_earnings(v0, earnings, g)

# Example usage
ggm_fundamentalvalue_and_justified_price_earnings_ratio(1.5,0.035,0.106,3)


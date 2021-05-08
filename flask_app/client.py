import yfinance as yf

class Stock(object) :
    def __init__(self, stock_json):
        self.symbol = stock_json["symbol"]
        self.name = stock_json["shortName"]
        self.long_business_summary = stock_json["longBusinessSummary"]
        self.sector = stock_json["sector"]
        self.industry = stock_json["industry"]
        self.market_cap = stock_json['marketCap']

        self.open = stock_json["open"]
        self.previous_close = stock_json["previousClose"]
        self.regular_market_day_high = stock_json['regularMarketDayHigh']
        self.regular_market_day_low = stock_json['regularMarketDayLow']
        self.dayHigh = stock_json['dayHigh']
        self.dayLow = stock_json['dayLow']

        self.last_dividend_value = stock_json["lastDividendValue"]
        self.divdend_rate = stock_json['dividendRate']
        self.profitMargins = stock_json['profitMargins']

        self.logo_url = stock_json['logo_url']
    
    def __str__(self):
        return f"ticker: {self.symbol}, name: {self.name}, open: {self.open}, logo: {self.logo_url}"

class StockClient ():

    def search (self, stock_ticker):
        stock = yf.Ticker(stock_ticker.upper())
        data = stock.info
        if data['logo_url'] == '' :
            raise ValueError('Invalid ticker')
        return Stock(data)


## -- Example usage -- ###
if __name__ == "__main__":
    import os

    client = StockClient()

    stock = client.search("poop")

    print(stock)

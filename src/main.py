from src.gui import TradingApp

if __name__ == '__main__':
    symbols = ["AAPL","MSFT","GOOG","AMZN","TSLA","NFLX","FB","NVDA","BABA","JPM"]
    app = TradingApp(symbols)
    app.mainloop()
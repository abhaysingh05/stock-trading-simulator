# Multi-Stock Trading Simulator

A GUI-based stock trading game with simulated candlestick charts, buy/sell/short orders, and portfolio tracking.

## Project Structure
```
stock-trading-simulator/
├── README.md           # this file, including structure
├── LICENSE             # MIT license
├── requirements.txt    # Python dependencies
├── src/                # application code
│   ├── simulation.py   # StockSimulator back-end logic
│   ├── gui.py          # TradingApp front-end UI
│   └── main.py         # entry-point
└── tests/              # automated tests
    ├── test_simulation.py
    └── test_gui.py
```

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
python -m src.main
```

## 📽️ Demo

![Stock Trading Simulator Demo](assets/stock_demo.gif)

# License

MIT License (see [LICENSE](LICENSE))
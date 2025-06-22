import pytest
from src.gui import TradingApp

def test_app_init(qtbot):
    symbols = ['A','B']
    app = TradingApp(symbols)
    assert app.selected in symbols
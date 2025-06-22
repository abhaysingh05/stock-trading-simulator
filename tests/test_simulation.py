import pytest
from src.simulation import StockSimulator

@ pytest.fixture
def sim():
    return StockSimulator('TEST', days=5)

def test_advance_and_price(sim):
    assert sim.current_day == 0
    sim.advance()
    assert sim.current_day == 1
    price = sim.price()
    assert isinstance(price, float)

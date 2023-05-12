import pytest
from aemo_price_script.aemo_price_demand import gather_year_data

def test_gather_year_data():
    result = gather_year_data(2020)
    with open("test.txt", 'w') as f:
        f.write(result)
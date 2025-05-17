import pytest
import numpy as np
from core.calculators import PriceIndexCalculator


class TestPriceIndexCalculator:
    @pytest.fixture
    def calculator(self):
        calc = PriceIndexCalculator()
        calc.base_prices = {'1001': 50.0, '1002': 30.0}  # 模拟基期价格
        return calc

    def test_index_calculation(self, calculator):
        # 测试数据：价格涨20%
        prices = np.array([60.0, 60.0])
        sales = np.array([100, 200])

        result = calculator.calculate_daily_index(
            '2023-01-01',
            {'category_id': '1001', 'price': prices, 'sales': sales}
        )

        assert result['price_index'] == pytest.approx(120.0)  # 期望指数=120
        assert result['weighted_price'] == pytest.approx(60.0)
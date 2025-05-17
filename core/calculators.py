import numpy as np
from typing import Dict
from configs.settings import Config
from connectors.clickhouse_connector import ClickHouseConnector


class PriceIndexCalculator:
    def __init__(self):
        self.ch_conn = ClickHouseConnector()
        self.base_prices = self._load_base_prices()

    def _load_base_prices(self) -> Dict[str, float]:
        """从ClickHouse加载基期价格"""
        query = """
        SELECT 
            category_id,
            sum(price * sales) / sum(sales) AS base_price
        FROM fact_price
        WHERE toYear(date) = {base_year:UInt16}
        GROUP BY category_id
        """
        result = self.ch_conn.execute_query(
            query, {'base_year': Config.BASE_YEAR})
        return dict(zip(result['category_id'], result['base_price']))

    def calculate_daily_index(self, date, category_data) -> dict:
        """
        计算单日分类价格指数
        返回: {
            'date': date,
            'category_id': str,
            'weighted_price': float,
            'price_index': float
        }
        """
        category_id = category_data['category_id'].iloc[0]
        prices = category_data['price'].values
        sales = category_data['sales'].values

        # 计算加权平均价格
        weighted_price = np.sum(prices * sales) / np.sum(sales)

        # 计算价格指数
        base_price = self.base_prices.get(category_id, 1.0)
        price_index = (weighted_price / base_price) * Config.INDEX_SCALE

        return {
            'date': date,
            'category_id': category_id,
            'weighted_price': float(weighted_price),
            'price_index': float(price_index)
        }
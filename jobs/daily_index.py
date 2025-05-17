import pandas as pd
from datetime import datetime, timedelta
from core.data_cleaner import DataCleaner
from core.calculators import PriceIndexCalculator
from connectors.oss_connector import OSSConnector
from connectors.clickhouse_connector import ClickHouseConnector


class DailyIndexJob:
    def __init__(self):
        self.oss_conn = OSSConnector()
        self.ch_conn = ClickHouseConnector()
        self.cleaner = DataCleaner()
        self.calculator = PriceIndexCalculator()

    def run(self, process_date: datetime = None):
        """执行日指数计算任务"""
        # 1. 确定处理日期（默认前一天）
        if not process_date:
            process_date = datetime.now() - timedelta(days=1)

        # 2. 从OSS加载原始数据
        raw_df = self._load_raw_data(process_date)

        # 3. 数据清洗
        clean_df = self.cleaner.clean_price_data(raw_df)

        # 4. 计算指数
        results = []
        for category_id, group in clean_df.groupby('category_id'):
            result = self.calculator.calculate_daily_index(
                process_date.date(), group)
            results.append(result)

        # 5. 存储结果
        if results:
            self.ch_conn.batch_insert('idx_price_daily', results)

        return len(results)

    def _load_raw_data(self, date: datetime) -> pd.DataFrame:
        """从OSS加载指定日期的数据"""
        object_path = f"raw/{date:%Y/%m/%d}/price_data.csv"
        return self.oss_conn.read_csv(object_path)
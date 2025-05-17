from datetime import datetime, timedelta
from core.data_cleaner import DataCleaner
from core.calculators import PriceIndexCalculator
from connectors.oss_connector import OSSConnector
from connectors.clickhouse_connector import ClickHouseConnector
from utils.date_utils import get_previous_day


class HistoryBackfillJob:
    def __init__(self):
        self.oss_conn = OSSConnector()
        self.ch_conn = ClickHouseConnector()
        self.cleaner = DataCleaner()
        self.calculator = PriceIndexCalculator()

    def run(self, start_date, end_date):
        """回填指定日期范围的数据"""
        current_date = start_date
        while current_date <= end_date:
            try:
                self.process_single_day(current_date)
            except Exception as e:
                print(f"Failed to process {current_date}: {str(e)}")
            current_date += timedelta(days=1)

    def process_single_day(self, date):
        """处理单日数据"""
        raw_df = self._load_raw_data(date)
        clean_df = self.cleaner.clean_price_data(raw_df)

        results = []
        for category_id, group in clean_df.groupby('category_id'):
            result = self.calculator.calculate_daily_index(date, group)
            results.append(result)

        if results:
            self.ch_conn.batch_insert('idx_price_daily', results)

        return len(results)

    def _load_raw_data(self, date):
        """加载历史数据"""
        object_path = f"raw/{date:%Y/%m/%d}/price_data.csv"
        return self.oss_conn.read_csv(object_path)
import pandas as pd
import numpy as np
from datetime import datetime


class DataCleaner:
    @staticmethod
    def clean_price_data(raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        数据清洗流程：
        1. 处理缺失值
        2. 过滤异常值
        3. 类型转换
        """
        # 复制数据避免修改原始数据
        df = raw_df.copy()

        # 1. 处理缺失值
        df = df.dropna(subset=['price', 'sales', 'category_id'])

        # 2. 过滤异常值
        df = df[
            (df['price'] > 0) &
            (df['price'] < 1e6) &  # 价格上限100万
            (df['sales'] < 1e5)  # 销量上限10万
            ]

        # 3. 类型转换
        df['date'] = pd.to_datetime(df['date']).dt.date
        df['price'] = df['price'].astype(np.float32)
        df['sales'] = df['sales'].astype(np.uint32)

        return df
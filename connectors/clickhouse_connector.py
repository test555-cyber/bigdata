import clickhouse_connect
from configs.settings import Config


class ClickHouseConnector:
    def __init__(self):
        self.client = clickhouse_connect.get_client(
            host=Config.CH_HOST,
            port=Config.CH_PORT,
            username=Config.CH_USER,
            password=Config.CH_PASSWORD
        )

    def execute_query(self, query: str, params=None):
        """执行查询返回DataFrame"""
        return self.client.query_df(query, parameters=params)

    def insert_data(self, table_name: str, data: dict):
        """插入单条数据"""
        self.client.insert(table_name, [data])

    def batch_insert(self, table_name: str, data: list):
        """批量插入数据"""
        self.client.insert(table_name, data)
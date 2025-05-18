import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    # OSS配置
    OSS_ACCESS_KEY = os.getenv('OSS_ACCESS_KEY', '**')
    OSS_SECRET_KEY = os.getenv('OSS_SECRET_KEY', '**')
    OSS_ENDPOINT = 'https://oss-cn-hangzhou.aliyuncs.com'
    OSS_BUCKET = 'maiyadexiangqi'

    # ClickHouse配置
    CH_HOST = os.getenv('CLICKHOUSE_HOST', 'localhost')
    CH_PORT = 8123
    CH_USER = 'default'
    CH_PASSWORD = ''

    # 计算参数
    BASE_YEAR = 2020
    INDEX_SCALE = 100  # 指数基数
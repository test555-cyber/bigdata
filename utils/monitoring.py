# utils/monitoring.py
import time  # 添加缺失的导入
from prometheus_client import Counter, Gauge
from utils.logger import setup_logger

logger = setup_logger('monitoring')

# 定义监控指标
PROCESSED_RECORDS = Counter(
    'price_index_processed_records',
    'Number of processed price records',
    ['category']  # 添加标签维度
)

CALCULATION_TIME = Gauge(
    'price_index_calculation_seconds',
    'Time spent calculating indices',
    ['calculation_type']
)


def record_metrics(start_time: float, record_count: int, category: str = None):
    """
    记录处理指标
    :param start_time: time.time()获取的开始时间戳
    :param record_count: 处理的记录数
    :param category: 商品分类(可选)
    """
    duration = time.time() - start_time

    # 记录带标签的指标
    labels = {'category': category or 'all'}
    CALCULATION_TIME.labels(calculation_type='daily').set(duration)
    PROCESSED_RECORDS.labels(**labels).inc(record_count)

    logger.info(
        f"Processed {record_count} {category or ''} records "
        f"in {duration:.2f} seconds"
    )


def start_timer() -> float:
    """返回当前时间戳用于计算耗时"""
    return time.time()
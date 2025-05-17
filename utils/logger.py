import logging
from configs.settings import BASE_DIR


def setup_logger(name):
    """配置日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 创建文件handler
    log_file = BASE_DIR / 'logs' / f'{name}.log'
    log_file.parent.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    logger.addHandler(file_handler)
    return logger
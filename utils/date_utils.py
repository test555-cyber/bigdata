from datetime import datetime, timedelta

def get_previous_day(reference_date=None):
    """获取前一天日期"""
    if reference_date is None:
        reference_date = datetime.now()
    return (reference_date - timedelta(days=1)).date()

def format_oss_path(date_obj):
    """生成OSS路径格式"""
    return date_obj.strftime("%Y/%m/%d")
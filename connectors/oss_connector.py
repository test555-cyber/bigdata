import oss2
import pandas as pd
from configs.settings import Config


class OSSConnector:
    def __init__(self):
        self.auth = oss2.Auth(Config.OSS_ACCESS_KEY, Config.OSS_SECRET_KEY)
        self.bucket = oss2.Bucket(
            self.auth, Config.OSS_ENDPOINT, Config.OSS_BUCKET)

    def read_csv(self, object_path: str) -> pd.DataFrame:
        """从OSS读取CSV文件"""
        try:
            obj = self.bucket.get_object(object_path)
            return pd.read_csv(obj)
        except oss2.exceptions.NoSuchKey:
            raise FileNotFoundError(f"OSS object not found: {object_path}")

    def write_parquet(self, df: pd.DataFrame, object_path: str):
        """写入Parquet到OSS"""
        import io
        buffer = io.BytesIO()
        df.to_parquet(buffer)
        self.bucket.put_object(object_path, buffer.getvalue())
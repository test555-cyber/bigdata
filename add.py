import os
import pandas as pd
# 指定 daily_price 文件夹路径
folder_path = '../data/daily_price'  # 请修改为你的实际路径
output_file = '../data/merged_daily_prices.csv'
# 获取所有 CSV 文件名
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
# 存储所有 DataFrame 的列表
dataframes = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # 如果 utf-8 解码失败，尝试 gbk
        df = pd.read_csv(file_path, encoding='gbk')

    dataframes.append(df)
# 合并所有 DataFrame
merged_df = pd.concat(dataframes, ignore_index=True)
# 写入合并后的 CSV 文件（使用 UTF-8 编码）
merged_df.to_csv('merged_daily_prices.csv', index=False, encoding='utf-8')
print(f"已合并 {len(csv_files)} 个文件，保存为 merged_daily_prices.csv")

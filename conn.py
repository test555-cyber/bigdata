import os
import chardet
import shutil
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read(10000)
    result = chardet.detect(rawdata)
    return result['encoding']
def convert_file_to_utf8(source_path, target_path):
    original_encoding = detect_encoding(source_path)
    if not original_encoding:
        print(f"无法检测编码: {source_path}")
        return
    try:
        with open(source_path, 'r', encoding=original_encoding, errors='ignore') as infile:
            content = infile.read()

        os.makedirs(os.path.dirname(target_path), exist_ok=True)  # 创建目标文件夹
        with open(target_path, 'w', encoding='utf-8') as outfile:
            outfile.write(content)
        print(f"转换成功: {source_path} → {target_path}")
    except Exception as e:
        print(f"转换失败: {source_path}，错误: {e}")
def convert_all_csvs_to_utf8(source_root, target_root):
    for dirpath, _, filenames in os.walk(source_root):
        for filename in filenames:
            if filename.lower().endswith('.csv'):
                source_file = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(source_file, source_root)
                target_file = os.path.join(target_root, relative_path)
                convert_file_to_utf8(source_file, target_file)
if __name__ == "__main__":
    source_folder = "../data"         # 原始csv文件所在根目录
    target_folder = "../data"  # 转换后的csv输出目录

    convert_all_csvs_to_utf8(source_folder, target_folder)

# 电商价格指数计算系统

[![Python Version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Airflow Version](https://img.shields.io/badge/Airflow-2.10.1-brightgreen)](https://airflow.apache.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

基于电商平台数据的高频价格指数计算系统，利用Apache Airflow实现自动化数据处理流水线。

## 项目概述

### 核心功能
- 🕒 **日粒度计算**：T+1模式计算每日价格指数
- 📊 **多维度分析**：支持分类指数和综合指数
- ⚡ **高性能处理**：单日千万级数据处理能力
- 📈 **可视化监控**：集成Prometheus/Grafana监控看板

### 技术栈
| 组件              | 技术选型                     |
|-------------------|----------------------------|
| **工作流引擎**    | Apache Airflow 3.0         |
| **数据存储**      | ClickHouse + OSS           |
| **计算框架**      | Pandas + NumPy             |
| **可视化**        | Quick BI / Matplotlib      |
| **监控**          | Prometheus + Grafana       |

## 快速开始

### 环境准备
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置文件
复制示例配置并修改：
```bash
cp configs/settings.example.py configs/settings.py
```

### 运行计算任务
```bash
# 执行单日计算
python main.py daily --date 2023-05-01

# 历史数据回填
python main.py backfill 2023-01-01 2023-05-31
```

## 项目结构
```
price-index-system/
├── configs/               # 配置文件
├── connectors/            # 数据连接器
├── core/                  # 核心计算逻辑
├── dags/                  # Airflow DAG定义
├── jobs/                  # 批处理任务
├── tests/                 # 单元测试
├── utils/                 # 工具类
├── requirements.txt       # 依赖清单
└── main.py                # 主入口
```

## 核心算法

### 价格指数公式
$$
\text{PriceIndex}_t = \left( \frac{\sum (P_{i,t} \times Q_{i,t})}{\sum (P_{i,base} \times Q_{i,t})} \right) \times 100
$$

### 计算流程
1. **数据清洗**：处理缺失值和异常值
2. **权重计算**：按销量加权平均
3. **基期对比**：以2020年为基准年(100点)

## 生产部署

### Airflow配置
```ini
# airflow.cfg
[core]
dags_folder = /opt/airflow/dags
parallelism = 32

[scheduler]
max_threads = 8
```

## 扩展开发

### 自定义计算器
继承 `BaseCalculator` 实现新算法：
```python
from core.calculators import BaseCalculator

class CustomCalculator(BaseCalculator):
    def calculate(self, data):
        # 实现自定义逻辑
        return custom_index
```

## 许可证
[MIT License](LICENSE) © 2023 数据科学团队

# raw / master から必要なCSVを読み込む
# 列名をそろえる
# DataFrameを返す

import pandas as pd
from pathlib import Path


def load_sales_data(data_dir: Path) -> pd.DataFrame:
    return pd.read_csv(data_dir / "raw" / "sales_monthly.csv")


def load_store_master(data_dir: Path) -> pd.DataFrame:
    return pd.read_csv(data_dir / "master" / "store_location.csv")


def load_candidate_data(data_dir: Path) -> pd.DataFrame:
    return pd.read_csv(data_dir / "raw" / "candidate_location.csv")

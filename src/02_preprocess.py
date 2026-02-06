# 責務：分析用1枚テーブルを作る
# 直近12か月売上の集計
# 既存店ランク付け
# 特徴量抽出
# 標準化

import pandas as pd
from sklearn.preprocessing import StandardScaler


def aggregate_rolling_12m(sales_df: pd.DataFrame) -> pd.DataFrame:
    return (
        sales_df.sort_values(["store_id", "year_month"])
        .groupby("store_id")
        .tail(12)
        .groupby("store_id")["sales"]
        .sum()
        .reset_index(name="sales_12m")
    )


def assign_rank(df: pd.DataFrame, q=(0.33, 0.66)) -> pd.DataFrame:
    q1, q2 = df["sales_12m"].quantile(q).values
    df["rank"] = 1
    df.loc[df["sales_12m"] >= q1, "rank"] = 2
    df.loc[df["sales_12m"] >= q2, "rank"] = 3
    return df


def standardize_features(df: pd.DataFrame, feature_cols: list) -> pd.DataFrame:
    scaler = StandardScaler()
    df_std = df.copy()
    df_std[feature_cols] = scaler.fit_transform(df[feature_cols])
    return df_std

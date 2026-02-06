import pandas as pd


def calculate_store_rank(
    df_monthly: pd.DataFrame,
    value_col: str,
    store_col: str = "store_id",
    month_col: str = "year_month",
    rank_bins: tuple = (0.3, 0.7),
    n_months: int = 12,
) -> pd.DataFrame:
    """
    月次データから店舗ランクを算出する
    """

    # 1. year_month を datetime に変換
    df = df_monthly.copy()
    df[month_col] = pd.to_datetime(df[month_col])

    # 2. 直近 n_months を抽出
    latest_month = df[month_col].max()
    start_month = latest_month - pd.DateOffset(months=n_months - 1)
    df = df[df[month_col].between(start_month, latest_month)]

    # 3. 店舗ごとに平均値を算出
    agg = (
        df.groupby(store_col, as_index=False)[value_col]
        .mean()
        .rename(columns={value_col: "metric_mean"})
    )

    # 4. 分位点を計算
    q_low = agg["metric_mean"].quantile(rank_bins[0])
    q_high = agg["metric_mean"].quantile(rank_bins[1])

    # 5. ランク付与
    def assign_rank(x):
        if x >= q_high:
            return 3
        elif x >= q_low:
            return 2
        else:
            return 1

    agg["rank"] = agg["metric_mean"].apply(assign_rank)

    return agg

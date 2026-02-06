# 責務：自己検証
# 既存店のみ対象
# 1店舗ずつ除外
# rank と score の関係を見る

import pandas as pd


def self_validation(df_existing: pd.DataFrame, feature_cols: list) -> pd.DataFrame:
    records = []

    for idx, row in df_existing.iterrows():
        df_train = df_existing.drop(idx)
        score = calculate_similarity_score(df_train, feature_cols).loc[idx]
        records.append(
            {"store_id": row["store_id"], "rank": row["rank"], "score": score}
        )

    return pd.DataFrame(records)

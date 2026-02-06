# 責務：距離 → スコア
# 設計思想
# 距離計算は単純
# 好調店舗集合は Rank3
# 中央値距離を採用

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


def calculate_similarity_score(
    df_all: pd.DataFrame, feature_cols: list, good_rank: int = 3
) -> pd.Series:

    good_stores = df_all[df_all["rank"] == good_rank]
    X_good = good_stores[feature_cols].values
    X_all = df_all[feature_cols].values

    distances = cdist(X_all, X_good, metric="euclidean")
    score = np.median(distances, axis=1)

    return pd.Series(score, index=df_all.index, name="score")

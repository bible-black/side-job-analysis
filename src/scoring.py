# 近い既存店ほど影響が大きい
# 売上が高い既存店ほど影響が大きい

# src/scoring.py
from distance import haversine

TRADE_AREA_RADIUS_KM = 3.0


def location_score(candidate, stores):
    score = 0.0

    for _, store in stores.iterrows():
        d = haversine(
            candidate["lat"],
            candidate["lon"],
            store["lat"],
            store["lon"],
        )

        if d == 0:
            continue

        score += store["sales_index"] / d

    return score


# src/scoring.py
# 正規化関数を追加

from distance import haversine


def location_score(candidate, stores):
    score = 0.0

    for _, store in stores.iterrows():
        d = haversine(
            candidate["lat"],
            candidate["lon"],
            store["lat"],
            store["lon"],
        )

        if d == 0:
            continue

        score += store["sales_index"] / d

    return score


def normalize_scores(df, score_col="score"):
    min_score = df[score_col].min()
    max_score = df[score_col].max()

    df["normalized_score"] = (df[score_col] - min_score) / (max_score - min_score) * 100

    return df


# コメント付与関数を追加


def add_evaluation(df):
    def evaluate(score):
        if score >= 80:
            return "既存店との相乗効果が高く有望"
        elif score >= 60:
            return "出店検討価値あり"
        elif score >= 40:
            return "慎重な検討が必要"
        else:
            return "優先度は低い"

    df["evaluation"] = df["normalized_score"].apply(evaluate)
    return df

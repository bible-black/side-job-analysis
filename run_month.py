from pathlib import Path
import datetime

from src.load_data import (
    load_sales_data,
    load_store_master,
    load_candidate_data,
)
from src.preprocess import (
    aggregate_rolling_12m,
    assign_rank,
    standardize_features,
)
from src.score_calculation import calculate_similarity_score
from src.validation import self_validation
from src.visualization import (
    plot_candidate_ranking,
    plot_score_distribution,
    plot_portfolio,
)
from src.export import export_tables

import yaml


def load_config(name: str) -> dict:
    with open(Path("config") / name, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():

    # ==== 0. 共通設定 ====
    today = datetime.date.today()
    ym = today.strftime("%Y-%m")

    data_dir = Path("data")
    output_dir = Path("output") / ym
    fig_dir = output_dir / "fig"
    table_dir = output_dir / "table"

    fig_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)

    features_cfg = load_config("features.yaml")
    ranking_cfg = load_config("ranking.yaml")
    score_cfg = load_config("score.yaml")
    output_cfg = load_config("output.yaml")

    feature_cols = features_cfg["location_features"]
    good_rank = score_cfg["similarity_score"]["base_group"]["rank"]

    # ==== 1. データ読み込み ====
    sales_df = load_sales_data(data_dir)
    store_master_df = load_store_master(data_dir)
    candidate_df = load_candidate_data(data_dir)

    # ==== 2. 前処理 ====
    sales_12m = aggregate_rolling_12m(sales_df)

    existing_df = store_master_df.merge(sales_12m, on="store_id", how="left")

    existing_df = assign_rank(existing_df)

    existing_std = standardize_features(existing_df, feature_cols)
    candidate_std = standardize_features(candidate_df, feature_cols)

    # ==== 3. スコア計算 ====
    all_df = existing_std.assign(data_type="existing").append(
        candidate_std.assign(data_type="candidate"), ignore_index=True
    )

    all_df["score"] = calculate_similarity_score(
        all_df, feature_cols, good_rank=good_rank
    )

    existing_scored = all_df[all_df["data_type"] == "existing"]
    candidate_scored = all_df[all_df["data_type"] == "candidate"]

    # ==== 4. 妥当性検証 ====
    validation_df = self_validation(existing_std, feature_cols)

    # ==== 5. 可視化 ====
    plot_candidate_ranking(candidate_scored, fig_dir / "candidate_ranking.png")

    plot_score_distribution(
        existing_scored, candidate_scored, fig_dir / "score_distribution.png"
    )

    plot_portfolio(all_df, fig_dir / "portfolio.png")

    # ==== 6. 出力 ====
    export_tables(
        candidate_scored.sort_values("score"), table_dir / "candidate_score_ranking.csv"
    )

    export_tables(validation_df, table_dir / "validation_result.csv")


if __name__ == "__main__":
    main()

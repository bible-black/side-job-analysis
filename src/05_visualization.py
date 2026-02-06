# 責務：描くだけ
# 計算しない
# DataFrameを受け取って保存するだけ

import matplotlib.pyplot as plt


def plot_candidate_ranking(df_candidate, save_path):
    df = df_candidate.sort_values("score")
    plt.figure(figsize=(8, 4))
    plt.barh(df["candidate_name"], df["score"])
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

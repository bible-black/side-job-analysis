# 責務：成果物をまとめる

# ここは業務により変わるため、最小限にします。
# 例としてCSV出力、figフォルダ整理を想定しています。


def export_tables(df, path):
    df.to_csv(path, index=False)

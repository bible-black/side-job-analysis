# src/main.py
import pandas as pd
from scoring import location_score, normalize_scores, add_evaluation

candidates = pd.read_csv("data/candidate_locations.csv")
stores = pd.read_csv("data/existing_stores.csv")

results = []

for _, loc in candidates.iterrows():
    score = location_score(loc, stores)
    results.append(
        {
            "location_name": loc["location_name"],
            "location_type": loc["location_type"],
            "score": score,
        }
    )

df_result = pd.DataFrame(results)
df_result = normalize_scores(df_result)
df_result = add_evaluation(df_result)

df_result = df_result.sort_values("normalized_score", ascending=False)
print(df_result)

import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("results/graphs", exist_ok=True)

# Load final neural-network ranking
df = pd.read_csv("results/neural_network_ranking.csv")

print("Results loaded successfully!")
print("Total Candidates:", len(df))


# ==================================================
# GRAPH 1: Neural Network Score Distribution
# ==================================================

plt.figure(figsize=(8, 5))

plt.hist(
    df["Neural_Network_Score"],
    bins=20,
    edgecolor="black"
)

plt.xlabel("Neural Network Suitability Score")
plt.ylabel("Number of Candidates")
plt.title("Distribution of Candidate Suitability Scores")

plt.tight_layout()
plt.savefig(
    "results/graphs/score_distribution.png",
    dpi=300
)
plt.close()


# ==================================================
# GRAPH 2: Top 10 Candidate Scores
# ==================================================

top10 = df.head(10).copy()

plt.figure(figsize=(10, 6))

plt.bar(
    top10["Candidate_ID"],
    top10["Neural_Network_Score"]
)

plt.xlabel("Candidate ID")
plt.ylabel("Neural Network Score")
plt.title("Top 10 Candidates Ranked by NeuroHire")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "results/graphs/top10_candidates.png",
    dpi=300
)
plt.close()


# ==================================================
# GRAPH 3: Target vs Neural Network Prediction
# ==================================================

plt.figure(figsize=(7, 6))

plt.scatter(
    df["Suitability_Target"],
    df["Neural_Network_Score"],
    alpha=0.6
)

minimum = min(
    df["Suitability_Target"].min(),
    df["Neural_Network_Score"].min()
)

maximum = max(
    df["Suitability_Target"].max(),
    df["Neural_Network_Score"].max()
)

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)

plt.xlabel("Rule-Derived Suitability Target")
plt.ylabel("Neural Network Predicted Score")
plt.title("Target vs Neural Network Prediction")

plt.tight_layout()

plt.savefig(
    "results/graphs/target_vs_prediction.png",
    dpi=300
)
plt.close()


# ==================================================
# GRAPH 4: Feature Distributions
# ==================================================

features = [
    "Skill_Match",
    "JD_Similarity",
    "Experience_Score",
    "Education_Score"
]

for feature in features:

    plt.figure(figsize=(8, 5))

    plt.hist(
        df[feature],
        bins=15,
        edgecolor="black"
    )

    plt.xlabel(feature.replace("_", " "))
    plt.ylabel("Number of Candidates")
    plt.title(
        f"Distribution of {feature.replace('_', ' ')}"
    )

    plt.tight_layout()

    filename = feature.lower() + "_distribution.png"

    plt.savefig(
        f"results/graphs/{filename}",
        dpi=300
    )

    plt.close()


# ==================================================
# Save Top 10 separately for paper
# ==================================================

top10_columns = [
    "Candidate_ID",
    "Skill_Match",
    "JD_Similarity",
    "Experience_Score",
    "Education_Score",
    "Suitability_Target",
    "Neural_Network_Score",
    "Rank"
]

top10[top10_columns].to_csv(
    "results/top10_final_candidates.csv",
    index=False
)


print("\n============================")
print("RESULT GENERATION COMPLETED")
print("============================")

print("\nGraphs saved in:")
print("results/graphs/")

print("\nTop 10 table saved:")
print("results/top10_final_candidates.csv")

print("\nTop 10 Candidate Details:")
print(top10[top10_columns].to_string(index=False))
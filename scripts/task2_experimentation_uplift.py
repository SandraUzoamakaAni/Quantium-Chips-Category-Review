"""
Quantium Data Analytics Virtual Experience - Task 2
Experimentation and uplift testing.
"""
import pandas as pd
from scipy import stats

TRIAL_STORES = [77, 86, 88]
TRIAL_PERIOD = [pd.Period("2019-02"), pd.Period("2019-03"), pd.Period("2019-04")]
PRE_TRIAL_MONTHS = [pd.Period(f"2018-{m:02d}") for m in range(7, 13)] + [pd.Period("2019-01")]

data = pd.read_csv("QVI_data.csv")
data["DATE"] = pd.to_datetime(data["DATE"])
data["YEARMONTH"] = data["DATE"].dt.to_period("M")
months_per_store = data.groupby("STORE_NBR")["YEARMONTH"].nunique()
full_history_stores = months_per_store[months_per_store == 12].index
data = data[data["STORE_NBR"].isin(full_history_stores)]

monthly = data.groupby(["STORE_NBR", "YEARMONTH"]).agg(
    totSales=("TOT_SALES", "sum"),
    nCustomers=("LYLTY_CARD_NBR", "nunique"),
    nTxn=("TXN_ID", "nunique"),
    nChips=("PROD_QTY", "sum"),
).reset_index()
monthly["nTxnPerCust"] = monthly["nTxn"] / monthly["nCustomers"]
monthly["nChipsPerTxn"] = monthly["nChips"] / monthly["nTxn"]
monthly["avgPricePerUnit"] = monthly["totSales"] / monthly["nChips"]
monthly.to_csv("monthly_store_metrics.csv", index=False)


def calculate_correlation(pre_trial, metric, trial_store):
    trial_series = pre_trial[pre_trial.STORE_NBR == trial_store].set_index("YEARMONTH")[metric]
    rows = []
    for store in pre_trial["STORE_NBR"].unique():
        if store == trial_store:
            continue
        other = pre_trial[pre_trial.STORE_NBR == store].set_index("YEARMONTH")[metric]
        aligned = pd.concat([trial_series, other], axis=1, join="inner").dropna()
        if len(aligned) >= 2:
            rows.append({"STORE_NBR": store, "correlation": aligned.iloc[:, 0].corr(aligned.iloc[:, 1])})
    return pd.DataFrame(rows)


def calculate_magnitude_distance(pre_trial, metric, trial_store):
    trial_series = pre_trial[pre_trial.STORE_NBR == trial_store].set_index("YEARMONTH")[metric]
    rows = []
    for store in pre_trial["STORE_NBR"].unique():
        if store == trial_store:
            continue
        other = pre_trial[pre_trial.STORE_NBR == store].set_index("YEARMONTH")[metric]
        aligned = pd.concat([trial_series, other], axis=1, join="inner").dropna()
        aligned.columns = ["trial", "other"]
        rows.append({"STORE_NBR": store, "distance": (aligned["trial"] - aligned["other"]).abs().mean()})
    result = pd.DataFrame(rows)
    if result.empty:
        return result
    lo, hi = result["distance"].min(), result["distance"].max()
    result["magnitude_score"] = 1.0 if hi == lo else 1 - (result["distance"] - lo) / (hi - lo)
    return result


def select_control_store(monthly_data, trial_store):
    pre = monthly_data[monthly_data["YEARMONTH"].isin(PRE_TRIAL_MONTHS)]
    score_tables = []
    for metric in ["totSales", "nCustomers"]:
        corr = calculate_correlation(pre, metric, trial_store).rename(columns={"correlation": f"corr_{metric}"})
        mag = calculate_magnitude_distance(pre, metric, trial_store).rename(columns={"magnitude_score": f"mag_{metric}"})
        merged = corr.merge(mag[["STORE_NBR", f"mag_{metric}"]], on="STORE_NBR", how="inner")
        merged[f"score_{metric}"] = 0.5 * merged[f"corr_{metric}"] + 0.5 * merged[f"mag_{metric}"]
        score_tables.append(merged[["STORE_NBR", f"score_{metric}"]])
    scores = score_tables[0].merge(score_tables[1], on="STORE_NBR")
    scores["final_score"] = scores[["score_totSales", "score_nCustomers"]].mean(axis=1)
    scores = scores.sort_values("final_score", ascending=False)
    return int(scores.iloc[0]["STORE_NBR"]), scores


def assess_trial(monthly_data, trial_store, control_store):
    pre = monthly_data[monthly_data["YEARMONTH"].isin(PRE_TRIAL_MONTHS)]
    trial_pre = pre[pre.STORE_NBR == trial_store].set_index("YEARMONTH")
    control_pre = pre[pre.STORE_NBR == control_store].set_index("YEARMONTH")
    scaling_factor = trial_pre["totSales"].sum() / control_pre["totSales"].sum()
    control_all = monthly_data[monthly_data.STORE_NBR == control_store].set_index("YEARMONTH").copy()
    trial_all = monthly_data[monthly_data.STORE_NBR == trial_store].set_index("YEARMONTH")
    comparison = pd.DataFrame({"trial_sales": trial_all["totSales"], "scaled_control_sales": control_all["totSales"] * scaling_factor})
    comparison["pct_diff"] = (comparison["trial_sales"] - comparison["scaled_control_sales"]) / comparison["scaled_control_sales"]
    pre_diff = comparison.loc[comparison.index.isin(PRE_TRIAL_MONTHS), "pct_diff"]
    std_dev = pre_diff.std()
    df = len(pre_diff) - 1
    trial_diff = comparison.loc[comparison.index.isin(TRIAL_PERIOD), "pct_diff"]
    t_values = trial_diff / std_dev
    critical_t = stats.t.ppf(0.95, df)
    result = pd.DataFrame({"pct_diff": trial_diff, "t_value": t_values, "significant_uplift": t_values > critical_t})
    return result

control_map = {}
for trial_store in TRIAL_STORES:
    control_store, scores = select_control_store(monthly, trial_store)
    control_map[trial_store] = control_store
    print(f"Trial store {trial_store} -> control store {control_store}")
    result = assess_trial(monthly, trial_store, control_store)
    print(result.to_string())

print("\nDriver breakdown during trial period")
for trial_store, control_store in control_map.items():
    trial = monthly[(monthly.STORE_NBR == trial_store) & monthly.YEARMONTH.isin(TRIAL_PERIOD)]
    control = monthly[(monthly.STORE_NBR == control_store) & monthly.YEARMONTH.isin(TRIAL_PERIOD)]
    for metric in ["nCustomers", "nTxnPerCust", "avgPricePerUnit"]:
        pct = (trial[metric].mean() - control[metric].mean()) / control[metric].mean() * 100
        print(f"Store {trial_store} vs {control_store} - {metric}: {pct:+.1f}%")

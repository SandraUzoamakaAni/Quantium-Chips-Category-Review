"""
Quantium Data Analytics Virtual Experience - Task 2
Experimentation and uplift testing

Goal: Julia ran a store trial (layout change) in stores 77, 86 and 88.
For each trial store we need to:
  1. Build monthly metrics per store (sales, customers, txns/customer)
  2. Select the best-matching control store using pre-trial correlation +
     magnitude similarity
  3. Compare trial vs. control during the trial period (Feb-Apr 2019) and
     test whether the difference is statistically significant
  4. Identify whether any uplift came from more customers, more
     transactions per customer, or higher spend per transaction
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

pd.set_option("display.width", 120)

TRIAL_STORES = [77, 86, 88]
TRIAL_PERIOD = [pd.Period("2019-02"), pd.Period("2019-03"), pd.Period("2019-04")]

# ---------------------------------------------------------------
# 1. Load data & build monthly metrics per store
# ---------------------------------------------------------------
data = pd.read_csv("QVI_data.csv")
data["DATE"] = pd.to_datetime(data["DATE"])
data["YEARMONTH"] = data["DATE"].dt.to_period("M")

# Only keep stores that have a full 12 months of data - a store with
# missing months would distort the correlation/magnitude matching
months_per_store = data.groupby("STORE_NBR")["YEARMONTH"].nunique()
full_history_stores = months_per_store[months_per_store == 12].index
data = data[data["STORE_NBR"].isin(full_history_stores)]

monthly = (
    data.groupby(["STORE_NBR", "YEARMONTH"])
    .agg(
        totSales=("TOT_SALES", "sum"),
        nCustomers=("LYLTY_CARD_NBR", "nunique"),
        nTxn=("TXN_ID", "nunique"),
        nChips=("PROD_QTY", "sum"),
    )
    .reset_index()
)
monthly["nTxnPerCust"] = monthly["nTxn"] / monthly["nCustomers"]
monthly["nChipsPerTxn"] = monthly["nChips"] / monthly["nTxn"]
monthly["avgPricePerUnit"] = monthly["totSales"] / monthly["nChips"]

monthly.to_csv("monthly_store_metrics.csv", index=False)
print(f"Monthly metrics built for {monthly['STORE_NBR'].nunique()} stores "
      f"({len(full_history_stores)} had full 12-month history)")

PRE_TRIAL_MONTHS = [pd.Period(f"2018-{m:02d}") for m in range(7, 13)] + [pd.Period("2019-01")]

# ---------------------------------------------------------------
# 2. Control store selection: correlation + magnitude distance
# ---------------------------------------------------------------
def calculate_correlation(pre_trial, metric, trial_store):
    """Pearson correlation of `metric` trend between trial_store and every
    other store during the pre-trial period."""
    trial_series = pre_trial[pre_trial.STORE_NBR == trial_store].set_index("YEARMONTH")[metric]
    scores = []
    for store in pre_trial["STORE_NBR"].unique():
        if store == trial_store:
            continue
        other_series = pre_trial[pre_trial.STORE_NBR == store].set_index("YEARMONTH")[metric]
        aligned = pd.concat([trial_series, other_series], axis=1, join="inner")
        if len(aligned) < 2:
            continue
        corr = aligned.iloc[:, 0].corr(aligned.iloc[:, 1])
        scores.append({"STORE_NBR": store, "corr_" + metric: corr})
    return pd.DataFrame(scores)


def calculate_magnitude_distance(pre_trial, metric, trial_store):
    """1 - normalised absolute distance of `metric` between trial_store and
    every other store during the pre-trial period (1 = identical magnitude)."""
    trial_series = pre_trial[pre_trial.STORE_NBR == trial_store].set_index("YEARMONTH")[metric]
    rows = []
    for store in pre_trial["STORE_NBR"].unique():
        if store == trial_store:
            continue
        other_series = pre_trial[pre_trial.STORE_NBR == store].set_index("YEARMONTH")[metric]
        aligned = pd.concat([trial_series, other_series], axis=1, join="inner")
        aligned.columns = ["trial", "other"]
        aligned["abs_dist"] = (aligned["trial"] - aligned["other"]).abs()
        rows.append(aligned.reset_index().assign(STORE_NBR=store))
    dist_df = pd.concat(rows, ignore_index=True)
    monthly_dist = dist_df.groupby(["STORE_NBR", "YEARMONTH"])["abs_dist"].mean().reset_index()
    min_d, max_d = monthly_dist["abs_dist"].min(), monthly_dist["abs_dist"].max()
    monthly_dist["mag_" + metric] = 1 - (monthly_dist["abs_dist"] - min_d) / (max_d - min_d)
    return monthly_dist.groupby("STORE_NBR")["mag_" + metric].mean().reset_index()


def select_control_store(monthly, trial_store, metrics=("totSales", "nCustomers")):
    """Combine correlation + magnitude-distance scores across the given
    metrics into one composite score (0.5 weight each, as recommended in
    the task brief) and return the best-matching control store."""
    pre_trial = monthly[monthly["YEARMONTH"].isin(PRE_TRIAL_MONTHS)]

    scores = None
    for metric in metrics:
        corr = calculate_correlation(pre_trial, metric, trial_store)
        mag = calculate_magnitude_distance(pre_trial, metric, trial_store)
        combined = corr.merge(mag, on="STORE_NBR")
        combined["score_" + metric] = 0.5 * combined["corr_" + metric] + 0.5 * combined["mag_" + metric]
        combined = combined[["STORE_NBR", "score_" + metric]]
        scores = combined if scores is None else scores.merge(combined, on="STORE_NBR")

    score_cols = [c for c in scores.columns if c.startswith("score_")]
    scores["final_score"] = scores[score_cols].mean(axis=1)
    scores = scores.sort_values("final_score", ascending=False)
    best = scores.iloc[0]
    return int(best["STORE_NBR"]), scores


control_map = {}
for trial_store in TRIAL_STORES:
    control_store, scores = select_control_store(monthly, trial_store)
    control_map[trial_store] = control_store
    print(f"\nTrial store {trial_store} -> best control store: {control_store} "
          f"(score={scores.iloc[0]['final_score']:.3f})")
    print(scores.head(3).to_string(index=False))

# ---------------------------------------------------------------
# 3. Visualise trial vs. control pre-trial trends (sanity check on the match)
# ---------------------------------------------------------------
for trial_store, control_store in control_map.items():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for store, label, color in [(trial_store, f"Trial store {trial_store}", "#2563eb"),
                                 (control_store, f"Control store {control_store}", "#f97316")]:
        s = monthly[monthly.STORE_NBR == store].sort_values("YEARMONTH")
        ax.plot(s["YEARMONTH"].astype(str), s["totSales"], marker="o", label=label, color=color)
    ax.axvspan(str(TRIAL_PERIOD[0]), str(TRIAL_PERIOD[-1]), color="gray", alpha=0.15, label="Trial period")
    ax.set_title(f"Total Sales: Trial Store {trial_store} vs. Control Store {control_store}")
    ax.set_ylabel("Total sales ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.xticks(rotation=45)
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"trial_vs_control_{trial_store}.png", dpi=150)
    plt.close()

# ---------------------------------------------------------------
# 4. Statistical significance test during the trial period
# ---------------------------------------------------------------
def assess_trial(monthly, trial_store, control_store):
    """Scale the control store's pre-trial sales to match the trial store's
    average level, then use the pre-trial scaled % differences to estimate a
    standard deviation. Any trial-period % difference beyond ~1.96 std devs
    (one-tailed t-test, ~95% confidence) is considered a significant uplift."""
    pre_trial = monthly[monthly["YEARMONTH"].isin(PRE_TRIAL_MONTHS)]
    trial_pre = pre_trial[pre_trial.STORE_NBR == trial_store].set_index("YEARMONTH")
    control_pre = pre_trial[pre_trial.STORE_NBR == control_store].set_index("YEARMONTH")

    scaling_factor = trial_pre["totSales"].sum() / control_pre["totSales"].sum()

    all_months = monthly[monthly.STORE_NBR == control_store].set_index("YEARMONTH").copy()
    all_months["scaled_control_sales"] = all_months["totSales"] * scaling_factor

    trial_all = monthly[monthly.STORE_NBR == trial_store].set_index("YEARMONTH")
    comparison = pd.DataFrame({
        "trial_sales": trial_all["totSales"],
        "scaled_control_sales": all_months["scaled_control_sales"],
    })
    comparison["pct_diff"] = (comparison["trial_sales"] - comparison["scaled_control_sales"]) / comparison["scaled_control_sales"]

    pre_trial_pct_diff = comparison.loc[comparison.index.isin(PRE_TRIAL_MONTHS), "pct_diff"]
    std_dev = pre_trial_pct_diff.std()
    degrees_freedom = len(pre_trial_pct_diff) - 1

    from scipy import stats
    trial_period_diff = comparison.loc[comparison.index.isin(TRIAL_PERIOD), "pct_diff"]
    t_values = trial_period_diff / std_dev
    critical_t = stats.t.ppf(0.95, degrees_freedom)  # one-tailed, 95% confidence

    result = pd.DataFrame({
        "pct_diff": trial_period_diff,
        "t_value": t_values,
        "significant_uplift": t_values > critical_t,
    })
    return comparison, result, scaling_factor, critical_t


all_results = {}
for trial_store, control_store in control_map.items():
    comparison, result, scaling_factor, critical_t = assess_trial(monthly, trial_store, control_store)
    all_results[trial_store] = result
    print(f"\n=== Trial store {trial_store} vs. control {control_store} "
          f"(scaling factor {scaling_factor:.3f}, critical t={critical_t:.2f}) ===")
    print(result.to_string())

# ---------------------------------------------------------------
# 5. Was the uplift driven by more customers, more txns/customer, or price?
# ---------------------------------------------------------------
print("\n=== Driver breakdown during trial period ===")
for trial_store, control_store in control_map.items():
    t = monthly[(monthly.STORE_NBR == trial_store) & (monthly.YEARMONTH.isin(TRIAL_PERIOD))]
    c_pre = monthly[(monthly.STORE_NBR == control_store) & (monthly.YEARMONTH.isin(PRE_TRIAL_MONTHS))]
    c_trial = monthly[(monthly.STORE_NBR == control_store) & (monthly.YEARMONTH.isin(TRIAL_PERIOD))]

    for metric in ["nCustomers", "nTxnPerCust", "avgPricePerUnit"]:
        t_avg = t[metric].mean()
        c_avg = c_trial[metric].mean()
        pct = (t_avg - c_avg) / c_avg * 100
        print(f"Store {trial_store} vs control {control_store} - {metric}: "
              f"trial={t_avg:.2f}, control={c_avg:.2f}, diff={pct:+.1f}%")
    print()

print("Task 2 analysis complete.")

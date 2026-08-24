import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

data = pd.read_csv("QVI_data_clean.csv")
data["DATE"] = pd.to_datetime(data["DATE"])
segment_summary = pd.read_csv("segment_summary.csv")

pivot = segment_summary.pivot(index="LIFESTAGE", columns="PREMIUM_CUSTOMER", values="TOT_SALES")
pivot = pivot[["Budget", "Mainstream", "Premium"]]
pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=True).index]
fig, ax = plt.subplots(figsize=(9, 6))
pivot.plot(kind="barh", stacked=True, ax=ax, color=["#f97316", "#2563eb", "#16a34a"])
ax.set_xlabel("Total sales ($)")
ax.set_ylabel("")
ax.set_title("Total Chip Sales by Customer Segment")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend(title="Customer type", loc="lower right")
plt.tight_layout()
plt.savefig("chart1_sales_by_segment.png", dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(9, 6))
colors = {"Budget": "#f97316", "Mainstream": "#2563eb", "Premium": "#16a34a"}
for pc, grp in segment_summary.groupby("PREMIUM_CUSTOMER"):
    ax.scatter(grp["N_CUSTOMERS"], grp["AVG_SPEND_PER_CUSTOMER"], s=grp["TOT_SALES"] / 400, alpha=0.7, color=colors[pc], label=pc, edgecolors="white")
    for _, row in grp.iterrows():
        ax.annotate(row["LIFESTAGE"].title(), (row["N_CUSTOMERS"], row["AVG_SPEND_PER_CUSTOMER"]), fontsize=7, xytext=(4, 4), textcoords="offset points")
ax.set_xlabel("Number of customers in segment")
ax.set_ylabel("Average spend per customer ($)")
ax.set_title("Segment Size vs. Average Spend per Customer\n(bubble size = total segment sales)")
ax.legend(title="Customer type")
plt.tight_layout()
plt.savefig("chart2_spend_vs_size.png", dpi=150)
plt.close()

target = data[(data.LIFESTAGE == "YOUNG SINGLES/COUPLES") & (data.PREMIUM_CUSTOMER == "Mainstream")]
rest = data[~((data.LIFESTAGE == "YOUNG SINGLES/COUPLES") & (data.PREMIUM_CUSTOMER == "Mainstream"))]
t_brand = target["BRAND"].value_counts(normalize=True)
r_brand = rest["BRAND"].value_counts(normalize=True)
affinity = (t_brand / r_brand).dropna().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(affinity.index[::-1], affinity.values[::-1], color="#2563eb")
ax.axvline(1.0, color="gray", linestyle="--", linewidth=1)
ax.set_xlabel("Affinity index (1.0 = same rate as rest of customers)")
ax.set_title("Brand Affinity: Mainstream Young Singles/Couples vs. All Other Customers")
plt.tight_layout()
plt.savefig("chart3_brand_affinity.png", dpi=150)
plt.close()

monthly = data.set_index("DATE").resample("ME")["TOT_SALES"].sum()
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(monthly.index, monthly.values, marker="o", color="#2563eb")
ax.set_title("Total Chip Sales by Month (Jul 2018 - Jun 2019)")
ax.set_ylabel("Total sales ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart4_monthly_trend.png", dpi=150)
plt.close()

print("Charts saved.")

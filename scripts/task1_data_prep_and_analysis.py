"""
Quantium Data Analytics Virtual Experience - Task 1
Data preparation and customer analytics
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

pd.set_option("display.width", 120)

txn = pd.read_excel("QVI_transaction_data.xlsx")
txn["DATE"] = pd.to_datetime(txn["DATE"], unit="D", origin="1899-12-30")
before = len(txn)
txn = txn.drop_duplicates()
print(f"Removed {before - len(txn)} duplicate row(s)")
txn["IS_SALSA"] = txn["PROD_NAME"].str.lower().str.contains("salsa")
print(f"Removing {txn['IS_SALSA'].sum()} salsa transactions ({txn.loc[txn['IS_SALSA'], 'PROD_NAME'].nunique()} salsa products)")
txn = txn[~txn["IS_SALSA"]].drop(columns="IS_SALSA")
print("\nTop 5 PROD_QTY values before outlier removal:")
print(txn["PROD_QTY"].sort_values(ascending=False).head())
outlier_card = txn.loc[txn["PROD_QTY"] >= 200, "LYLTY_CARD_NBR"].unique()
print(f"Removing outlier loyalty card(s): {outlier_card}")
txn = txn[~txn["LYLTY_CARD_NBR"].isin(outlier_card)]

txn["PACK_SIZE"] = txn["PROD_NAME"].str.extract(r"(\d+)\s*[gG]").astype(int)
brand_map = {
    "RED": "RRD", "RRD": "RRD", "SNBTS": "SUNBITES", "SUNBITES": "SUNBITES",
    "INFZNS": "INFUZIONS", "INFUZIONS": "INFUZIONS", "WW": "WOOLWORTHS", "WOOLWORTHS": "WOOLWORTHS",
    "SMITH": "SMITHS", "SMITHS": "SMITHS", "NCC": "NATURAL", "NATURAL": "NATURAL",
    "DORITO": "DORITOS", "DORITOS": "DORITOS", "GRAIN": "GRNWVES", "GRNWVES": "GRNWVES",
}
txn["BRAND"] = txn["PROD_NAME"].str.split().str[0].str.upper().map(lambda b: brand_map.get(b, b))
print(f"\nCleaned transaction rows: {len(txn):,}")
print(f"Date range: {txn['DATE'].min().date()} to {txn['DATE'].max().date()}")
print(f"Unique brands: {txn['BRAND'].nunique()}")
print(f"Pack sizes: {sorted(txn['PACK_SIZE'].unique())}")

cust = pd.read_csv("QVI_purchase_behaviour.csv")
print(f"\nCustomer records: {len(cust):,}")
print(f"Nulls:\n{cust.isnull().sum()}")
print(f"LIFESTAGE categories: {cust['LIFESTAGE'].unique().tolist()}")
print(f"PREMIUM_CUSTOMER categories: {cust['PREMIUM_CUSTOMER'].unique().tolist()}")

data = txn.merge(cust, on="LYLTY_CARD_NBR", how="left")
print(f"\nMerged dataset shape: {data.shape}")
print(f"Unmatched customers after merge: {data['LIFESTAGE'].isnull().sum()}")
data.to_csv("QVI_data_clean.csv", index=False)
print("Saved cleaned & merged dataset -> QVI_data_clean.csv")

sales_by_segment = data.groupby(["LIFESTAGE", "PREMIUM_CUSTOMER"])["TOT_SALES"].sum().reset_index().sort_values("TOT_SALES", ascending=False)
sales_by_segment.to_csv("sales_by_segment.csv", index=False)
print("\nTop 5 segments by total sales:")
print(sales_by_segment.head())
customers_by_segment = cust.groupby(["LIFESTAGE", "PREMIUM_CUSTOMER"])["LYLTY_CARD_NBR"].nunique().reset_index(name="N_CUSTOMERS")
spend_per_cust = data.groupby(["LIFESTAGE", "PREMIUM_CUSTOMER", "LYLTY_CARD_NBR"])["TOT_SALES"].sum().reset_index()
avg_spend_by_segment = spend_per_cust.groupby(["LIFESTAGE", "PREMIUM_CUSTOMER"])["TOT_SALES"].mean().reset_index(name="AVG_SPEND_PER_CUSTOMER")
units_per_cust = data.groupby(["LIFESTAGE", "PREMIUM_CUSTOMER", "LYLTY_CARD_NBR"])["PROD_QTY"].sum().reset_index()
avg_units_by_segment = units_per_cust.groupby(["LIFESTAGE", "PREMIUM_CUSTOMER"])["PROD_QTY"].mean().reset_index(name="AVG_UNITS_PER_CUSTOMER")
segment_summary = sales_by_segment.merge(customers_by_segment, on=["LIFESTAGE", "PREMIUM_CUSTOMER"]).merge(avg_spend_by_segment, on=["LIFESTAGE", "PREMIUM_CUSTOMER"]).merge(avg_units_by_segment, on=["LIFESTAGE", "PREMIUM_CUSTOMER"])
segment_summary["AVG_PRICE_PER_UNIT"] = segment_summary["TOT_SALES"] / (segment_summary["AVG_UNITS_PER_CUSTOMER"] * segment_summary["N_CUSTOMERS"])
segment_summary.to_csv("segment_summary.csv", index=False)
print("\nFull segment summary:")
print(segment_summary.to_string(index=False))
top_segments = segment_summary.nlargest(2, "TOT_SALES")[["LIFESTAGE", "PREMIUM_CUSTOMER"]]
print("\nTop 2 segments by total sales:")
print(top_segments)
for _, seg in top_segments.iterrows():
    seg_data = data[(data["LIFESTAGE"] == seg["LIFESTAGE"]) & (data["PREMIUM_CUSTOMER"] == seg["PREMIUM_CUSTOMER"])]
    top_brands = seg_data.groupby("BRAND")["PROD_QTY"].sum().sort_values(ascending=False).head(5)
    top_packs = seg_data.groupby("PACK_SIZE")["PROD_QTY"].sum().sort_values(ascending=False).head(5)
    print(f"\n--- {seg['LIFESTAGE']} / {seg['PREMIUM_CUSTOMER']} ---")
    print("Top brands (by units):\n", top_brands)
    print("Top pack sizes (by units):\n", top_packs)
print("\nAnalysis complete.")

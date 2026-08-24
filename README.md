# Quantium Data Analytics Virtual Experience — Chips Category Review

> A portfolio project based on the Quantium Data Analytics Job Simulation completed through Forage.

## Project overview

This project analyses a fictional retail chips category from two perspectives: **customer and product analytics** and **store-trial experimentation**. The work turns raw retail data into commercial insights and recommendations for a client.

### Task 1 — Data preparation & customer analytics
- Cleaned transaction and customer purchase-behaviour data.
- Removed duplicate records, non-chip salsa products and an extreme bulk-purchase outlier.
- Standardised product brands and extracted pack sizes from product names.
- Merged transaction and customer data into an analysis-ready dataset.
- Segmented customers by life stage and premium/budget/mainstream status.
- Compared segment size, total sales, average spend and purchasing behaviour.
- Analysed brand affinity and pack-size preferences for priority customer segments.

### Task 2 — Experimentation & uplift testing
- Built monthly store-level performance metrics.
- Matched trial stores 77, 86 and 88 with comparable control stores using pre-trial correlation and magnitude similarity.
- Compared trial and control performance during the February–April 2019 trial period.
- Tested whether observed sales differences represented statistically significant uplift.
- Broke uplift down into customer counts, transactions per customer and average price per unit.

### Task 3 — Commercial presentation
- Converted the analysis into a client-ready presentation using a conclusion-first structure.
- Presented the key customer opportunity, trial results and recommended commercial actions with supporting evidence.

## Key findings

- **Mainstream Young & Midage Singles/Couples** are a standout growth opportunity because of their large customer base and purchasing behaviour.
- The priority segment shows stronger affinity toward selected premium brands and larger pack sizes, creating opportunities for targeted ranging and promotions.
- **2 of 3 trial stores showed statistically significant sales uplift** during the trial period.
- The observed uplift was primarily associated with **increased customer numbers**, rather than simply higher spend per visit.

## Repository structure

```text
Quantium-Chips-Category-Review/
├── README.md
├── requirements.txt
├── data/
│   ├── sales_by_segment.csv
│   ├── segment_summary.csv
│   └── monthly_store_metrics.csv
├── scripts/
│   ├── task1_data_prep_and_analysis.py
│   ├── task1_charts.py
│   └── task2_experimentation_uplift.py
├── charts/
│   ├── chart1_sales_by_segment.png
│   ├── chart2_spend_vs_size.png
│   ├── chart3_brand_affinity.png
│   ├── chart4_monthly_trend.png
│   └── trial_vs_control_77.png
└── presentation/
    ├── Quantium_Chips_Category_Review.pdf
    └── Quantium_Chips_Category_Review.pptx
```

## Tools & methods

- Python
- pandas
- NumPy
- Matplotlib
- SciPy
- python-pptx
- Data cleaning and transformation
- Customer segmentation
- Exploratory data analysis
- Control-store matching
- Statistical significance testing
- Commercial storytelling

## Running the analysis

Install the dependencies:

```bash
pip install -r requirements.txt
```

The original Quantium transaction and purchase-behaviour datasets are required to run the raw-data preparation script. The repository also contains the generated summary tables and charts used in the final analysis.

Run the scripts from the repository root so their relative file paths resolve correctly.

## Deliverables

The `presentation/` folder contains both the editable PowerPoint deck and PDF version of the final client-facing presentation.

## Disclaimer

This is an educational portfolio project based on a job simulation. It is not affiliated with or endorsed by Quantium beyond participation in the simulation.

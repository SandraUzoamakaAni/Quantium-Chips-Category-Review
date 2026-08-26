# Quantium Chips Category Review

> A data analytics and experimentation portfolio project based on the **Quantium Data Analytics Job Simulation** through Forage.

## Project overview

This project analyzes customer purchasing behavior in the chips category and evaluates a store trial designed to determine whether a new store layout improved sales performance.

The analysis combines **data preparation, customer segmentation, exploratory analysis, visualization, control-store selection, and uplift testing** to turn retail transaction data into practical commercial recommendations.

## Business questions

- Which customer segments contribute most to chips sales?
- How do customer characteristics relate to chip spend and purchase behavior?
- Which brands and pack sizes show the strongest customer affinity?
- What seasonal patterns appear in category sales?
- Did the trial stores experience meaningful uplift compared with matched control stores?
- What actions should the business take based on the evidence?

## Analysis

### 1. Customer & Category Analysis

The first stage prepares and analyzes transaction and customer data, including:

- duplicate and outlier handling
- salsa-product exclusion
- product-name standardization
- customer segmentation
- total sales by customer segment
- spend and purchase behavior by pack size
- brand affinity
- monthly sales trends

### 2. Store Trial Experimentation

The second stage evaluates the trial using comparable control stores and measures:

- monthly sales performance
- transaction and customer metrics
- correlation and magnitude-based control-store matching
- trial vs. scaled-control performance
- uplift during the trial period
- statistical significance using a t-test framework
- customer frequency and pricing drivers

## Key outputs

The repository contains the analysis scripts, processed summary datasets, visualizations, and final presentation materials used to communicate the findings.

## Repository structure

```text
Quantium-Chips-Category-Review/
├── README.md
├── requirements.txt
│
├── data/
│   ├── README.md
│   ├── monthly_store_metrics.csv
│   ├── sales_by_segment.csv
│   └── segment_summary.csv
│
├── scripts/
│   ├── task1_data_prep_and_analysis.py
│   ├── task1_charts.py
│   └── task2_experimentation_uplift.py
│
├── charts/
│   ├── chart1_sales_by_segment.png
│   ├── chart2_spend_vs_size.png
│   ├── chart3_brand_affinity.png
│   ├── chart4_monthly_trend.png
│   └── trial_vs_control_77.png
│
└── presentations/
    ├── Quantium_Chips_Category_Review.pdf
    └── Quantium_Chips_Category_Review.pptx
```

## Technologies

- Python
- pandas
- NumPy
- Matplotlib
- SciPy
- Statistical analysis
- Customer segmentation
- Data visualization
- Experimental design
- Control-store comparison
- Uplift analysis

## Running the project

Install the dependencies:

```bash
pip install -r requirements.txt
```

The scripts are designed to be run from the repository and use paths relative to the project root. The original Quantium simulation source files must be placed in `data/` before running the raw-data workflow:

- `QVI_transaction_data.xlsx`
- `QVI_purchase_behaviour.csv`
- `QVI_data.csv`

The public repository intentionally does **not** redistribute those original simulation files. The included processed CSVs, charts, scripts, and presentations preserve the portfolio evidence without republishing the source data.

### Task 1 workflow

1. Place `QVI_transaction_data.xlsx` and `QVI_purchase_behaviour.csv` in `data/`.
2. Run `scripts/task1_data_prep_and_analysis.py`.
3. Run `scripts/task1_charts.py` to regenerate the charts in `charts/`.

### Task 2 workflow

1. Place `QVI_data.csv` in `data/`.
2. Run `scripts/task2_experimentation_uplift.py`.

## Deliverables

- **Analysis scripts:** data preparation, category analysis, visualization, and experimentation workflow.
- **Processed datasets:** summary tables used for the final analysis.
- **Charts:** key customer, category, and trial/control visuals.
- **Presentation:** PDF and editable PowerPoint versions of the final analysis.

## Disclaimer

This is an educational portfolio project based on the Quantium Data Analytics Job Simulation. It is not affiliated with, endorsed by, or representative of Quantium beyond participation in the simulation.

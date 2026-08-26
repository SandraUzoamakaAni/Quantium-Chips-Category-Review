# Quantium Chips Category Review

> A data analytics and experimentation project based on the **Quantium Data Analytics Job Simulation** through Forage.

## Project overview

This project analyzes customer purchasing behavior in the chips category and evaluates a store trial designed to understand whether a new store layout improved sales performance.

The analysis combines **data preparation, customer segmentation, exploratory analysis, visualization, and uplift/experimentation analysis** to turn transaction data into practical commercial recommendations.

## Business questions

- Which customer segments contribute most to chips sales?
- How do customer characteristics relate to chip spend and purchase behavior?
- Which brands and pack sizes show the strongest customer affinity?
- What seasonal patterns appear in category sales?
- Did the trial store experience a meaningful uplift compared with its control stores?
- What actions should the business take based on the evidence?

## Analysis

### 1. Customer & Category Analysis

The first stage prepares and analyzes the customer and transaction data, including:

- customer segmentation
- total sales by customer segment
- spend and purchase behavior by pack size
- brand affinity
- monthly sales trends
- category-level visualizations

### 2. Store Trial Experimentation

The second stage evaluates the trial using comparable control stores and measures:

- monthly sales performance
- transaction and customer metrics
- trial vs. control performance
- uplift during the trial period
- whether the observed change supports a commercial recommendation

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
└── presentation/
    ├── Quantium_Chips_Category_Review.pdf
    └── Quantium_Chips_Category_Review.pptx
```

## Technologies

- Python
- pandas
- NumPy
- Matplotlib
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

The scripts document the original analysis workflow. The processed CSV files in `data/` contain summary outputs used by the visualizations and presentation.

> **Source-data note:** The original Quantium simulation files (`QVI_transaction_data.xlsx`, `QVI_purchase_behaviour.csv`, and `QVI_data.csv`) are not included in this public repository. This avoids redistributing the original simulation data while still providing the analysis code, processed outputs, charts, and final presentation.

## Deliverables

### Analysis
The Python scripts document the main data preparation, category analysis, visualization, and experimentation workflow.

### Visualizations
The `charts/` folder contains the key charts generated from the analysis.

### Final presentation
The `presentation/` folder contains both the PDF and editable PowerPoint versions of the final analysis presentation.

## Disclaimer

This is an educational portfolio project based on the Quantium Data Analytics Job Simulation. It is not affiliated with, endorsed by, or representative of Quantium beyond participation in the simulation.

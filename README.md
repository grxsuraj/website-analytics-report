# Website Analytics & Conversion Optimization

### Python | SQL | Pandas | Excel | Data Analytics

**Author:** Arya Vilas Kadam
**Target Role:** EY Consulting – Technology Analyst
**Domain:** Data Analytics

```text
Raw Website Data
        ↓
   SQL Analysis
        ↓
Python/Pandas Analysis
        ↓
    KPI Reporting
        ↓
 Business Insights
        ↓
 Recommendations
```

---

## Overview

This project is a technology and data analytics case study focused on understanding digital patient acquisition, website engagement, traffic channel performance, and appointment booking conversions for a wellness clinic.

The analysis covers **38,181 website sessions** collected over a **24-month period**.

The project uses **basic SQL** for business-oriented analysis, **Python/Pandas** for data validation and automated KPI computation, and **Excel** for presenting summarized results.

The objective is to convert raw website data into actionable business insights and recommendations.

---

## Business Problem

The clinic's management lacked clear quantitative visibility into its digital acquisition and appointment booking funnel.

The analysis focuses on four key areas:

1. **Traffic Channel Performance**
   Which sources generate the most website traffic and which generate the highest number of appointment bookings?

2. **User Drop-Off**
   Which traffic sources have high bounce rates or relatively low conversion rates?

3. **Device Performance**
   How do user engagement and conversion rates differ between mobile, desktop, and tablet visitors?

4. **Growth Trends**
   How are website sessions and appointment bookings changing over time?

---

## Business Questions

This project answers five core business questions:

* Which acquisition channels generate the most traffic?
* Which channels have the highest conversion rates?
* How does website performance differ across devices?
* Are there noticeable monthly trends in traffic and conversions?
* Where are the main opportunities for improving website conversion?

---

## Dataset

* **Source:** Synthetic Google Analytics-style website session data modeled on wellness clinic traffic patterns.
* **Volume:** **38,181 session records**
* **Period:** June 2022 – May 2024
* **Duration:** 24 months

### Key Attributes

| Attribute            | Description                                            |
| -------------------- | ------------------------------------------------------ |
| `session_id`         | Unique identifier for each session                     |
| `date`               | Session date                                           |
| `year_month`         | Month used for trend analysis                          |
| `traffic_source`     | Acquisition channel                                    |
| `device`             | Mobile, Desktop, or Tablet                             |
| `pages_viewed`       | Number of pages viewed during the session              |
| `session_duration_s` | Session duration in seconds                            |
| `bounced`            | Whether the user left after a single page              |
| `converted`          | Whether the session resulted in an appointment booking |

---

## Tools & Technologies

| Tool / Technology   | Purpose                                                      |
| ------------------- | ------------------------------------------------------------ |
| **SQL**             | Business queries, KPI calculations, grouping, and comparison |
| **Python**          | Data processing and automation                               |
| **Pandas**          | Data cleaning, aggregation, and analysis                     |
| **NumPy**           | Numerical calculations where required                        |
| **Microsoft Excel** | KPI summary and stakeholder reporting                        |

---

## Methodology

The project follows a simple five-step analytics workflow.

### 1. Data Ingestion & Validation

Loaded **38,181 session records** into Python and performed basic data-quality checks, including missing-value and duplicate checks.

### 2. SQL Analysis

Created four modular SQL queries using basic SQL operations such as:

* `SELECT`
* `WHERE`
* `GROUP BY`
* `ORDER BY`
* `COUNT`
* `SUM`
* `AVG`
* `CASE WHEN`

The queries analyze overall KPIs, channel performance, device performance, and monthly trends.

### 3. Python/Pandas Analysis

Developed a lightweight Python pipeline to:

* load the dataset
* validate data quality
* calculate KPIs
* aggregate channel and device performance
* analyze monthly trends
* export analysis results

The pipeline is intentionally kept concise and readable for easy maintenance and reproducibility.

### 4. KPI Reporting

Generated summary outputs covering traffic volume, conversions, conversion rate, bounce rate, and average session duration.

The results are also exported to an Excel executive summary.

### 5. Insights & Recommendations

Converted analytical findings into business insights and practical recommendations based on the observed data.

---

## Key KPIs

| KPI                          |       Value | Business Meaning                                  |
| ---------------------------- | ----------: | ------------------------------------------------- |
| **Total Sessions**           |  **38,181** | Total website visits during the analysis period   |
| **Total Conversions**        |   **1,220** | Sessions resulting in an appointment booking      |
| **Overall Conversion Rate**  |   **3.20%** | Percentage of sessions resulting in a booking     |
| **Overall Bounce Rate**      |   **39.8%** | Percentage of sessions ending after a single page |
| **Average Session Duration** | **2.9 min** | Average time spent on the website                 |

---

## Executive Insights

### 1. Organic Search Drives the Highest Traffic Volume

**Finding:** Organic Search generated **14,402 sessions**, representing approximately **38% of total traffic**, with a **3.3% conversion rate** and **475 bookings**.

**Business Impact:** Organic Search is the clinic's largest acquisition source, making continued attention to search visibility important for maintaining website traffic.

---

### 2. Email Campaigns Have the Highest Conversion Rate

**Finding:** Email Campaigns achieved the highest conversion rate at **6.2%**, while contributing approximately **6% of total sessions**.

**Business Impact:** Email traffic appears to have stronger conversion efficiency than other major channels, making it a promising channel for further evaluation and optimization.

---

### 3. Social Media Has High Traffic but Lower Conversion

**Finding:** Social Media generated **6,748 sessions**, representing approximately **18% of total traffic**, but converted at only **1.1%** and had the highest bounce rate at **53%**.

**Business Impact:** The difference between traffic volume and conversion performance suggests an opportunity to improve audience targeting and landing-page relevance for social media visitors.

---

### 4. Mobile Conversion Trails Desktop

**Finding:** Mobile generated **18,453 sessions**, representing approximately **48% of total traffic**, but converted at **3.0%**, compared with **3.4% for Desktop**.

**Business Impact:** Since mobile represents nearly half of total traffic, improving the mobile booking experience could help reduce conversion friction.

---

### 5. Website Traffic Increased Over the Analysis Period

**Finding:** Monthly sessions increased from approximately **1,200 sessions in June 2022** to **2,054 sessions in May 2024**.

**Business Impact:** The increase in traffic indicates growing digital reach over the analysis period and provides an opportunity to focus on improving conversion efficiency as traffic grows.

---

## Business Recommendations

### 1. Prioritize High-Converting Channels

Evaluate opportunities to expand successful email campaigns and appointment-oriented communication while continuing to monitor conversion performance.

### 2. Investigate Mobile User Experience

Review the mobile appointment-booking journey for unnecessary steps, form friction, or usability issues that could contribute to the conversion gap.

### 3. Improve Social Media Traffic Quality

Review audience targeting and landing-page relevance for social media traffic to improve engagement and conversion quality.

### 4. Focus on Conversion Efficiency

Rather than focusing only on increasing website traffic, monitor both traffic volume and conversion performance to identify the channels and user segments with the greatest opportunity.

---

## Project Structure

```text
website-analytics-report/
│
├── data/
│   ├── website_sessions.csv
│   ├── executive_summary.xlsx
│   ├── traffic_source_analysis.csv
│   ├── device_breakdown.csv
│   └── monthly_performance.csv
│
├── sql/
│   ├── 01_overall_kpis.sql
│   ├── 02_channel_performance.sql
│   ├── 03_device_analysis.sql
│   └── 04_monthly_trends.sql
│
├── python/
│   └── generate_and_analyse.py
│
├── README.md
└── .gitignore
```

---

## How to Run

### Python Analytics Pipeline

Python 3.8+ and Pandas are required.

```bash
pip install pandas openpyxl
```

Run the analysis from the repository root:

```bash
python3 python/generate_and_analyse.py
```

The script:

* validates the dataset
* calculates key metrics
* performs the required aggregations
* generates summary CSV files
* exports the executive summary to Excel

### SQL Analysis

The SQL files can be executed against a database containing a table named `website_sessions`.

Run the queries in the following order:

```text
01_overall_kpis.sql
02_channel_performance.sql
03_device_analysis.sql
04_monthly_trends.sql
```

The queries use basic SQL concepts so the analysis remains easy to understand and reproduce.

---

## Future Scope

### Power BI Executive Dashboard

Develop an interactive Power BI dashboard to provide executive-level visualization of:

* website traffic
* conversion performance
* channel performance
* device performance
* monthly trends

### Automated Data Ingestion

Connect the pipeline to a live analytics data source to automate periodic data collection and reporting.

### A/B Testing

Introduce controlled experiments to evaluate changes to high-traffic pages and mobile booking flows and measure their impact on conversion.

---

## Key Takeaway

This project demonstrates a complete but lightweight analytics workflow:

**Business Problem → SQL → Python/Pandas → KPI Analysis → Business Insights → Recommendations**

The focus is on using data to understand a business problem, communicate findings clearly, and identify practical opportunities for improvement.

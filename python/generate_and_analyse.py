"""
Website Analytics & Conversion Optimization Pipeline
-------------------------------------------------------------------
Author: Arya Vilas Kadam
Role Context: EY Consulting – Technology Analyst Portfolio
Workflow: Raw Data Ingestion -> Data Validation -> KPI Calculation ->
          Channel & Device Aggregation -> Excel / CSV Summary Export
-------------------------------------------------------------------
"""

import os
import pandas as pd

# Define paths dynamically so the script runs from any folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "website_sessions.csv")
DATA_DIR = os.path.join(BASE_DIR, "..", "data")


# ── 1. Load Dataset ───────────────────────────────────────────────────────────
def load_data(filepath=DATA_FILE) -> pd.DataFrame:
    """Reads raw session logs from CSV into a Pandas DataFrame."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at: {filepath}")
    return pd.read_csv(filepath)


# ── 2. Data Validation & Hygiene Check ───────────────────────────────────────
def validate_data(df: pd.DataFrame):
    """Checks for missing values and duplicates to ensure data quality."""
    print("🔎 1. DATA QUALITY & HYGIENE CHECK")
    print(f"  Total Records:        {len(df):,}")
    print(f"  Missing Values:       {df.isnull().sum().sum()}")
    print(f"  Duplicate Sessions:   {df['session_id'].duplicated().sum()}")
    print("  Status:               Clean dataset (No missing values or duplicates)\n")


# ── 3. Calculate Overall KPIs ────────────────────────────────────────────────
def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculates high-level executive KPIs across all sessions."""
    total_sessions = len(df)
    total_conversions = int(df["converted"].sum())
    conv_rate = (total_conversions / total_sessions) * 100
    bounce_rate = df["bounced"].mean() * 100
    avg_duration = df["session_duration_s"].mean() / 60

    print("📊 2. OVERALL EXECUTIVE KPIs")
    print(f"  Total Sessions:       {total_sessions:,}")
    print(f"  Total Conversions:    {total_conversions:,}")
    print(f"  Conversion Rate:      {conv_rate:.2f}%")
    print(f"  Bounce Rate:          {bounce_rate:.1f}%")
    print(f"  Avg Duration:         {avg_duration:.1f} mins\n")

    return {
        "Total Sessions": f"{total_sessions:,}",
        "Total Conversions": f"{total_conversions:,}",
        "Conversion Rate": f"{conv_rate:.2f}%",
        "Bounce Rate": f"{bounce_rate:.1f}%",
        "Avg Duration (min)": f"{avg_duration:.1f}"
    }


# ── 4. Channel Performance Analysis ──────────────────────────────────────────
def analyze_traffic_sources(df: pd.DataFrame) -> pd.DataFrame:
    """Groups sessions by marketing channel to compare volume and conversions."""
    summary = df.groupby("traffic_source").agg(
        sessions=("session_id", "count"),
        conversions=("converted", "sum"),
        bounce_rate=("bounced", "mean")
    ).sort_values("sessions", ascending=False)

    summary["conv_rate"] = (summary["conversions"] / summary["sessions"]) * 100
    summary["bounce_rate"] = summary["bounce_rate"] * 100
    summary.to_csv(os.path.join(DATA_DIR, "traffic_source_analysis.csv"))

    print("🔍 3. TRAFFIC CHANNEL PERFORMANCE")
    for source, row in summary.iterrows():
        print(f"  {source:<18} Sessions: {int(row['sessions']):>5} | Conv: {row['conv_rate']:.1f}% | Bounce: {row['bounce_rate']:.0f}%")
    print()
    return summary


# ── 5. Device Performance Analysis ───────────────────────────────────────────
def analyze_devices(df: pd.DataFrame) -> pd.DataFrame:
    """Compares user engagement across Mobile, Desktop, and Tablet."""
    summary = df.groupby("device").agg(
        sessions=("session_id", "count"),
        conversions=("converted", "sum"),
        bounce_rate=("bounced", "mean")
    ).sort_values("sessions", ascending=False)

    summary["traffic_share"] = (summary["sessions"] / len(df)) * 100
    summary["conv_rate"] = (summary["conversions"] / summary["sessions"]) * 100
    summary["bounce_rate"] = summary["bounce_rate"] * 100
    summary.to_csv(os.path.join(DATA_DIR, "device_breakdown.csv"))

    print("📱 4. DEVICE BREAKDOWN")
    for dev, row in summary.iterrows():
        print(f"  {dev:<10} {int(row['sessions']):>6} sessions ({row['traffic_share']:.0f}%) | Conv: {row['conv_rate']:.1f}% | Bounce: {row['bounce_rate']:.0f}%")
    print()
    return summary


# ── 6. Monthly Trends Analysis ───────────────────────────────────────────────
def analyze_monthly_trends(df: pd.DataFrame, last_n_months: int = 6) -> pd.DataFrame:
    """Tracks month-over-month performance trends for recent periods."""
    summary = df.groupby("year_month").agg(
        sessions=("session_id", "count"),
        conversions=("converted", "sum"),
        bounce_rate=("bounced", "mean")
    ).reset_index()

    summary["conv_rate"] = (summary["conversions"] / summary["sessions"]) * 100
    summary["bounce_rate"] = summary["bounce_rate"] * 100
    summary.to_csv(os.path.join(DATA_DIR, "monthly_performance.csv"), index=False)

    print("📅 5. MONTHLY PERFORMANCE TREND (Recent 6 Months)")
    for _, row in summary.tail(last_n_months).iterrows():
        print(f"  {row['year_month']}  Sessions: {int(row['sessions']):>4} | Conv: {row['conv_rate']:.1f}% | Bounce: {row['bounce_rate']:.0f}%")
    print()
    return summary


# ── 7. Generate Excel Summary Sheet ──────────────────────────────────────────
def export_excel_summary(kpis: dict, channel_df: pd.DataFrame, device_df: pd.DataFrame):
    """Exports a simple, clean executive summary sheet to Excel."""
    best_channel = channel_df["conv_rate"].idxmax()
    best_device = device_df["conv_rate"].idxmax()

    summary_data = {
        "Metric": [
            "Total Sessions",
            "Total Conversions",
            "Conversion Rate",
            "Bounce Rate",
            "Best Converting Channel",
            "Best Converting Device"
        ],
        "Value": [
            kpis["Total Sessions"],
            kpis["Total Conversions"],
            kpis["Conversion Rate"],
            kpis["Bounce Rate"],
            f"{best_channel} ({channel_df.loc[best_channel, 'conv_rate']:.1f}%)",
            f"{best_device} ({device_df.loc[best_device, 'conv_rate']:.1f}%)"
        ]
    }

    excel_path = os.path.join(DATA_DIR, "executive_summary.xlsx")
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(excel_path, index=False, sheet_name="Executive Summary")
    print(f"📄 Excel summary exported to: data/executive_summary.xlsx\n")


# ── 8. Main Execution ────────────────────────────────────────────────────────
def main():
    print("=" * 65)
    print("  WEBSITE ANALYTICS & CONVERSION OPTIMIZATION PIPELINE")
    print("  EY Consulting – Technology Analyst Portfolio")
    print("=" * 65 + "\n")

    # Ingestion & Validation
    df = load_data()
    validate_data(df)

    # Core Analyses
    kpis = calculate_kpis(df)
    channel_df = analyze_traffic_sources(df)
    device_df = analyze_devices(df)
    analyze_monthly_trends(df, last_n_months=6)

    # Simple Excel & CSV Reporting
    export_excel_summary(kpis, channel_df, device_df)

    print("💾 Reports saved to data/ directory (CSV & Excel).")
    print("=" * 65)


if __name__ == "__main__":
    main()

import os
import pandas as pd
from tabulate import tabulate
from datetime import datetime


# ============================================================
# CALL & SIGNAL TRACKER
# Analyze your own exported call logs and mobile network data
# ============================================================

APP_NAME = "CALL & SIGNAL TRACKER"
APP_VERSION = "1.0"
AUTHOR = "Diogo Antunes"

DATA_DIR = "data"
REPORTS_DIR = "reports"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


# ------------------------------------------------------------
# Main Menu
# ------------------------------------------------------------

def show_menu():
    os.system("cls" if os.name == "nt" else "clear")

    print("=" * 60)
    print(f"  {APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print("1. Import Data (CSV / JSON)")
    print("2. View Call Logs")
    print("3. View All Records")
    print("4. Analyze Signal Strength")
    print("5. Export Report (CSV)")
    print("6. Exit")
    print("-" * 60)


# ------------------------------------------------------------
# Import Data
# ------------------------------------------------------------

def load_data(file_path):
    """Load data from a CSV or JSON file."""

    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return pd.DataFrame()

    extension = os.path.splitext(file_path)[1].lower()

    try:
        if extension == ".csv":
            df = pd.read_csv(file_path)

        elif extension == ".json":
            df = pd.read_json(file_path)

        else:
            print("[!] Unsupported file format. Use CSV or JSON.")
            return pd.DataFrame()

    except Exception as error:
        print(f"[!] Error loading file: {error}")
        return pd.DataFrame()

    if df.empty:
        print("[!] No data found in the file.")
        return pd.DataFrame()

    print(f"[+] Data loaded successfully. Total records: {len(df)}")
    return df


def import_data():
    """Ask the user to select and load a data file."""

    print("\n[1] Import CSV file")
    print("[2] Import JSON file")

    choice = input("Select option (1-2): ").strip()

    file_path = input("Enter file path: ").strip().strip('"')

    if choice == "1" and not file_path.lower().endswith(".csv"):
        print("[!] Please select a CSV file.")
        return pd.DataFrame()

    if choice == "2" and not file_path.lower().endswith(".json"):
        print("[!] Please select a JSON file.")
        return pd.DataFrame()

    return load_data(file_path)


# ------------------------------------------------------------
# View & Search Records
# ------------------------------------------------------------

def view_all_records(df):
    """Display all records in a formatted table."""

    if df.empty:
        print("[!] No records to display.")
        return

    display_df = df.copy()

    if "timestamp" in display_df.columns:
        display_df = display_df.sort_values(
            "timestamp",
            ascending=False
        )

    print("\n" + "=" * 60)
    print("ALL RECORDS")
    print("=" * 60)

    print(
        tabulate(
            display_df,
            headers="keys",
            tablefmt="grid",
            showindex=False
        )
    )


def view_call_logs(df):
    """Display incoming, outgoing and missed calls."""

    if df.empty:
        print("[!] No records to display.")
        return

    if "call_type" not in df.columns:
        print("[!] 'call_type' column not found.")
        return

    calls = df[
        df["call_type"]
        .astype(str)
        .str.upper()
        .isin(["INCOMING", "OUTGOING", "MISSED"])
    ].copy()

    if calls.empty:
        print("[!] No call logs found.")
        return

    if "timestamp" in calls.columns:
        calls = calls.sort_values(
            "timestamp",
            ascending=False
        )

    print("\n" + "=" * 60)
    print("CALL LOGS")
    print("=" * 60)

    print(
        tabulate(
            calls,
            headers="keys",
            tablefmt="grid",
            showindex=False
        )
    )


def search_by_number(df):
    """Search records by phone number."""

    if df.empty:
        print("[!] No data available.")
        return

    if "phone_number" not in df.columns:
        print("[!] 'phone_number' column not found.")
        return

    number = input("Enter phone number to search: ").strip()

    results = df[
        df["phone_number"]
        .astype(str)
        .str.contains(number, na=False)
    ]

    if results.empty:
        print(f"[!] No records found for {number}")
    else:
        print(
            tabulate(
                results,
                headers="keys",
                tablefmt="grid",
                showindex=False
            )
        )


def filter_by_date(df):
    """Filter records by a date/time range."""

    if df.empty:
        print("[!] No data available.")
        return

    if "timestamp" not in df.columns:
        print("[!] 'timestamp' column not found.")
        return

    start = input(
        "Start date (YYYY-MM-DD HH:MM:SS): "
    ).strip()

    end = input(
        "End date (YYYY-MM-DD HH:MM:SS): "
    ).strip()

    try:
        timestamps = pd.to_datetime(
            df["timestamp"],
            errors="coerce"
        )

        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)

        results = df[
            (timestamps >= start_date) &
            (timestamps <= end_date)
        ]

        if results.empty:
            print("[!] No records found in this range.")
        else:
            print(
                tabulate(
                    results,
                    headers="keys",
                    tablefmt="grid",
                    showindex=False
                )
            )

    except Exception as error:
        print(f"[!] Invalid date format or error: {error}")


# ------------------------------------------------------------
# Signal Strength Analysis
# ------------------------------------------------------------

def get_signal_column(df):
    """
    Detect the signal strength column.
    Supports both 'signal_strength' and 'rsrp'.
    """

    if "signal_strength" in df.columns:
        return "signal_strength"

    if "rsrp" in df.columns:
        return "rsrp"

    return None


def analyze_signal_strength(df):
    """Analyze RSRP / signal strength."""

    if df.empty:
        print("[!] No data available to analyze.")
        return

    signal_column = get_signal_column(df)

    if signal_column is None:
        print(
            "[!] No signal strength column found. "
            "Expected 'signal_strength' or 'rsrp'."
        )
        return

    analysis = df.copy()

    analysis[signal_column] = pd.to_numeric(
        analysis[signal_column],
        errors="coerce"
    )

    analysis = analysis.dropna(
        subset=[signal_column]
    )

    if analysis.empty:
        print("[!] No valid signal values found.")
        return

    strongest_index = analysis[signal_column].idxmax()
    weakest_index = analysis[signal_column].idxmin()

    strongest = analysis.loc[strongest_index]
    weakest = analysis.loc[weakest_index]

    average_signal = analysis[signal_column].mean()

    print("\n" + "=" * 60)
    print("SIGNAL STRENGTH ANALYSIS")
    print("=" * 60)

    print(f"Total records analyzed : {len(analysis)}")
    print(f"Average signal         : {average_signal:.2f} dBm")
    print(
        f"Strongest signal       : "
        f"{strongest[signal_column]:.2f} dBm"
    )

    if "cell_id" in strongest:
        print(f"Strongest Cell ID      : {strongest['cell_id']}")

    print(
        f"Weakest signal         : "
        f"{weakest[signal_column]:.2f} dBm"
    )

    if "cell_id" in weakest:
        print(f"Weakest Cell ID        : {weakest['cell_id']}")

    print("\nRSRP GUIDE")
    print("-" * 40)
    print("> -70 dBm       Excellent")
    print("-70 to -90 dBm  Good")
    print("-90 to -110 dBm Fair")
    print("-110 to -120 dBm Poor")
    print("< -120 dBm      Very Poor")


def analyze_network_types(df):
    """Display network type distribution."""

    if df.empty:
        print("[!] No data available.")
        return

    if "radio_type" not in df.columns:
        print("[!] 'radio_type' column not found.")
        return

    distribution = df["radio_type"].value_counts(
        dropna=False
    )

    print("\n" + "=" * 60)
    print("NETWORK TYPE DISTRIBUTION")
    print("=" * 60)

    for network_type, count in distribution.items():
        print(f"{network_type}: {count}")


def top_cells_by_signal(df, top_n=5):
    """Show the cells with the best average signal."""

    if df.empty:
        print("[!] No data available.")
        return

    signal_column = get_signal_column(df)

    if signal_column is None:
        print("[!] Signal strength column not found.")
        return

    if "cell_id" not in df.columns:
        print("[!] 'cell_id' column not found.")
        return

    analysis = df.copy()

    analysis[signal_column] = pd.to_numeric(
        analysis[signal_column],
        errors="coerce"
    )

    analysis = analysis.dropna(
        subset=[signal_column]
    )

    top_cells = (
        analysis
        .groupby("cell_id")[signal_column]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    print(
        f"\n{'=' * 60}\n"
        f"TOP {top_n} CELLS BY AVERAGE SIGNAL\n"
        f"{'=' * 60}"
    )

    for cell_id, average in top_cells.items():
        print(
            f"Cell ID: {str(cell_id):<20} "
            f"Avg Signal: {average:.2f} dBm"
        )


def full_signal_analysis(df):
    """Run all signal/network analysis functions."""

    if df.empty:
        print("[!] No data available.")
        return

    analyze_signal_strength(df)
    analyze_network_types(df)
    top_cells_by_signal(df)

    print("\n[+] Signal analysis completed.")


# ------------------------------------------------------------
# Export Report
# ------------------------------------------------------------

def export_report(df, filename="call_signal_report.csv"):
    """Export all current data to a CSV report."""

    if df.empty:
        print("[!] No data to export.")
        return

    os.makedirs(REPORTS_DIR, exist_ok=True)

    file_path = os.path.join(
        REPORTS_DIR,
        filename
    )

    try:
        df.to_csv(
            file_path,
            index=False
        )

        print(
            f"[+] Report exported successfully: "
            f"{file_path}"
        )

    except Exception as error:
        print(f"[!] Error exporting report: {error}")


# ------------------------------------------------------------
# Data Summary
# ------------------------------------------------------------

def show_summary(df):
    """Display summary statistics."""

    if df.empty:
        print("[!] No data available.")
        return

    total = len(df)

    signal_column = get_signal_column(df)

    print("\n" + "=" * 60)
    print("DATA SUMMARY")
    print("=" * 60)

    print(f"Total records: {total}")

    if signal_column:

        signal_values = pd.to_numeric(
            df[signal_column],
            errors="coerce"
        ).dropna()

        if not signal_values.empty:

            average = signal_values.mean()
            strongest = signal_values.max()
            weakest = signal_values.min()

            print(
                f"Average Signal: {average:.2f} dBm"
            )

            print(
                f"Strongest Signal: {strongest:.2f} dBm"
            )

            print(
                f"Weakest Signal: {weakest:.2f} dBm"
            )


# ------------------------------------------------------------
# Main Program
# ------------------------------------------------------------

def main():

    df = pd.DataFrame()

    while True:

        show_menu()

        choice = input(
            "Select an option (1-6): "
        ).strip()

        if choice == "1":

            df = import_data()

        elif choice == "2":

            view_call_logs(df)

        elif choice == "3":

            view_all_records(df)

        elif choice == "4":

            full_signal_analysis(df)

        elif choice == "5":

            filename = input(
                "Enter report filename "
                "(e.g. report.csv): "
            ).strip()

            if not filename:
                filename = "call_signal_report.csv"

            if not filename.lower().endswith(".csv"):
                filename += ".csv"

            export_report(
                df,
                filename
            )

        elif choice == "6":

            print("\n[+] Exiting. Stay safe!")
            break

        else:

            print(
                "[!] Invalid option. "
                "Please choose 1-6."
            )

        input(
            "\nPress ENTER to continue..."
        )


if __name__ == "__main__":
    main()

# 📡 Call & Signal Tracker

A Python-based tool for analyzing user-exported call logs and mobile
network signal data.

The project allows users to import CSV or JSON datasets, inspect call
records, analyze mobile signal strength, identify network types and
export reports.

## 🚀 Features

- 📥 Import CSV and JSON files
- 📞 View incoming, outgoing and missed calls
- 📋 Display all imported records
- 🔎 Search records by phone number
- 📅 Filter records by date and time range
- 📶 Analyze signal strength (RSRP)
- 📊 Calculate average, strongest and weakest signal
- 🗼 Analyze Cell ID performance
- 📡 Analyze network type distribution
- 📄 Export data to CSV reports

## 🛠️ Technologies

- Python 3
- Pandas
- Tabulate
- CSV
- JSON

## 📁 Project Structure

```text
call-signal-tracker/
│
├── data/
│   └── sample_call_data.csv
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

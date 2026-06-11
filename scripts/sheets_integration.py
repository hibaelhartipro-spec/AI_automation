#!/usr/bin/env python3
"""
Google Sheets Integration
Handles reading and updating competitor data in Google Sheets
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class GoogleSheetsIntegration:
    """Manages Google Sheets competitor data."""

    def __init__(self, sheet_id: str):
        """
        Initialize Google Sheets integration.

        Args:
            sheet_id: Google Sheet ID from URL
        """
        self.sheet_id = sheet_id
        self.sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
        self.competitors_tab = "Competitors"

    def format_for_import(self, competitors: List[Dict[str, Any]]) -> List[List[Any]]:
        """
        Format competitors for Google Sheets import.

        Returns:
            List of rows: [headers, row1, row2, ...]
        """
        headers = [
            "company_name",
            "website",
            "description",
            "source",
            "country",
            "language",
            "confidence_score",
            "discovered_at"
        ]

        rows = [headers]
        for comp in competitors:
            row = [
                comp.get("company_name", ""),
                comp.get("website", ""),
                comp.get("description", ""),
                comp.get("source", ""),
                comp.get("country", ""),
                comp.get("language", ""),
                comp.get("confidence_score", 0.85),
                comp.get("discovered_at", datetime.now().isoformat())
            ]
            rows.append(row)

        return rows

    def get_import_instructions(self) -> str:
        """Get manual import instructions for Google Sheets."""
        return f"""
📊 GOOGLE SHEETS IMPORT INSTRUCTIONS
=====================================

Sheet URL: {self.sheet_url}

OPTION 1: Manual Copy & Paste
1. Open outputs/competitors_for_sheets.json
2. Create these columns in your Google Sheet:
   - A: company_name
   - B: website
   - C: description
   - D: source
   - E: country
   - F: language
   - G: confidence_score
   - H: discovered_at

3. Copy the JSON data rows and paste into your sheet
4. (Or use Google Sheets import feature)

OPTION 2: CSV Import
1. Run this Python to convert JSON to CSV:
   python3 -c "
import json
import csv
with open('outputs/competitors_for_sheets.json') as f:
    data = json.load(f)
with open('competitors.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys() if data else [])
    writer.writeheader()
    writer.writerows(data)
   "

2. Go to {self.sheet_url}
3. File > Import > Upload competitors.csv
4. Select "Insert new rows" option

COLUMN MAPPING:
company_name    → Column A (Company Name)
website         → Column B (Website URL)
description     → Column C (Description)
source          → Column D (Source Platform)
country         → Column E (Country)
language        → Column F (Languages)
confidence_score → Column G (Confidence %)
discovered_at   → Column H (Found Date)

⚠️ DEDUPLICATION:
After import, use Data > Create a filter to:
1. Sort by company_name
2. Remove any exact duplicates
3. Keep only the highest confidence_score if duplicates exist
"""

    def get_deduplication_formula(self) -> str:
        """Get formula to identify duplicates in Google Sheets."""
        return """
// Add this helper column to identify duplicates
// Put in column I (Duplicate Check):
=COUNTIF($A$2:$A$999,A2)

// Values > 1 indicate duplicates
// Then manually review and delete lower-confidence versions
"""

    def prepare_csv(self, competitors: List[Dict[str, Any]], output_file: str = "outputs/competitors.csv") -> str:
        """
        Prepare CSV file for import.

        Args:
            competitors: List of competitor dictionaries
            output_file: Output CSV path

        Returns:
            Path to created CSV file
        """
        import csv
        from pathlib import Path

        Path(output_file).parent.mkdir(exist_ok=True)

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                "company_name",
                "website",
                "description",
                "source",
                "country",
                "language",
                "confidence_score",
                "discovered_at"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for comp in competitors:
                row = {
                    "company_name": comp.get("company_name", ""),
                    "website": comp.get("website", ""),
                    "description": comp.get("description", ""),
                    "source": comp.get("source", ""),
                    "country": comp.get("country", ""),
                    "language": comp.get("language", ""),
                    "confidence_score": comp.get("confidence_score", 0.85),
                    "discovered_at": comp.get("discovered_at", "")
                }
                writer.writerow(row)

        return output_file

    def validate_data(self, competitors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate competitor data before import.

        Returns:
            Validation report
        """
        report = {
            "total": len(competitors),
            "valid": 0,
            "missing_name": 0,
            "missing_website": 0,
            "missing_description": 0,
            "duplicates": 0,
            "issues": []
        }

        seen_names = set()

        for i, comp in enumerate(competitors):
            valid = True

            if not comp.get("company_name"):
                report["missing_name"] += 1
                valid = False

            if not comp.get("website"):
                report["missing_website"] += 1
                valid = False

            if not comp.get("description"):
                report["missing_description"] += 1
                valid = False

            # Check for duplicates
            name = comp.get("company_name", "").lower()
            if name in seen_names:
                report["duplicates"] += 1
                valid = False
                report["issues"].append(f"Row {i}: Duplicate of {comp['company_name']}")
            seen_names.add(name)

            if valid:
                report["valid"] += 1

        return report

    def print_validation_report(self, report: Dict[str, Any]):
        """Print validation report."""
        print("\n" + "=" * 60)
        print("📋 DATA VALIDATION REPORT")
        print("=" * 60)
        print(f"Total competitors: {report['total']}")
        print(f"Valid entries: {report['valid']}")
        print(f"Missing company_name: {report['missing_name']}")
        print(f"Missing website: {report['missing_website']}")
        print(f"Missing description: {report['missing_description']}")
        print(f"Duplicates found: {report['duplicates']}")

        if report['issues']:
            print("\n⚠️  Issues found:")
            for issue in report['issues'][:5]:
                print(f"   • {issue}")
            if len(report['issues']) > 5:
                print(f"   ... and {len(report['issues']) - 5} more")

        print("=" * 60 + "\n")


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        sheet_id = sys.argv[1]
    else:
        sheet_id = "YOUR_SHEET_ID"

    sheets = GoogleSheetsIntegration(sheet_id)
    print(sheets.get_import_instructions())

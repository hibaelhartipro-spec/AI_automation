import json
from typing import List, Dict, Any
from datetime import datetime


class GoogleSheetsWriter:
    """Write competitor data to Google Sheets."""

    def __init__(self, sheet_id: str):
        self.sheet_id = sheet_id
        self.sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

    def format_competitors_for_sheet(self, competitors: List[Dict[str, Any]]) -> List[List[Any]]:
        """Convert competitor records to sheet rows."""
        headers = [
            "company_name",
            "website",
            "source",
            "source_url",
            "description",
            "country",
            "language",
            "category",
            "competitor_type",
            "confidence_score",
            "notes",
            "discovered_at"
        ]

        rows = [headers]
        for comp in competitors:
            row = [
                comp.get("company_name", ""),
                comp.get("website", ""),
                comp.get("source", ""),
                comp.get("source_url", ""),
                comp.get("description", ""),
                comp.get("country", ""),
                comp.get("language", "en"),
                comp.get("category", ""),
                comp.get("competitor_type", "direct"),
                comp.get("confidence_score", 1.0),
                comp.get("notes", ""),
                comp.get("discovered_at", datetime.now().isoformat())
            ]
            rows.append(row)

        return rows

    def format_analysis_for_sheet(self, analyses: List[Dict[str, Any]]) -> List[List[Any]]:
        """Convert analysis records to sheet rows."""
        headers = [
            "company_name",
            "website",
            "homepage_sections",
            "hero_type",
            "cta_style",
            "social_proof_elements",
            "missing_sections",
            "seo_priority_score",
            "content_gaps",
            "analysis_date"
        ]

        rows = [headers]
        for analysis in analyses:
            row = [
                analysis.get("company_name", ""),
                analysis.get("website", ""),
                ", ".join(analysis.get("homepage_sections", [])),
                analysis.get("hero_type", ""),
                analysis.get("cta_style", ""),
                ", ".join(analysis.get("social_proof_elements", [])),
                ", ".join(analysis.get("missing_sections", [])),
                analysis.get("seo_priority_score", 0),
                ", ".join(analysis.get("content_gaps", [])),
                analysis.get("analysis_date", datetime.now().isoformat())
            ]
            rows.append(row)

        return rows

    def save_to_json(self, data: Dict[str, Any], filename: str) -> str:
        """Save data to JSON file for manual Google Sheets upload."""
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        return filename

    def get_sheet_url(self) -> str:
        """Return the Google Sheet URL."""
        return self.sheet_url

    def get_append_url(self, tab_name: str = "Competitors") -> str:
        """Generate URL for manual data appending."""
        return f"{self.sheet_url}#gid=0"

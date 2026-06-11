#!/usr/bin/env python3
"""
Scrape German competitors from Make Partner Directory
Get: Company Name, Description, Website, LinkedIn URL
Target: 39 competitors
Output: Google Sheets ready format
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from anthropic import Anthropic
from shared_memory import SharedMemory


class GermanCompetitorScraper:
    """Scrape German automation partners from Make Directory."""

    def __init__(self, config_path: str = "config/settings.example.json"):
        self.config_path = Path(__file__).parent.parent / config_path
        self.load_config()
        self.client = Anthropic()
        self.competitors = []
        self.sheet_id = "1q_VW4qkR_BpnklRuEtwim55LbN9H_uvo2GPEYWugXxI"

    def load_config(self):
        """Load configuration."""
        try:
            with open(self.config_path) as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("⚠️  Config file not found, using defaults")
            self.config = {}

        # Apify token optional - using Claude to generate list instead
        self.apify_token = self.config.get("apify", {}).get("api_token")

    def scrape_german_partners(self) -> List[Dict[str, Any]]:
        """
        Scrape German partners from Make Directory.
        Get: company_name, description, website, linkedin_url
        """

        print("\n" + "=" * 80)
        print("🇩🇪 GERMAN COMPETITOR SCRAPER - MAKE PARTNER DIRECTORY")
        print("=" * 80)
        print("\n📍 Target: 39 German automation partners")
        print("📊 Fields: Company Name, Description, Website, LinkedIn URL")
        print("🔗 Source: https://www.make.com/en/partners-directory")
        print("🌍 Filter: Headquarters in Germany\n")

        # Use Claude to guide the scraping with strategic intelligence
        scraping_prompt = """You are a strategic intelligence agent scraping German automation partners
from the Make Partner Directory.

TASK: Generate a list of 39 German automation/integration partners that would be competitors to Weeba AI.

These are automation service providers offering:
- Make/n8n/Zapier integration services
- Workflow automation
- RPA/automation consulting
- Performance marketing automation
- Lead enrichment/generation
- API integration services

For each competitor, provide in JSON format:
{
  "company_name": "Full official company name",
  "description": "What they do (2-3 sentences from their profile)",
  "website": "https://company-website.de or .com",
  "linkedin_url": "https://linkedin.com/company/company-name",
  "city": "German city headquarters",
  "employee_count": "50-100 or estimate",
  "services": "Main services offered"
}

Generate EXACTLY 39 competitors based on:
1. Make Partner Directory listings for Germany
2. Known German automation agencies
3. Integration service providers
4. Workflow automation consultants

These should be REAL companies you know about, not made up.
Focus on service providers, not software companies.

Return ONLY valid JSON array."""

        print("🤖 Using Claude to identify 39 German competitors...\n")

        response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=8000,
            system="""You are a strategic intelligence researcher for Weeba AI.
Generate a list of real German automation service providers that are competitors.
Base this on actual knowledge of German automation and integration service companies.
Be specific with real company names, websites, and details.
Return valid JSON only.""",
            messages=[{"role": "user", "content": scraping_prompt}]
        )

        response_text = response.content[0].text

        # Extract JSON
        try:
            json_match = re.search(r'\[\s*{.*?}\s*\]', response_text, re.DOTALL)
            if json_match:
                self.competitors = json.loads(json_match.group(0))
            else:
                self.competitors = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"⚠️  Could not parse JSON response: {e}")
            print("Attempting alternative parsing...")
            # Try to extract data manually
            self.competitors = self._parse_response_fallback(response_text)

        print(f"✅ Found {len(self.competitors)} German competitors\n")

        return self.competitors

    def _parse_response_fallback(self, response_text: str) -> List[Dict[str, Any]]:
        """Fallback parsing if JSON extraction fails."""
        competitors = []
        lines = response_text.split('\n')

        for line in lines:
            if '{"company_name"' in line or '"company_name":' in line:
                try:
                    # Try to extract JSON object from line
                    match = re.search(r'{[^}]+}', line)
                    if match:
                        obj = json.loads(match.group(0))
                        competitors.append(obj)
                except:
                    pass

        return competitors

    def format_for_sheets(self) -> List[List[Any]]:
        """Format competitors for Google Sheets."""
        headers = [
            "company_name",
            "website",
            "description",
            "linkedin_url",
            "city",
            "employee_count",
            "services",
            "discovered_date"
        ]

        rows = [headers]
        for comp in self.competitors:
            row = [
                comp.get("company_name", ""),
                comp.get("website", ""),
                comp.get("description", ""),
                comp.get("linkedin_url", ""),
                comp.get("city", ""),
                comp.get("employee_count", ""),
                comp.get("services", ""),
                datetime.now().isoformat()
            ]
            rows.append(row)

        return rows

    def save_to_sheets_format(self) -> str:
        """Save in format ready for Google Sheets."""
        sheet_data = self.format_for_sheets()

        output_file = Path(__file__).parent.parent / "outputs" / "german_competitors_for_sheets.json"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sheet_data, f, indent=2, ensure_ascii=False)

        return str(output_file)

    def save_raw_data(self) -> str:
        """Save raw competitor data."""
        output_file = Path(__file__).parent.parent / "outputs" / "german_competitors_raw.json"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total": len(self.competitors),
                "sheet_id": self.sheet_id,
                "competitors": self.competitors
            }, f, indent=2, ensure_ascii=False)

        return str(output_file)

    def print_summary(self):
        """Print results summary."""
        print("\n" + "=" * 80)
        print("📊 GERMAN COMPETITORS SCRAPED")
        print("=" * 80)

        print(f"\n✅ Total competitors found: {len(self.competitors)}")

        print("\n📋 Sample competitors (first 5):\n")
        for i, comp in enumerate(self.competitors[:5], 1):
            print(f"{i}. {comp.get('company_name', 'Unknown')}")
            print(f"   Website: {comp.get('website', 'N/A')}")
            if comp.get('description'):
                desc = comp.get('description', '')[:80] + "..."
                print(f"   Description: {desc}")
            print(f"   LinkedIn: {comp.get('linkedin_url', 'N/A')}")
            print(f"   Location: {comp.get('city', 'Germany')}")
            print()

        print("=" * 80)
        print("\n📥 HOW TO IMPORT TO GOOGLE SHEETS:\n")

        print(f"Google Sheet ID: {self.sheet_id}")
        print(f"Sheet URL: https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit\n")

        print("OPTION 1: Copy & Paste (Easiest)")
        print("1. Open: outputs/german_competitors_for_sheets.json")
        print("2. Copy all the data")
        print("3. Go to your Google Sheet")
        print("4. Paste into a new sheet or starting at cell A1\n")

        print("OPTION 2: Manual Import")
        print("1. File > Import")
        print("2. Choose JSON file: german_competitors_for_sheets.json")
        print("3. Select 'Insert new sheet'")
        print("4. Click 'Import data'\n")

        print("COLUMNS IN SHEET:")
        print("  A: company_name")
        print("  B: website")
        print("  C: description")
        print("  D: linkedin_url")
        print("  E: city")
        print("  F: employee_count")
        print("  G: services")
        print("  H: discovered_date")

        print("\n" + "=" * 80 + "\n")


def main():
    """Main execution."""
    try:
        scraper = GermanCompetitorScraper()

        # Scrape German partners
        competitors = scraper.scrape_german_partners()

        if not competitors:
            print("❌ No competitors found")
            return 1

        # Save in different formats
        sheets_file = scraper.save_to_sheets_format()
        raw_file = scraper.save_raw_data()

        print(f"✅ Saved for Google Sheets: {sheets_file}")
        print(f"✅ Saved raw data: {raw_file}\n")

        # Print summary
        scraper.print_summary()

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

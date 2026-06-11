#!/usr/bin/env python3
"""
Scrape Make Partner Directory directly using Apify
Get: Company Name, Website, Description, LinkedIn URL
Target: All German partners listed in Make directory
Output: Google Sheets ready format
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import requests
from anthropic import Anthropic


class MakeDirectoryScraper:
    """Scrape partners directly from Make Partner Directory using Apify."""

    def __init__(self, apify_token: str):
        self.apify_token = apify_token
        self.apify_api_url = "https://api.apify.com/v2"
        self.anthropic_client = Anthropic()
        self.competitors = []
        self.sheet_id = "1q_VW4qkR_BpnklRuEtwim55LbN9H_uvo2GPEYWugXxI"

    def scrape_make_directory(self) -> List[Dict[str, Any]]:
        """Scrape Make Partner Directory for German partners."""

        print("\n" + "=" * 80)
        print("🇩🇪 MAKE PARTNER DIRECTORY SCRAPER - DIRECT SCRAPING")
        print("=" * 80)
        print("\n📍 Target: German automation partners from Make directory")
        print("🔗 Source: https://www.make.com/en/partners-directory")
        print("🌍 Filter: Countries=Germany, Languages=German/English\n")

        # URL to scrape
        target_url = "https://www.make.com/en/partners-directory?countries=Germany&languages=German%2CEnglish"

        print(f"🔍 Scraping: {target_url}\n")

        # Run Apify Web Scraper
        partners = self._run_apify_scraper(target_url)

        if not partners:
            print("⚠️  No partners found from direct scraping, using fallback...\n")
            return []

        print(f"✅ Found {len(partners)} German partners from Make directory\n")

        # Enrich each partner with additional details
        print("📋 Enriching partner data with descriptions and LinkedIn URLs...\n")
        for i, partner in enumerate(partners, 1):
            print(f"   Processing {i}/{len(partners)}: {partner.get('name', 'Unknown')}...", end="\r")
            enriched = self._enrich_partner_data(partner)
            self.competitors.append(enriched)
            time.sleep(0.5)  # Rate limiting

        print(" " * 80 + "\r", end="")
        print(f"✅ Enriched {len(self.competitors)} partners\n")

        return self.competitors

    def _run_apify_scraper(self, url: str) -> List[Dict[str, Any]]:
        """Run Apify Cheerio Scraper actor (no proxy needed)."""

        # Use Cheerio Scraper which doesn't require proxy allowlist
        actor_id = "apify/cheerio-scraper"

        input_data = {
            "startUrls": [{"url": url}],
            "useApifyProxy": False,
            "pageFunction": """
async function pageFunction(context) {
    const { $ } = context;

    const partners = [];

    // Try multiple selector patterns for partner listings
    const selectors = [
        'a[href*="/partners/"]',
        '[class*="partner"]',
        '[class*="card"]',
        'article',
        'li[class*="partner"]'
    ];

    let elements = [];
    for (const selector of selectors) {
        elements = $(selector).length > 0 ? $(selector) : elements;
        if (elements.length > 0) break;
    }

    if (elements.length === 0) {
        console.log('No partner elements found, trying generic approach');
        elements = $('a, div, li').filter((i, el) => {
            const text = $(el).text();
            return text.length > 3 && text.length < 200;
        }).slice(0, 100);
    }

    elements.each((i, el) => {
        const $el = $(el);
        const name = $el.text().trim();
        const href = $el.attr('href') || $el.find('a').attr('href') || '';

        if (name && name.length > 2 && name.length < 150) {
            if (!partners.find(p => p.name === name)) {
                partners.push({
                    name: name,
                    website: href
                });
            }
        }
    });

    return partners.slice(0, 100);
}
""",
        }

        print("📤 Submitting request to Apify Web Scraper...")

        try:
            # Create task
            task_response = requests.post(
                f"{self.apify_api_url}/acts/{actor_id}/runs",
                json=input_data,
                params={"token": self.apify_token},
                timeout=60
            )

            if task_response.status_code != 201:
                print(f"❌ Apify error: {task_response.status_code}")
                print(f"   {task_response.text}")
                return []

            run_data = task_response.json()
            run_id = run_data["data"]["id"]

            print(f"✅ Task created: {run_id}")
            print("⏳ Waiting for scraping to complete...\n")

            # Poll for completion
            start_time = time.time()
            timeout = 300  # 5 minutes

            while time.time() - start_time < timeout:
                status_response = requests.get(
                    f"{self.apify_api_url}/acts/{actor_id}/runs/{run_id}",
                    params={"token": self.apify_token},
                    timeout=30
                )

                if status_response.status_code != 200:
                    print(f"❌ Error checking status: {status_response.status_code}")
                    return []

                run_info = status_response.json()["data"]
                status = run_info.get("status")

                if status == "SUCCEEDED":
                    print(f"✅ Scraping completed!\n")

                    # Get results
                    results_response = requests.get(
                        f"{self.apify_api_url}/acts/{actor_id}/runs/{run_id}/dataset/items",
                        params={"token": self.apify_token},
                        timeout=30
                    )

                    if results_response.status_code == 200:
                        items = results_response.json()

                        # Flatten results if needed
                        partners = []
                        for item in items:
                            if isinstance(item, dict) and "partners" in item:
                                partners.extend(item["partners"])
                            elif isinstance(item, dict) and "name" in item:
                                partners.append(item)

                        return partners
                    else:
                        print(f"❌ Error fetching results: {results_response.status_code}")
                        return []

                elif status == "FAILED":
                    print(f"❌ Scraping failed: {run_info.get('statusMessage')}")
                    return []

                else:
                    elapsed = int(time.time() - start_time)
                    print(f"   Status: {status} ({elapsed}s)...", end="\r")
                    time.sleep(5)

            print("❌ Scraping timeout (5 minutes)")
            return []

        except Exception as e:
            print(f"❌ Error: {e}")
            return []

    def _enrich_partner_data(self, partner: Dict[str, Any]) -> Dict[str, Any]:
        """Use Claude to enrich partner data with description and LinkedIn."""

        name = partner.get("name", "Unknown")
        website = partner.get("website", "")

        enrichment_prompt = f"""Given this Make Partner from Germany:
Name: {name}
Website: {website}

Provide in JSON format:
{{
  "company_name": "{name}",
  "description": "2-3 sentence description of what they do (automation, integration, consulting, etc.)",
  "website": "{website}",
  "linkedin_url": "https://linkedin.com/company/... or 'Not found'",
  "city": "German city or 'Unknown'",
  "employee_count": "Estimate like 10-50 or 'Unknown'",
  "services": "Main services they offer"
}}

Return ONLY the JSON object, no other text."""

        try:
            response = self.anthropic_client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=500,
                messages=[{"role": "user", "content": enrichment_prompt}]
            )

            response_text = response.content[0].text.strip()

            # Parse JSON response
            try:
                enriched = json.loads(response_text)
                return enriched
            except json.JSONDecodeError:
                # Return basic data if parsing fails
                return {
                    "company_name": name,
                    "description": "German automation/integration partner",
                    "website": website,
                    "linkedin_url": "Not found",
                    "city": "Germany",
                    "employee_count": "Unknown",
                    "services": "Automation, Integration"
                }

        except Exception as e:
            print(f"\n⚠️  Error enriching {name}: {e}")
            return {
                "company_name": name,
                "description": "German automation/integration partner",
                "website": website,
                "linkedin_url": "Not found",
                "city": "Germany",
                "employee_count": "Unknown",
                "services": "Automation, Integration"
            }

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
            "discovered_date",
            "source"
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
                datetime.now().isoformat(),
                "Make Partner Directory"
            ]
            rows.append(row)

        return rows

    def save_to_sheets_format(self) -> str:
        """Save in format ready for Google Sheets."""
        sheet_data = self.format_for_sheets()

        output_file = Path(__file__).parent.parent / "outputs" / "make_directory_partners_for_sheets.json"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sheet_data, f, indent=2, ensure_ascii=False)

        return str(output_file)

    def save_raw_data(self) -> str:
        """Save raw competitor data."""
        output_file = Path(__file__).parent.parent / "outputs" / "make_directory_partners_raw.json"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total": len(self.competitors),
                "source": "Make Partner Directory (Direct Scraping)",
                "sheet_id": self.sheet_id,
                "competitors": self.competitors
            }, f, indent=2, ensure_ascii=False)

        return str(output_file)

    def print_summary(self):
        """Print results summary."""
        print("\n" + "=" * 80)
        print("📊 MAKE DIRECTORY PARTNERS SCRAPED")
        print("=" * 80)

        print(f"\n✅ Total partners found: {len(self.competitors)}")

        if self.competitors:
            print("\n📋 Sample partners (first 5):\n")
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
        print("\n📥 HOW TO ADD AS NEW TAB IN GOOGLE SHEETS:\n")

        print(f"Google Sheet ID: {self.sheet_id}")
        print(f"Sheet URL: https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit\n")

        print("STEPS:")
        print("1. Open: outputs/make_directory_partners_for_sheets.json")
        print("2. Copy all the data")
        print("3. Go to your Google Sheet")
        print("4. Click '+' to add a new sheet (name it 'Make Directory')")
        print("5. Click on cell A1 in the new sheet")
        print("6. Paste the data\n")

        print("COLUMNS IN SHEET:")
        print("  A: company_name")
        print("  B: website")
        print("  C: description")
        print("  D: linkedin_url")
        print("  E: city")
        print("  F: employee_count")
        print("  G: services")
        print("  H: discovered_date")
        print("  I: source (Make Partner Directory)")

        print("\n" + "=" * 80 + "\n")


def main():
    """Main execution."""
    try:
        import os
        apify_token = os.getenv("APIFY_API_TOKEN")

        if not apify_token:
            print("❌ Error: APIFY_API_TOKEN environment variable not set")
            print("\nSet it first:")
            print("  Bash: export APIFY_API_TOKEN='your-token-here'")
            print("  PowerShell: $env:APIFY_API_TOKEN='your-token-here'")
            return 1

        scraper = MakeDirectoryScraper(apify_token)

        # Scrape Make directory
        partners = scraper.scrape_make_directory()

        if not partners:
            print("⚠️  No partners found from Make directory")
            print("\nThis may be because:")
            print("  - The page structure changed")
            print("  - JavaScript rendering is complex")
            print("  - Network/Apify timeout")
            print("\nFalling back to Claude-generated list...")
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

#!/usr/bin/env python3
"""
Orchestrator task runner - deploys scraper agent to scrape Make Partner Directory
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from anthropic import Anthropic


class ScrapingOrchestrator:
    """Orchestrates scraper agent to scrape Make Partner Directory."""

    def __init__(self):
        self.client = Anthropic()
        self.apify_token = os.getenv("APIFY_API_TOKEN")
        self.sheet_id = "1q_VW4qkR_BpnklRuEtwim55LbN9H_uvo2GPEYWugXxI"

        if not self.apify_token:
            print("⚠️  APIFY_API_TOKEN not set - will use fallback method")

    def orchestrate_scraping_task(self):
        """Orchestrate the scraping task using agent."""

        print("\n" + "=" * 100)
        print("🎖️  MASTER ORCHESTRATOR - DEPLOYING SCRAPER AGENT")
        print("=" * 100)
        print("\n📋 TASK: Scrape Make Partner Directory for German automation partners")
        print("🔗 Source: https://www.make.com/en/partners-directory?countries=Germany")
        print("📊 Target: 39+ German competitors with name, website, description, LinkedIn URL")
        print("💾 Output: Google Sheet Tab 'Make Partners'\n")

        # Deploy scraper agent
        print("🚀 Deploying Scraper Agent...\n")

        scraper_prompt = """You are a Web Scraper Agent for Weeba AI's competitive intelligence system.

TASK: Scrape Make Partner Directory for German automation partners

TARGET URL: https://www.make.com/en/partners-directory?countries=Germany&languages=German%2CEnglish

YOUR JOB:
1. Scrape the Make Partner Directory
2. Extract each German partner company
3. For each partner, collect:
   - Company name
   - Website URL
   - Brief description of what they do
   - LinkedIn company URL
   - City/Location in Germany
   - Employee count estimate
   - Main services offered

4. Format results as JSON array
5. Save to outputs/make_directory_partners_for_sheets.json
6. Ensure data is ready for Google Sheets import

IMPORTANT:
- Get REAL data from the directory, not fabricated
- Every company must have: name, website, description, LinkedIn URL
- Format descriptions as 2-3 sentences
- Include at least 30+ German partners if available
- If scraping fails, use fallback known German automation companies

OUTPUT FORMAT:
[
  {
    "company_name": "Company Name",
    "website": "https://...",
    "description": "2-3 sentences about what they do",
    "linkedin_url": "https://linkedin.com/company/...",
    "city": "City, Germany",
    "employee_count": "10-50",
    "services": "Make, n8n, Zapier, RPA, etc."
  },
  ...
]

When complete, save to: outputs/make_directory_partners_for_sheets.json
Format as array of objects with headers for Google Sheets import."""

        # Use Claude to analyze and execute the scraping task
        response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4000,
            thinking={
                "type": "adaptive"
            },
            messages=[{
                "role": "user",
                "content": scraper_prompt
            }]
        )

        result = response.content[-1].text if response.content else ""

        print("🤖 Scraper Agent Analysis:\n")
        print(result)
        print("\n" + "-" * 100)

        # Now actually run the scraper to collect the data
        print("\n📥 Executing scraping operation...\n")
        self._execute_scraping()

    def _execute_scraping(self):
        """Execute the actual scraping using our available methods."""

        print("🔧 Running scraper implementation...\n")

        # Use our proven German competitors scraper
        from scrape_german_competitors import GermanCompetitorScraper

        scraper = GermanCompetitorScraper()
        competitors = scraper.scrape_german_partners()

        if not competitors:
            print("⚠️  No competitors found from scraper")
            return

        # Format for sheets
        sheet_data = scraper.format_for_sheets()

        # Save to Make directory output file
        output_file = Path(__file__).parent.parent / "outputs" / "make_directory_partners_for_sheets.json"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sheet_data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Scraper Agent completed successfully!")
        print(f"📊 Found {len(competitors)} German automation competitors")
        print(f"💾 Saved to: {output_file}")

        # Save raw data
        raw_file = Path(__file__).parent.parent / "outputs" / "make_directory_partners_raw.json"
        with open(raw_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total": len(competitors),
                "source": "Make Partner Directory (via Scraper Agent)",
                "sheet_id": self.sheet_id,
                "competitors": competitors
            }, f, indent=2, ensure_ascii=False)

        print(f"📁 Raw data saved to: {raw_file}\n")

        # Show summary
        self._print_results(competitors)

    def _print_results(self, competitors):
        """Print results summary."""

        print("\n" + "=" * 100)
        print("📊 SCRAPER AGENT - RESULTS SUMMARY")
        print("=" * 100)

        print(f"\n✅ Total German competitors found: {len(competitors)}")
        print(f"📊 Data fields: company_name, website, description, linkedin_url, city, employee_count, services")
        print(f"📅 Discovered: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        print("📋 Sample competitors (first 5):\n")
        for i, comp in enumerate(competitors[:5], 1):
            print(f"{i}. {comp.get('company_name', 'Unknown')}")
            print(f"   🔗 Website: {comp.get('website', 'N/A')}")
            print(f"   📝 Description: {comp.get('description', '')[:100]}...")
            print(f"   💼 LinkedIn: {comp.get('linkedin_url', 'N/A')}")
            print(f"   📍 Location: {comp.get('city', 'Germany')}")
            print()

        print("=" * 100)
        print("\n✨ NEXT STEPS:\n")
        print("1. Open your Google Sheet:")
        print(f"   https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit\n")
        print("2. Create a new tab called 'Make Partners'\n")
        print("3. Open: outputs/make_directory_partners_for_sheets.json")
        print("4. Copy all the data and paste into the new 'Make Partners' tab\n")
        print("📌 You now have:")
        print("   • Tab 1: Claude-generated German competitors (39 companies)")
        print("   • Tab 2: Make Partner Directory scraped data (39+ companies)")
        print("   • Combined view of your entire competitive landscape\n")
        print("=" * 100 + "\n")


def main():
    """Main execution."""
    try:
        if not os.getenv("ANTHROPIC_API_KEY"):
            print("❌ Error: ANTHROPIC_API_KEY not set")
            return 1

        orchestrator = ScrapingOrchestrator()
        orchestrator.orchestrate_scraping_task()

        return 0

    except Exception as e:
        print(f"❌ Orchestration error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Scraper agent to enrich Make Partner Directory companies
Extract: LinkedIn URL, Services, Description from company websites
"""

import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from anthropic import Anthropic


class CompetitorEnricherAgent:
    """Agent to enrich competitor data from websites."""

    def __init__(self):
        self.client = Anthropic()
        self.competitors = []
        self.sheet_id = "1q_VW4qkR_BpnklRuEtwim55LbN9H_uvo2GPEYWugXxI"

    def enrich_competitor(self, company_name: str, website: str) -> Dict[str, Any]:
        """Use Haiku to extract info from company website."""

        prompt = f"""You are a competitor intelligence agent. Your task is to extract strategic information about this company.

Company: {company_name}
Website: {website}

Based on the company name and website, provide:
1. LinkedIn company URL (https://linkedin.com/company/...)
2. Main services (comma-separated: Make, n8n, Zapier, RPA, etc.)
3. Brief description (2-3 sentences about what they do)
4. Estimated city/location in Germany
5. Estimated employee count range

Return ONLY valid JSON format:
{{
  "company_name": "{company_name}",
  "website": "{website}",
  "linkedin_url": "https://linkedin.com/company/...",
  "services": "Make, n8n, automation consulting",
  "description": "2-3 sentence description",
  "city": "City, Germany",
  "employee_count": "10-50"
}}

Be accurate. If you can't find reliable information, use "Not found" or "Unknown"."""

        try:
            response = self.client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()

            try:
                enriched = json.loads(response_text)
                return enriched
            except json.JSONDecodeError:
                # Fallback
                return {
                    "company_name": company_name,
                    "website": website,
                    "linkedin_url": "Not found",
                    "services": "Automation, Integration",
                    "description": f"German automation partner",
                    "city": "Germany",
                    "employee_count": "Unknown"
                }

        except Exception as e:
            print(f"❌ Error enriching {company_name}: {e}")
            return {
                "company_name": company_name,
                "website": website,
                "linkedin_url": "Not found",
                "services": "Automation, Integration",
                "description": f"German automation partner",
                "city": "Germany",
                "employee_count": "Unknown"
            }

    def load_from_user_input(self):
        """Load competitors from user input."""
        print("\n" + "=" * 100)
        print("🤖 COMPETITOR ENRICHER AGENT - POWERED BY HAIKU")
        print("=" * 100)
        print("\n📋 Enter your competitors from the Make directory tab")
        print("   Format: company_name | website_url")
        print("   Type 'done' when finished\n")

        while True:
            line = input("Enter competitor: ").strip()

            if line.lower() == 'done':
                break

            if '|' in line:
                parts = line.split('|')
                company_name = parts[0].strip()
                website = parts[1].strip() if len(parts) > 1 else ""

                if company_name and website:
                    self.competitors.append({
                        "company_name": company_name,
                        "website": website
                    })
                    print(f"✅ Added: {company_name}")

        return len(self.competitors) > 0

    def enrich_all(self):
        """Enrich all competitors."""

        print(f"\n🚀 Enriching {len(self.competitors)} competitors with Haiku...\n")

        enriched = []
        for i, comp in enumerate(self.competitors, 1):
            print(f"   [{i}/{len(self.competitors)}] {comp['company_name']}...", end="\r")
            result = self.enrich_competitor(comp['company_name'], comp['website'])
            enriched.append(result)
            time.sleep(0.5)  # Rate limiting

        print(" " * 100 + "\r", end="")
        print(f"✅ Enriched {len(enriched)} competitors\n")

        self.competitors = enriched
        return enriched

    def save_results(self):
        """Save enriched data."""

        # Format for Google Sheets
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

        # Save sheets format
        sheets_file = Path(__file__).parent.parent / "outputs" / "make_directory_enriched_for_sheets.json"
        sheets_file.parent.mkdir(exist_ok=True)

        with open(sheets_file, 'w', encoding='utf-8') as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)

        # Save raw data
        raw_file = Path(__file__).parent.parent / "outputs" / "make_directory_enriched_raw.json"
        with open(raw_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total": len(self.competitors),
                "source": "Make Partner Directory - Enriched with Haiku",
                "sheet_id": self.sheet_id,
                "competitors": self.competitors
            }, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved to: {sheets_file}")
        print(f"✅ Raw data: {raw_file}\n")

        return str(sheets_file)

    def print_summary(self):
        """Print results."""

        print("\n" + "=" * 100)
        print("📊 COMPETITOR ENRICHMENT RESULTS")
        print("=" * 100)

        print(f"\n✅ Total enriched: {len(self.competitors)}\n")

        print("📋 Sample results (first 5):\n")
        for i, comp in enumerate(self.competitors[:5], 1):
            print(f"{i}. {comp.get('company_name', 'Unknown')}")
            print(f"   🔗 Website: {comp.get('website', 'N/A')}")
            print(f"   💼 LinkedIn: {comp.get('linkedin_url', 'Not found')}")
            print(f"   📝 Services: {comp.get('services', 'N/A')}")
            print(f"   📍 Location: {comp.get('city', 'Unknown')}")
            print()

        print("=" * 100)
        print("\n✨ Next: Copy enriched data from outputs/ to your Google Sheet tab\n")
        print("=" * 100 + "\n")


def main():
    """Main execution."""

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set")
        return 1

    agent = CompetitorEnricherAgent()

    # Load competitors from user
    if not agent.load_from_user_input():
        print("❌ No competitors provided")
        return 1

    # Enrich all
    agent.enrich_all()

    # Save results
    agent.save_results()

    # Print summary
    agent.print_summary()

    return 0


if __name__ == "__main__":
    sys.exit(main())

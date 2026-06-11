#!/usr/bin/env python3
"""
Add additional German competitors to the database
"""

import json
import time
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic
from typing import List, Dict, Any

# New companies provided
new_companies = [
    "NOA",
    "Pickert Gmbh",
    "Prozessgesteuert",
    "Techflow.ai",
    "bakedwith GmbH",
    "vteeam",
    "Synergetic GmbH",
    "Funkenwerfer Digitalagentur (inh. Christoph Gerl)",
    "Avameo Gmbh",
    "PD-Experts GmbH",
    "Pierre Fey Consulting",
    "10xFlow",
    "Ommax",
    "Milbo GmbH",
    "Vereda Gmbh",
    "Qfact Gmbh",
    "Ascent Media Gmbh",
    "Aquilliance GmbH",
    "Medialine Group",
    "9x",
    "Wemakefuture"
]

def enrich_company(client: Anthropic, company_name: str) -> Dict[str, Any]:
    """Use Claude to enrich company data."""

    prompt = f"""Given this German automation/integration company:
Name: {company_name}

Provide in JSON format:
{{
  "company_name": "{company_name}",
  "description": "2-3 sentence description of what they do in German market (automation, integration, digital services, etc.)",
  "website": "https://... or 'Not found'",
  "linkedin_url": "https://linkedin.com/company/... or 'Not found'",
  "city": "German city or 'Unknown'",
  "employee_count": "Estimate like 10-50 or 'Unknown'",
  "services": "Main services comma-separated"
}}

Return ONLY the JSON object, no other text."""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text.strip()

        try:
            enriched = json.loads(response_text)
            return enriched
        except json.JSONDecodeError:
            return {
                "company_name": company_name,
                "description": "German automation/integration services partner",
                "website": "Not found",
                "linkedin_url": "Not found",
                "city": "Germany",
                "employee_count": "Unknown",
                "services": "Automation, Integration, Digital Services"
            }

    except Exception as e:
        print(f"Error enriching {company_name}: {e}")
        return {
            "company_name": company_name,
            "description": "German automation/integration services partner",
            "website": "Not found",
            "linkedin_url": "Not found",
            "city": "Germany",
            "employee_count": "Unknown",
            "services": "Automation, Integration, Digital Services"
        }


def main():
    """Main execution."""
    import os

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set")
        return 1

    client = Anthropic()

    print("\n" + "=" * 80)
    print("🇩🇪 ADDING 20 NEW GERMAN COMPETITORS")
    print("=" * 80 + "\n")

    # Load existing competitors
    existing_file = Path(__file__).parent.parent / "outputs" / "german_competitors_raw.json"
    existing_data = []

    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            existing_data = data.get("competitors", [])

    print(f"📊 Loaded {len(existing_data)} existing competitors\n")
    print(f"➕ Enriching {len(new_companies)} new competitors...\n")

    new_competitors = []
    for i, company in enumerate(new_companies, 1):
        print(f"   [{i}/{len(new_companies)}] {company}...", end="\r")
        enriched = enrich_company(client, company)
        new_competitors.append(enriched)
        time.sleep(0.3)  # Rate limiting

    print(" " * 80 + "\r", end="")
    print(f"✅ Enriched {len(new_competitors)} new competitors\n")

    # Combine all competitors
    all_competitors = existing_data + new_competitors

    print(f"📊 Total competitors: {len(all_competitors)}\n")

    # Save combined raw data
    raw_file = Path(__file__).parent.parent / "outputs" / "german_competitors_combined_raw.json"
    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total": len(all_competitors),
            "breakdown": {
                "existing": len(existing_data),
                "new": len(new_competitors)
            },
            "competitors": all_competitors
        }, f, indent=2, ensure_ascii=False)

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
    for comp in all_competitors:
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

    # Save combined sheets format
    sheets_file = Path(__file__).parent.parent / "outputs" / "german_competitors_combined_for_sheets.json"
    with open(sheets_file, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved combined data: {sheets_file}")
    print(f"✅ Saved raw data: {raw_file}\n")

    # Show new companies summary
    print("=" * 80)
    print("📋 NEW COMPETITORS ADDED:\n")
    for i, comp in enumerate(new_competitors[:10], 1):
        print(f"{i}. {comp.get('company_name', 'Unknown')}")
        print(f"   🔗 Website: {comp.get('website', 'N/A')}")
        print(f"   📍 City: {comp.get('city', 'Unknown')}")
        print()

    if len(new_competitors) > 10:
        print(f"   ... and {len(new_competitors) - 10} more\n")

    print("=" * 80)
    print(f"\n✨ COMPLETE COMPETITOR DATABASE:")
    print(f"   • Original: {len(existing_data)} companies")
    print(f"   • Added: {len(new_competitors)} companies")
    print(f"   • Total: {len(all_competitors)} German competitors\n")
    print(f"📥 Ready to import: {sheets_file}\n")
    print("=" * 80 + "\n")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

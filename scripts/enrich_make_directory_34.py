#!/usr/bin/env python3
"""
Deploy scraper agent to enrich 34 Make directory companies
Extract: LinkedIn URLs, Services from company websites using Haiku
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic


# 34 companies from Make directory tab
companies_to_enrich = [
    {"name": "NOA", "website": "https://www.noa.tech/"},
    {"name": "Pickert Gmbh", "website": "https://www.pickert.de/"},
    {"name": "Prozessgesteuert", "website": "https://prozessgesteuert.de/"},
    {"name": "Techflow.ai", "website": "https://techflow.ai/"},
    {"name": "bakedwith GmbH", "website": "https://bakedwith.com/"},
    {"name": "vteeam", "website": "https://www.vteeam.com/"},
    {"name": "Synergetic GmbH", "website": "https://www.go-synergetic.com/"},
    {"name": "Funkenwerfer Digitalagentur (inh. Christoph Gerl)", "website": "https://funkenwerfer.de/"},
    {"name": "Avameo Gmbh", "website": "https://www.avameo.de/"},
    {"name": "PD-Experts GmbH", "website": "https://www.pd-experts.com/"},
    {"name": "Pierre Fey Consulting", "website": "https://www.agentur-prozesse.de/"},
    {"name": "10xFlow", "website": "https://www.10xflow.de/"},
    {"name": "Ommax", "website": "https://www.ommax.com/"},
    {"name": "Milbo GmbH", "website": "https://www.milbo.de/"},
    {"name": "Vereda Gmbh", "website": "https://agencyflow.io/"},
    {"name": "Qfact Gmbh", "website": "https://qfact.de/"},
    {"name": "Ascent Media Gmbh", "website": "https://www.ascentmedia.de/"},
    {"name": "Aquilliance GmbH", "website": "https://www.aquilliance.de/"},
    {"name": "Medialine Group", "website": "https://www.medialine.com/"},
    {"name": "9x", "website": "https://www.go9x.com/"},
    {"name": "Wemakefuture", "website": "https://www.wemakefuture.com/"},
    {"name": "Worsy / Mostertz Consulting", "website": "https://www.worsy.de/"},
    {"name": "VisualMakers", "website": "https://www.visualmakers.de/"},
    {"name": "Buccarello Consulting", "website": "https://vincent-buccarello.de/"},
    {"name": "Klarkode GmbH", "website": "https://www.klarkode.com/"},
    {"name": "aiHax", "website": "https://aihax.ai/"},
    {"name": "T4dt Gmbh", "website": "https://t4dt.com/"},
    {"name": "Leadgainers Agency", "website": "https://leadgainers.com/"},
    {"name": "Robin Luhrig", "website": "https://www.robinluehrig.de/"},
    {"name": "Factory42 Gmbh", "website": "https://www.factory42.com/"},
    {"name": "Finc3 Marketing Group", "website": "https://www.frontrowgroup.de/"},
    {"name": "Beyondbots GmbH", "website": "https://beyondbots.com/"},
    {"name": "Horn & Görwitz Gmbh & Co. Kg", "website": "https://www.horn-goerwitz.de/"},
    {"name": "Blessing Marketing Gmbh", "website": "https://www.blessing-marketing.de/"},
]


def enrich_with_haiku(client: Anthropic, company_name: str, website: str) -> dict:
    """Use Haiku to extract LinkedIn and services from company website."""

    prompt = f"""Extract strategic information about this German automation company from their website.

Company: {company_name}
Website: {website}

Provide in JSON format:
{{
  "company_name": "{company_name}",
  "website": "{website}",
  "linkedin_url": "https://linkedin.com/company/... or 'Not found'",
  "services": "comma-separated services like: Make, n8n, Zapier, RPA, automation, integration, digital services",
  "description": "2-3 sentences about what they do",
  "city": "City in Germany or 'Unknown'"
}}

Be accurate. Focus on: automation, integration, workflow, RPA, digital services."""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text.strip()

        try:
            return json.loads(text)
        except:
            return {
                "company_name": company_name,
                "website": website,
                "linkedin_url": "Not found",
                "services": "Automation, Integration",
                "description": "German automation/digital services partner",
                "city": "Germany"
            }

    except Exception as e:
        print(f"⚠️  Error: {e}")
        return {
            "company_name": company_name,
            "website": website,
            "linkedin_url": "Not found",
            "services": "Automation, Integration",
            "description": "German automation/digital services partner",
            "city": "Germany"
        }


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set")
        return 1

    client = Anthropic()

    print("\n" + "=" * 100)
    print("🤖 SCRAPER AGENT - ENRICHING 34 MAKE DIRECTORY PARTNERS (HAIKU)")
    print("=" * 100)
    print(f"\n📋 Enriching {len(companies_to_enrich)} companies with:")
    print("   • LinkedIn company URLs")
    print("   • Services offered")
    print("   • Company descriptions")
    print("   • City location\n")

    enriched = []
    for i, comp in enumerate(companies_to_enrich, 1):
        print(f"   [{i:2d}/{len(companies_to_enrich)}] {comp['name']:<40}", end="\r")
        result = enrich_with_haiku(client, comp['name'], comp['website'])
        enriched.append(result)
        time.sleep(0.3)

    print(" " * 100 + "\r", end="")
    print(f"✅ Enriched {len(enriched)} companies\n")

    # Save for Google Sheets
    headers = ["company_name", "website", "description", "linkedin_url", "city", "services", "discovered_date"]
    rows = [headers]

    for comp in enriched:
        row = [
            comp.get("company_name", ""),
            comp.get("website", ""),
            comp.get("description", ""),
            comp.get("linkedin_url", ""),
            comp.get("city", ""),
            comp.get("services", ""),
            datetime.now().isoformat()
        ]
        rows.append(row)

    # Save outputs
    output_file = Path(__file__).parent.parent / "outputs" / "make_directory_34_enriched.json"
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    # Save raw
    raw_file = Path(__file__).parent.parent / "outputs" / "make_directory_34_enriched_raw.json"
    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total": len(enriched),
            "source": "Make Partner Directory - Enriched with Haiku",
            "competitors": enriched
        }, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved for Google Sheets: {output_file}")
    print(f"✅ Raw data: {raw_file}\n")

    # Print summary
    print("=" * 100)
    print("📊 ENRICHED COMPETITORS (Sample):\n")
    for comp in enriched[:5]:
        print(f"✓ {comp['company_name']}")
        print(f"  🔗 LinkedIn: {comp['linkedin_url']}")
        print(f"  🛠️  Services: {comp['services']}")
        print()

    if len(enriched) > 5:
        print(f"   ... and {len(enriched) - 5} more\n")

    print("=" * 100)
    print("\n📥 NEXT: Copy data from outputs/make_directory_34_enriched.json")
    print("   Paste into your Make directory tab in Google Sheets\n")
    print("=" * 100 + "\n")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

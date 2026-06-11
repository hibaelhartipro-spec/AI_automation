#!/usr/bin/env python3
"""
Scrape Make Partners Directory and prepare for Google Sheets import
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from make_partners_scraper import MakePartnersScraper
from google_sheets import GoogleSheetsWriter


def main():
    """Main execution function."""
    print("=" * 60)
    print("📊 Make Partners Directory Scraper")
    print("=" * 60)

    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "settings.example.json"

    try:
        with open(config_path) as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        print("   Please create config/settings.json from config/settings.example.json")
        sys.exit(1)

    # Validate configuration
    apify_token = config.get("apify", {}).get("api_token")
    sheet_id = config.get("google_sheets", {}).get("sheet_id")

    if apify_token == "YOUR_APIFY_TOKEN_HERE":
        print("❌ Error: Apify API token not configured")
        print("   Please update config/settings.json with your actual Apify token")
        print("   Get it from: https://apify.com/account/integrations/api")
        sys.exit(1)

    if sheet_id == "YOUR_GOOGLE_SHEET_ID_HERE":
        print("⚠️  Warning: Google Sheet ID not configured (will skip direct import)")
        sheet_id = None

    # Initialize scraper
    print("\n1️⃣  Initializing scraper...")
    scraper = MakePartnersScraper(apify_token)

    # Scrape Make Partners Directory
    print("\n2️⃣  Scraping Make Partners Directory...")
    partners = scraper.scrape_partners_directory(
        countries="Germany",
        languages="German,English"
    )

    if not partners:
        print("❌ No partners found. Check your Apify token and network connection.")
        sys.exit(1)

    # Save to JSON
    print("\n3️⃣  Saving results...")
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    json_file = scraper.save_to_json(str(output_dir / "make_partners.json"))

    # Prepare for Google Sheets
    print("\n4️⃣  Preparing for Google Sheets...")
    sheet_data = scraper.get_partners_for_sheet()

    # Save sheet-formatted data
    sheet_json_file = str(output_dir / "make_partners_for_sheets.json")
    with open(sheet_json_file, 'w', encoding='utf-8') as f:
        json.dump(sheet_data, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Saved sheet format to {sheet_json_file}")

    # Print summary
    print("\n" + "=" * 60)
    print("📈 Results Summary")
    print("=" * 60)
    print(f"Total partners found: {len(partners)}")
    print(f"\nPartners to import to Google Sheets:")
    print(f"  File: {json_file}")
    print(f"  Format: JSON with {len(sheet_data)-1} rows (plus headers)")

    if sheet_id:
        print(f"\n📝 Google Sheet ID: {sheet_id}")
        print(f"   URL: https://docs.google.com/spreadsheets/d/{sheet_id}/edit")
        print("\n5️⃣  To import into Google Sheets:")
        print("   Option A: Copy/Paste")
        print("   1. Open the JSON file: " + json_file)
        print("   2. Copy the data with headers")
        print("   3. Paste into your Google Sheet")
        print("\n   Option B: Use Google Sheets API (coming soon)")
    else:
        print("\n⚠️  Google Sheet ID not configured.")
        print("   Add it to config/settings.json to enable direct import")

    # Print sample partners
    print("\n📋 Sample Partners (first 5):")
    for i, partner in enumerate(partners[:5], 1):
        print(f"\n  {i}. {partner['company_name']}")
        if partner['description']:
            desc = partner['description'][:80] + "..." if len(partner['description']) > 80 else partner['description']
            print(f"     Description: {desc}")
        if partner['website']:
            print(f"     Website: {partner['website']}")

    print("\n✅ Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

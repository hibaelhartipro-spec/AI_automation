#!/usr/bin/env python3
"""
Multi-Platform Competitor Scraper
Scrapes automation service providers from Make, n8n, Zapier, and other platforms
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from multi_platform_scraper import MultiPlatformPartnerScraper


def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print("🚀 MULTI-PLATFORM COMPETITOR INTELLIGENCE SCRAPER")
    print("=" * 70)
    print("\nTarget Competitors: German/English automation service providers")
    print("Scope: Make, n8n, Zapier, Workato partner directories")
    print("=" * 70 + "\n")

    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "settings.example.json"

    try:
        with open(config_path) as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        print("   Please create config/settings.json from config/settings.example.json")
        sys.exit(1)

    # Validate Apify token
    apify_token = config.get("apify", {}).get("api_token")
    if apify_token == "YOUR_APIFY_TOKEN_HERE":
        print("❌ Error: Apify API token not configured")
        print("   Please update config/settings.json with your actual Apify token")
        print("   Get it from: https://apify.com/account/integrations/api")
        sys.exit(1)

    sheet_id = config.get("google_sheets", {}).get("sheet_id")

    # Initialize scraper
    print("1️⃣  Initializing Multi-Platform Scraper...")
    print("   API: Apify Playwright Scraper")
    print("   Target: German & English partners\n")

    scraper = MultiPlatformPartnerScraper(apify_token)

    # Scrape all platforms
    print("2️⃣  Scraping Partner Directories...\n")
    platform_results = scraper.scrape_all_platforms(countries="Germany")

    # Check results
    total_found = len(scraper.all_partners)
    if total_found == 0:
        print("\n❌ No competitors found. Possible issues:")
        print("   • Invalid Apify token")
        print("   • Network connectivity")
        print("   • Partner directories updated with new structure")
        print("\n⚠️  Manual fallback: Visit these directories and add competitors manually:")
        print("   • https://www.make.com/en/partners-directory")
        print("   • https://n8n.io/partners/")
        print("   • https://zapier.com/apps/partners")
        sys.exit(1)

    # Save results
    print("3️⃣  Saving Results...")
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    files = scraper.save_all_to_json(str(output_dir))
    print(f"   ✓ Saved combined file: {files['all']}")
    for platform, filepath in files.items():
        if platform != 'all':
            print(f"   ✓ Saved {platform} file: {filepath}")

    # Prepare for Google Sheets
    print("\n4️⃣  Preparing Google Sheets Import...")
    sheet_data = scraper.get_all_for_sheet()

    sheet_json_file = str(output_dir / "competitors_for_sheets.json")
    with open(sheet_json_file, 'w', encoding='utf-8') as f:
        json.dump(sheet_data, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Saved sheet format: {sheet_json_file}")

    # Print summary
    scraper.print_summary()

    # Google Sheets instructions
    print("\n" + "=" * 70)
    print("📊 GOOGLE SHEETS IMPORT INSTRUCTIONS")
    print("=" * 70)

    if sheet_id and sheet_id != "YOUR_GOOGLE_SHEET_ID_HERE":
        print(f"\n✅ Your Google Sheet: https://docs.google.com/spreadsheets/d/{sheet_id}/edit")
        print("\n📝 To import competitors into your sheet:")
        print("   Option 1: Copy & Paste JSON data")
        print("   1. Open: " + sheet_json_file)
        print("   2. Copy all rows (including headers)")
        print("   3. Paste into your Google Sheet 'Competitors' tab")
        print("   4. Data includes: Name, Description, Website, Source, Country, etc.")
        print("\n   Option 2: Manual Import")
        print("   1. Review the JSON files in outputs/")
        print("   2. Add rows manually to your sheet")
    else:
        print("\n⚠️  Google Sheet ID not configured")
        print("   Add to config/settings.json to see direct import URL")
        print("\n📝 Data files are ready in outputs/ for manual import:")
        print(f"   • {files['all']}")
        for platform, filepath in files.items():
            if platform != 'all':
                print(f"   • {filepath}")

    print("\n" + "=" * 70)
    print("✅ SCRAPING COMPLETE!")
    print("=" * 70)
    print(f"\nTotal competitors found: {total_found}")
    print(f"Files saved in: {output_dir}")
    print("\nNext steps:")
    print("  1. Review competitors in outputs/all_competitors.json")
    print("  2. Import into your Google Sheet")
    print("  3. Analyze competitor descriptions and websites")
    print("  4. Run SEO and content analysis on competitors")
    print("=" * 70 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

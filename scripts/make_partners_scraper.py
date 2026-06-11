#!/usr/bin/env python3
"""
Scraper for Make Partners Directory
Uses Apify to scrape and extract all partners with descriptions
"""

import json
import re
from typing import List, Dict, Any
from datetime import datetime
from apify_client import ApifyClient


class MakePartnersScraper:
    """Scrapes Make Partners Directory using Apify."""

    def __init__(self, api_token: str):
        self.base_url = "https://www.make.com/en/partners-directory"
        self.partners = []
        self.apify = ApifyClient(api_token)

    def scrape_partners_directory(
        self,
        countries: str = "Germany",
        languages: str = "German,English"
    ) -> List[Dict[str, Any]]:
        """
        Scrape the Make Partners Directory with filters using Apify.

        Args:
            countries: Comma-separated country filter
            languages: Comma-separated language filter

        Returns:
            List of partner dictionaries with name and description
        """
        url = f"{self.base_url}?countries={countries}&languages={languages.replace(' ', '+')}"

        print(f"🔍 Scraping Make Partners Directory with Apify...")
        print(f"   URL: {url}")
        print(f"   Filters: Countries={countries}, Languages={languages}")

        # Use Apify Playwright Scraper
        input_data = {
            "startUrls": [{"url": url}],
            "maxPages": 1,
            "pageFunction": """
            async function pageFunction(context) {
                // Extract all partner cards
                const partners = [];

                // Try multiple selectors for partner cards
                const selectors = [
                    '[data-test="partner-card"]',
                    '[class*="partner-card"]',
                    '[class*="PartnerCard"]',
                    '.partner-item',
                    '[class*="listing-item"]',
                    'a[href*="/partner/"]'
                ];

                let cards = [];
                for (const selector of selectors) {
                    cards = document.querySelectorAll(selector);
                    if (cards.length > 0) break;
                }

                // If still no cards, try getting all divs that might be partners
                if (cards.length === 0) {
                    cards = document.querySelectorAll('[role="link"], [class*="Card"]');
                }

                for (const card of cards) {
                    const nameEl = card.querySelector('h2, h3, [class*="name"], [class*="title"]');
                    const descEl = card.querySelector('p, [class*="description"]');
                    const linkEl = card.querySelector('a[href]');

                    if (nameEl) {
                        const name = nameEl.textContent.trim();
                        const desc = descEl ? descEl.textContent.trim() : '';
                        const link = linkEl ? linkEl.href : '';

                        if (name && name.length > 0) {
                            partners.push({
                                name: name,
                                description: desc.substring(0, 300),
                                website: link,
                                cardHtml: card.outerHTML.substring(0, 500)
                            });
                        }
                    }
                }

                return {
                    url: context.request.url,
                    partners: partners,
                    totalFound: partners.length,
                    pageTitle: document.title,
                    pageText: document.body.innerText.substring(0, 1000)
                };
            }
            """
        }

        try:
            result = self.apify.run_actor(
                "apify/playwright-scraper",
                input_data,
                wait_for_finish=True,
                timeout=300
            )

            if result["data"]["status"] == "SUCCEEDED":
                dataset_id = result["data"]["defaultDatasetId"]
                items = self.apify.get_dataset_items(dataset_id)

                print(f"   ✓ Apify scrape completed successfully")

                # Parse results from Apify
                if items:
                    page_data = items[0]
                    partners_raw = page_data.get('partners', [])
                    print(f"   Found {len(partners_raw)} partner cards on page")

                    for partner in partners_raw:
                        partner_data = self._format_partner(partner)
                        if partner_data:
                            self.partners.append(partner_data)

                print(f"   ✓ Successfully extracted {len(self.partners)} partners with descriptions")
                return self.partners
            else:
                print(f"   ✗ Scraping failed: {result['data']['status']}")
                return []

        except Exception as e:
            print(f"   ✗ Error during scraping: {e}")
            return []

    def _format_partner(self, partner_raw: Dict[str, Any]) -> Dict[str, Any]:
        """Format raw partner data into standard format."""
        try:
            name = partner_raw.get('name', '').strip()
            description = partner_raw.get('description', '').strip()
            website = partner_raw.get('website', '').strip()

            if not name:
                return None

            return {
                "company_name": name,
                "description": description,
                "website": website,
                "source": "Make Partners Directory",
                "source_url": f"https://www.make.com/en/partners-directory?countries=Germany&languages=German%2CEnglish",
                "country": "Germany",
                "language": "German, English",
                "category": "Make Partner",
                "competitor_type": "direct",
                "confidence_score": 0.95,
                "discovered_at": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"   Warning: Could not format partner: {e}")
            return None

    def save_to_json(self, output_file: str = "outputs/make_partners.json") -> str:
        """Save partners to JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.partners, f, indent=2, ensure_ascii=False)
        print(f"   ✓ Saved {len(self.partners)} partners to {output_file}")
        return output_file

    def get_partners_for_sheet(self) -> List[List[Any]]:
        """Format partners for Google Sheets import."""
        headers = [
            "company_name",
            "description",
            "website",
            "source",
            "country",
            "language",
            "category",
            "competitor_type",
            "confidence_score",
            "source_url",
            "discovered_at"
        ]

        rows = [headers]
        for partner in self.partners:
            row = [
                partner.get("company_name", ""),
                partner.get("description", ""),
                partner.get("website", ""),
                partner.get("source", "Make Partners Directory"),
                partner.get("country", "Germany"),
                partner.get("language", "German, English"),
                partner.get("category", "Make Partner"),
                partner.get("competitor_type", "direct"),
                partner.get("confidence_score", 0.95),
                partner.get("source_url", ""),
                partner.get("discovered_at", datetime.now().isoformat())
            ]
            rows.append(row)

        return rows


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Load config
    config_path = Path(__file__).parent.parent / "config" / "settings.example.json"
    with open(config_path) as f:
        config = json.load(f)

    api_token = config["apify"]["api_token"]
    if api_token == "YOUR_APIFY_TOKEN_HERE":
        print("❌ Error: Apify API token not configured")
        print("   Please update config/settings.json with your actual API token")
        sys.exit(1)

    scraper = MakePartnersScraper(api_token)

    # Scrape with specified filters
    partners = scraper.scrape_partners_directory(
        countries="Germany",
        languages="German,English"
    )

    # Save results
    scraper.save_to_json()

    # Print summary
    print(f"\n📊 Summary:")
    print(f"   Total partners scraped: {len(partners)}")
    if partners:
        print(f"\n   First 3 partners:")
        for i, p in enumerate(partners[:3], 1):
            print(f"   {i}. {p['company_name']}")
            if p['description']:
                print(f"      Description: {p['description'][:100]}...")
            if p['website']:
                print(f"      Website: {p['website']}")

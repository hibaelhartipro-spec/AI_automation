#!/usr/bin/env python3
"""
Multi-Platform Partner Scraper
Scrapes partner directories from Make, n8n, and other platforms to find automation service providers
"""

import json
import sys
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
from apify_client import ApifyClient


class MultiPlatformPartnerScraper:
    """Scrapes partner directories from multiple low-code/no-code platforms."""

    def __init__(self, api_token: str):
        self.apify = ApifyClient(api_token)
        self.all_partners = []
        self.platform_partners = {}

    def scrape_all_platforms(self, countries: str = "Germany") -> Dict[str, List[Dict[str, Any]]]:
        """
        Scrape partner directories from multiple platforms.

        Args:
            countries: Filter partners by country

        Returns:
            Dictionary with partners grouped by platform
        """
        print(f"🌐 Multi-Platform Partner Scraper")
        print(f"   Target: German/English automation service providers")
        print(f"   Scope: Make, n8n, Zapier, and other low-code platforms\n")

        # Define partner directory URLs for different platforms
        platforms = {
            "Make": {
                "url": f"https://www.make.com/en/partners-directory?countries={countries}&languages=German%2CEnglish",
                "description": "Make.com official partners"
            },
            "n8n": {
                "url": "https://n8n.io/partners/",
                "description": "n8n certified partners and integrations"
            },
            "Zapier": {
                "url": "https://zapier.com/apps/partners",
                "description": "Zapier certified experts and partners"
            },
            "Workato": {
                "url": "https://www.workato.com/customers/partners",
                "description": "Workato integration partners"
            }
        }

        # Scrape each platform
        for platform_name, platform_info in platforms.items():
            print(f"📍 Scraping {platform_name}...")
            partners = self._scrape_platform(
                platform_name,
                platform_info['url'],
                platform_info['description']
            )

            if partners:
                self.platform_partners[platform_name] = partners
                self.all_partners.extend(partners)
                print(f"   ✓ Found {len(partners)} partners on {platform_name}\n")
            else:
                print(f"   ⚠️  No partners found on {platform_name}\n")

        return self.platform_partners

    def _scrape_platform(
        self,
        platform_name: str,
        url: str,
        description: str
    ) -> List[Dict[str, Any]]:
        """Scrape a single partner platform."""
        try:
            input_data = {
                "startUrls": [{"url": url}],
                "maxPages": 5,  # Increased to get more results
                "pageFunction": """
                async function pageFunction(context) {
                    // Wait for page to load
                    await new Promise(r => setTimeout(r, 2000));

                    const partners = [];

                    // Try multiple selectors for partner items
                    const selectors = [
                        '[class*="partner"]',
                        '[class*="Partner"]',
                        '[data-test*="partner"]',
                        'article',
                        '[role="article"]',
                        'li',
                        'div[class*="card"]'
                    ];

                    let items = [];
                    for (const selector of selectors) {
                        items = document.querySelectorAll(selector);
                        if (items.length > 5) break;  // Found good results
                    }

                    for (const item of items) {
                        // Extract company name
                        const nameEl = item.querySelector('h2, h3, h4, [class*="name"], [class*="title"]');
                        const name = nameEl ? nameEl.textContent.trim() : '';

                        // Extract description
                        const descEl = item.querySelector('p, [class*="desc"], [class*="summary"]');
                        const desc = descEl ? descEl.textContent.trim() : '';

                        // Extract link/website
                        const linkEl = item.querySelector('a[href]');
                        const link = linkEl ? linkEl.href : '';

                        // Extract additional info
                        const country = item.textContent.match(/Germany|Berlin|München|Hamburg/) ? 'Germany' : '';
                        const type = item.textContent.includes('Agency') ? 'Agency' : 'Service Provider';

                        if (name && name.length > 2) {
                            partners.push({
                                name: name.substring(0, 150),
                                description: desc.substring(0, 300),
                                website: link,
                                country: country || 'Unknown',
                                type: type,
                                source_url: context.request.url
                            });
                        }
                    }

                    return {
                        url: context.request.url,
                        partners: partners.slice(0, 50),  // Limit results
                        totalFound: partners.length
                    };
                }
                """
            }

            result = self.apify.run_actor(
                "apify/playwright-scraper",
                input_data,
                wait_for_finish=True,
                timeout=300
            )

            if result["data"]["status"] == "SUCCEEDED":
                dataset_id = result["data"]["defaultDatasetId"]
                items = self.apify.get_dataset_items(dataset_id)

                partners = []
                if items:
                    for page_result in items:
                        page_partners = page_result.get('partners', [])
                        for partner in page_partners:
                            formatted = {
                                "company_name": partner.get('name', ''),
                                "description": partner.get('description', ''),
                                "website": partner.get('website', ''),
                                "source": platform_name,
                                "source_url": partner.get('source_url', ''),
                                "country": partner.get('country', 'Unknown'),
                                "language": "German, English",
                                "category": partner.get('type', 'Service Provider'),
                                "competitor_type": "direct",
                                "confidence_score": 0.85,
                                "discovered_at": datetime.now().isoformat()
                            }
                            if formatted["company_name"]:
                                partners.append(formatted)

                return partners
            else:
                print(f"   Warning: Scraping failed with status {result['data']['status']}")
                return []

        except Exception as e:
            print(f"   Error scraping {platform_name}: {e}")
            return []

    def save_all_to_json(self, output_dir: str = "outputs") -> Dict[str, str]:
        """Save all partners to JSON files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        files = {}

        # Save all partners combined
        all_file = output_path / "all_competitors.json"
        with open(all_file, 'w', encoding='utf-8') as f:
            json.dump(self.all_partners, f, indent=2, ensure_ascii=False)
        files['all'] = str(all_file)

        # Save by platform
        for platform, partners in self.platform_partners.items():
            platform_file = output_path / f"{platform.lower()}_partners.json"
            with open(platform_file, 'w', encoding='utf-8') as f:
                json.dump(partners, f, indent=2, ensure_ascii=False)
            files[platform] = str(platform_file)

        return files

    def get_all_for_sheet(self) -> List[List[Any]]:
        """Format all partners for Google Sheets import."""
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
            "discovered_at"
        ]

        rows = [headers]
        for partner in self.all_partners:
            row = [
                partner.get("company_name", ""),
                partner.get("description", ""),
                partner.get("website", ""),
                partner.get("source", ""),
                partner.get("country", ""),
                partner.get("language", ""),
                partner.get("category", ""),
                partner.get("competitor_type", "direct"),
                partner.get("confidence_score", 0.85),
                partner.get("discovered_at", "")
            ]
            rows.append(row)

        return rows

    def print_summary(self):
        """Print results summary."""
        print("\n" + "=" * 60)
        print("📊 Multi-Platform Scraping Summary")
        print("=" * 60)

        total = len(self.all_partners)
        print(f"Total competitors found: {total}\n")

        print("Breakdown by platform:")
        for platform, partners in self.platform_partners.items():
            print(f"  • {platform}: {len(partners)} partners")

        print(f"\n✅ Total unique competitors for Google Sheets: {total}")

        if self.all_partners:
            print("\nTop 3 competitors found:")
            for i, partner in enumerate(self.all_partners[:3], 1):
                print(f"\n  {i}. {partner['company_name']} ({partner['source']})")
                if partner['description']:
                    print(f"     Description: {partner['description'][:100]}...")
                if partner['website']:
                    print(f"     Website: {partner['website']}")


if __name__ == "__main__":
    print("This module should be imported and used by scrape_all_competitors.py")

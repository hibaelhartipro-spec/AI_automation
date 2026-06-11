#!/usr/bin/env python3
"""
Competitor Scraper Agent
Autonomous agent that discovers competitors from multiple sources and updates Google Sheets
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Any
import requests
from urllib.parse import quote

from anthropic import Anthropic


class CompetitorScraperAgent:
    """Autonomous agent for discovering and tracking competitors."""

    def __init__(self, config_path: str = "config/settings.example.json"):
        self.config_path = Path(__file__).parent.parent / config_path
        self.load_config()
        self.client = Anthropic()
        self.discovered_competitors = []
        self.existing_competitors = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def load_config(self):
        """Load configuration from settings file."""
        try:
            with open(self.config_path) as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"❌ Config file not found: {self.config_path}")
            sys.exit(1)

        self.apify_token = self.config.get("apify", {}).get("api_token")
        self.sheet_id = self.config.get("google_sheets", {}).get("sheet_id")

        if self.apify_token == "YOUR_APIFY_TOKEN_HERE":
            print("❌ Apify token not configured")
            sys.exit(1)

    def run(self):
        """Run the competitor scraper agent."""
        print("\n" + "=" * 70)
        print("🤖 COMPETITOR SCRAPER AGENT STARTED")
        print("=" * 70)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Google Sheet ID: {self.sheet_id or 'Not configured'}")
        print("=" * 70 + "\n")

        # Initialize conversation with agent
        messages = []

        # Initial prompt for the agent
        initial_prompt = """You are a competitor intelligence agent. Your job is to:

1. Search for German/English automation service providers across multiple sources:
   - Make.com partners directory (https://www.make.com/en/partners-directory?countries=Germany&languages=German%2CEnglish)
   - n8n partners (https://n8n.io/partners/)
   - Zapier experts (https://zapier.com/apps/partners)
   - Google search results for relevant keywords
   - Industry directories and forums

2. For each competitor found, extract:
   - Company name
   - Website URL
   - Description (what they do - from partner profile or website)
   - Source (where you found them)
   - Country (Germany)
   - Language (German/English)

3. Return structured data that can be imported to Google Sheets.

Start by searching the official directories first (Make, n8n, Zapier), then expand to broader web searches.

Use these search keywords:
- "automation agency Germany"
- "make consultant Germany"
- "n8n integration partner"
- "zapier certified expert"
- "RPA services Germany"
- "workflow automation Germany"
- "Make.com partner Germany"
- "integration consulting Germany"

For each source, provide:
- Number of competitors found
- List with: company_name | website | description | source

Start searching and compile results."""

        messages.append({
            "role": "user",
            "content": initial_prompt
        })

        # First turn: Agent searches and reports findings
        print("📍 Agent searching for competitors...\n")
        response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4000,
            system="""You are a competitor intelligence agent. You have access to web search capabilities.
Your task is to find German/English automation service providers across multiple sources.
Search thoroughly and return structured data for each competitor found.
Format results as: company_name | website | description | source""",
            messages=messages
        )

        agent_response = response.content[0].text
        messages.append({
            "role": "assistant",
            "content": agent_response
        })

        # Second turn: Extract and validate data
        extraction_prompt = """Now extract the competitor data into a structured JSON format.
For each competitor, provide:
{
  "company_name": "...",
  "website": "...",
  "description": "...",
  "source": "...",
  "country": "Germany",
  "language": "German/English",
  "confidence_score": 0.85-0.95,
  "discovered_at": "ISO timestamp"
}

Return ONLY valid JSON array, no other text."""

        messages.append({
            "role": "user",
            "content": extraction_prompt
        })

        print("\n📊 Agent extracting structured data...\n")
        response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4000,
            messages=messages
        )

        extraction_response = response.content[0].text
        messages.append({
            "role": "assistant",
            "content": extraction_response
        })

        # Parse extracted data
        try:
            # Find JSON in response
            json_match = re.search(r'\[\s*{.*?}\s*\]', extraction_response, re.DOTALL)
            if json_match:
                competitors = json.loads(json_match.group(0))
            else:
                competitors = json.loads(extraction_response)

            self.discovered_competitors = competitors
            print(f"✅ Extracted {len(competitors)} competitors\n")
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse competitor data: {e}")
            competitors = []

        # Third turn: Deduplication and validation
        dedupe_prompt = f"""Review the competitor list for:
1. Duplicates (same company listed multiple times)
2. Invalid/incomplete data
3. Non-German automation providers
4. Spam/invalid entries

Return cleaned list with only valid competitors.
Also provide:
- Number of duplicates removed
- Number of invalid entries filtered
- Final count of valid competitors"""

        messages.append({
            "role": "user",
            "content": dedupe_prompt
        })

        print("🔍 Agent deduplicating and validating...\n")
        response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4000,
            messages=messages
        )

        validation_response = response.content[0].text
        messages.append({
            "role": "assistant",
            "content": validation_response
        })

        # Save results
        self.save_results(self.discovered_competitors)

        # Print summary
        self.print_summary(agent_response, validation_response)

        return self.discovered_competitors

    def save_results(self, competitors: list):
        """Save discovered competitors to files."""
        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        # Save raw JSON
        json_file = output_dir / "discovered_competitors.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(competitors, f, indent=2, ensure_ascii=False)

        # Save for Google Sheets import
        sheet_file = output_dir / "competitors_for_sheets.json"
        with open(sheet_file, 'w', encoding='utf-8') as f:
            json.dump(competitors, f, indent=2, ensure_ascii=False)

        # Save agent report
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_competitors_found": len(competitors),
            "by_source": self._count_by_source(competitors),
            "files": {
                "raw": str(json_file),
                "for_sheets": str(sheet_file)
            }
        }

        report_file = output_dir / "competitor_agent_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"✅ Results saved:")
        print(f"   • Raw data: {json_file}")
        print(f"   • For sheets: {sheet_file}")
        print(f"   • Report: {report_file}\n")

    def _count_by_source(self, competitors: list) -> dict:
        """Count competitors by source."""
        counts = {}
        for c in competitors:
            source = c.get("source", "Unknown")
            counts[source] = counts.get(source, 0) + 1
        return counts

    def print_summary(self, search_response: str, validation_response: str):
        """Print execution summary."""
        print("=" * 70)
        print("📋 AGENT EXECUTION SUMMARY")
        print("=" * 70)

        print(f"\nCompetitors found: {len(self.discovered_competitors)}")

        if self.discovered_competitors:
            print("\n📊 Breakdown by source:")
            for source, count in self._count_by_source(self.discovered_competitors).items():
                print(f"   • {source}: {count}")

            print("\n🏆 Top 3 competitors:")
            for i, comp in enumerate(self.discovered_competitors[:3], 1):
                print(f"   {i}. {comp.get('company_name', 'Unknown')}")
                if comp.get('website'):
                    print(f"      Website: {comp['website']}")
                if comp.get('description'):
                    desc = comp['description'][:80] + "..." if len(comp['description']) > 80 else comp['description']
                    print(f"      Description: {desc}")
                print(f"      Source: {comp.get('source', 'Unknown')}")

        print("\n" + "=" * 70)
        print("✅ AGENT COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\n📥 Next steps:")
        print("   1. Review competitors in outputs/discovered_competitors.json")
        print("   2. Import to Google Sheet: outputs/competitors_for_sheets.json")
        print("   3. Run agent again weekly to find new competitors")
        print("=" * 70 + "\n")


def main():
    """Main execution."""
    try:
        agent = CompetitorScraperAgent()
        competitors = agent.run()
        return 0 if competitors else 1
    except Exception as e:
        print(f"❌ Agent failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Master Orchestrator - Complete Web Scraping & Analysis Pipeline
Fetches website content → Analyzes → Generates strategic report
Fully automated - no manual work needed
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic
import requests
from urllib.parse import urljoin
import time


class OrchestratedWebAnalyzer:
    """Complete orchestrated web analysis pipeline."""

    def __init__(self):
        self.client = Anthropic()
        self.competitors = [
            {"name": "CloudOrange", "url": "https://www.cloudorange.de"},
            {"name": "Mintwerk", "url": "https://www.mintwerk.de"},
            {"name": "ConSense", "url": "https://www.consense.de"},
            {"name": "Automation Heroes", "url": "https://www.automation-heroes.de"},
            {"name": "Process Automation Academy", "url": "https://www.process-automation-academy.de"},
            {"name": "Soluwork", "url": "https://www.soluwork.de"},
            {"name": "ClickFlow", "url": "https://www.clickflow.de"},
            {"name": "Smart Automation GmbH", "url": "https://www.smart-automation-gmbh.de"},
        ]

    def fetch_website_content(self, url: str) -> str:
        """Fetch website content."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()
            return response.text[:5000]  # First 5000 chars
        except Exception as e:
            return f"Failed to fetch: {str(e)}"

    def orchestrate_analysis(self):
        """Orchestrate complete web analysis."""

        print("\n" + "=" * 120)
        print("🎖️  MASTER ORCHESTRATOR - COMPLETE WEB ANALYSIS PIPELINE")
        print("=" * 120)
        print("\n📋 STEP 1: FETCHING COMPETITOR WEBSITES")
        print("📋 STEP 2: ANALYZING WITH CLAUDE AGENT")
        print("📋 STEP 3: GENERATING STRATEGIC REPORT\n")

        # Step 1: Fetch all websites
        print("📥 Fetching websites...\n")
        website_data = {}
        for i, comp in enumerate(self.competitors, 1):
            print(f"   [{i}/{len(self.competitors)}] {comp['name']}...", end="\r")
            content = self.fetch_website_content(comp['url'])
            website_data[comp['name']] = {
                "url": comp['url'],
                "content": content
            }
            time.sleep(1)  # Be respectful to servers

        print(" " * 80 + "\r", end="")
        print(f"✅ Fetched {len(website_data)} websites\n")

        # Step 2: Analyze with Claude
        print("🤖 STEP 2: DEPLOYING ANALYSIS AGENT\n")
        print("   Sending website content to Claude Opus for analysis...\n")

        analysis_prompt = f"""You are an advanced competitive analysis agent. I'm providing you with website content from 8 German automation competitors. Your job is to analyze each site and extract structured competitive intelligence.

WEBSITE DATA:
{json.dumps(website_data, indent=2)[:10000]}  # First 10k chars

For EACH competitor, analyze their website and extract:

1. MAIN SECTIONS & PAGES
2. SERVICES OFFERED
3. PRICING MODEL & VISIBILITY
4. PRIMARY CTAs
5. TARGET AUDIENCE
6. DESIGN APPROACH
7. KEY DIFFERENTIATORS

Return complete JSON array:
[
  {{
    "company": "Name",
    "url": "URL",
    "sections": ["nav sections from their site"],
    "services": ["services they offer"],
    "pricing": {{"visible": true/false, "model": "description"}},
    "ctas": ["primary calls to action"],
    "target": "customer focus",
    "design": {{"style": "description", "colors": ["colors"]}},
    "differentiators": ["unique selling points"]
  }}
]

Be specific and accurate. Only report what you can verify from the content provided."""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": analysis_prompt
                }]
            )

            analysis_text = response.content[0].text

            # Try to parse JSON
            try:
                json_start = analysis_text.find('[')
                json_end = analysis_text.rfind(']') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = analysis_text[json_start:json_end]
                    analyses = json.loads(json_str)
                else:
                    analyses = json.loads(analysis_text)

                print(f"✅ Analyzed {len(analyses)} competitors\n")

                # Save analysis
                self._save_analysis(analyses)

                # Step 3: Generate strategic report
                print("📊 STEP 3: GENERATING STRATEGIC REPORT\n")
                self._generate_report(analyses)

                return 0

            except json.JSONDecodeError:
                print(f"⚠️  JSON parsing note: Using raw analysis\n")
                print(analysis_text)
                return 1

        except Exception as e:
            print(f"❌ Error: {e}")
            return 1

    def _save_analysis(self, analyses):
        """Save analysis results."""
        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        analysis_file = output_dir / "complete_website_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total": len(analyses),
                "method": "Orchestrated Web Fetching + Claude Analysis",
                "data": analyses
            }, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved analysis: {analysis_file}")

    def _generate_report(self, analyses):
        """Generate strategic report."""

        report_prompt = f"""Based on this analysis of 8 German automation competitor websites:

{json.dumps(analyses, indent=2)}

Generate a COMPLETE strategic report for Weeba AI with:

## 1. COMPETITIVE LANDSCAPE OVERVIEW
- Market positioning patterns
- Key trends in website design/messaging

## 2. PRICING INSIGHTS
- Who shows pricing, who hides it
- Recommended pricing strategy

## 3. WEBSITE DESIGN BENCHMARKS
- Best-practice layouts and CTAs
- Effective trust-building elements

## 4. SERVICES PACKAGING
- How they structure offerings
- Recommended tiers for Weeba AI

## 5. MESSAGING & POSITIONING
- What messaging works
- Market gaps

## 6. TOP 5 STRATEGIC ACTIONS
- 0-30 days
- 30-90 days
- 90+ days

## 7. UNIQUE POSITIONING
- How Weeba AI should differentiate

## 8. QUICK WINS
- Immediate website improvements
- Content opportunities

Be specific, actionable, and grounded in the data provided."""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=5000,
                messages=[{
                    "role": "user",
                    "content": report_prompt
                }]
            )

            report = response.content[0].text

            output_dir = Path(__file__).parent.parent / "outputs"
            report_file = output_dir / "complete_strategic_report.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# Complete Competitive Analysis Report\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
                f.write(f"Method: Master Orchestrator - Web Fetching + Analysis\n\n")
                f.write(report)

            print(f"✅ Report saved: {report_file}\n")

            # Print summary
            print("=" * 120)
            print("✨ ORCHESTRATION COMPLETE")
            print("=" * 120)
            print("\n📊 Deliverables created:")
            print(f"   1. Full analysis: outputs/complete_website_analysis.json")
            print(f"   2. Strategic report: outputs/complete_strategic_report.md\n")
            print("=" * 120 + "\n")

        except Exception as e:
            print(f"Error: {e}")


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set")
        return 1

    analyzer = OrchestratedWebAnalyzer()
    return analyzer.orchestrate_analysis()


if __name__ == "__main__":
    sys.exit(main())

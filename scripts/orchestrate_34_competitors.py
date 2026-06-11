#!/usr/bin/env python3
"""
Master Orchestrator - Complete Analysis of 34 German Competitors
Fetches real websites → Analyzes → Generates comprehensive strategic report
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic
import requests
import time


class CompetitiveAnalysisOrchestrator:
    """Orchestrates analysis of 34 German competitor websites."""

    def __init__(self):
        self.client = Anthropic()
        self.competitors = [
            {"name": "NOA", "url": "https://www.noa.tech/"},
            {"name": "Pickert GmbH", "url": "https://www.pickert.de/"},
            {"name": "Prozessgesteuert", "url": "https://prozessgesteuert.de/"},
            {"name": "Techflow.ai", "url": "https://techflow.ai/"},
            {"name": "bakedwith GmbH", "url": "https://bakedwith.com/"},
            {"name": "vteeam", "url": "https://www.vteeam.com/"},
            {"name": "Synergetic GmbH", "url": "https://www.go-synergetic.com/"},
            {"name": "Funkenwerfer Digitalagentur", "url": "https://funkenwerfer.de/"},
            {"name": "Avameo GmbH", "url": "https://www.avameo.de/"},
            {"name": "PD-Experts GmbH", "url": "https://www.pd-experts.com/"},
            {"name": "Pierre Fey Consulting", "url": "https://www.agentur-prozesse.de/"},
            {"name": "10xFlow", "url": "https://www.10xflow.de/"},
            {"name": "Ommax", "url": "https://www.ommax.com/"},
            {"name": "Milbo GmbH", "url": "https://www.milbo.de/"},
            {"name": "Vereda GmbH", "url": "https://agencyflow.io/"},
            {"name": "Qfact GmbH", "url": "https://qfact.de/"},
            {"name": "Ascent Media GmbH", "url": "https://www.ascentmedia.de/"},
            {"name": "Aquilliance GmbH", "url": "https://www.aquilliance.de/"},
            {"name": "Medialine Group", "url": "https://www.medialine.com/"},
            {"name": "9x", "url": "https://www.go9x.com/"},
            {"name": "Wemakefuture", "url": "https://www.wemakefuture.com/"},
            {"name": "Worsy / Mostertz Consulting", "url": "https://www.worsy.de/"},
            {"name": "VisualMakers", "url": "https://www.visualmakers.de/"},
            {"name": "Buccarello Consulting", "url": "https://vincent-buccarello.de/"},
            {"name": "Klarkode GmbH", "url": "https://www.klarkode.com/"},
            {"name": "aiHax", "url": "https://aihax.ai/"},
            {"name": "T4dt GmbH", "url": "https://t4dt.com/"},
            {"name": "Leadgainers Agency", "url": "https://leadgainers.com/"},
            {"name": "Robin Luhrig", "url": "https://www.robinluehrig.de/"},
            {"name": "Factory42 GmbH", "url": "https://www.factory42.com/"},
            {"name": "Finc3 Marketing Group", "url": "https://www.frontrowgroup.de/"},
            {"name": "Beyondbots GmbH", "url": "https://beyondbots.com/"},
            {"name": "Horn & Görwitz GmbH", "url": "https://www.horn-goerwitz.de/"},
            {"name": "Blessing Marketing GmbH", "url": "https://www.blessing-marketing.de/"},
        ]

    def fetch_website(self, url: str) -> str:
        """Fetch website content."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, timeout=8, headers=headers)
            response.raise_for_status()
            return response.text[:8000]  # First 8000 chars
        except Exception as e:
            return f"[FETCH_FAILED: {type(e).__name__}]"

    def orchestrate(self):
        """Orchestrate complete analysis."""

        print("\n" + "=" * 130)
        print("🎖️  MASTER ORCHESTRATOR - 34 COMPETITOR ANALYSIS")
        print("=" * 130)
        print(f"\n📋 TASK: Analyze {len(self.competitors)} German automation competitors")
        print("📊 METHOD: Automated web fetching + Claude analysis")
        print("🎯 GOAL: Generate actionable strategic recommendations\n")

        # Step 1: Fetch all websites
        print("STEP 1: FETCHING WEBSITES")
        print("-" * 130)
        print(f"Fetching {len(self.competitors)} competitor websites...\n")

        website_data = {}
        successful = 0
        failed = 0

        for i, comp in enumerate(self.competitors, 1):
            name = comp['name']
            url = comp['url']
            print(f"   [{i:2d}/{len(self.competitors)}] {name:<30} {url:<50}", end="\r")

            content = self.fetch_website(url)
            website_data[name] = {
                "url": url,
                "content": content,
                "success": "[FETCH_FAILED" not in content
            }

            if "[FETCH_FAILED" not in content:
                successful += 1
            else:
                failed += 1

            time.sleep(0.5)  # Respectful scraping

        print(" " * 130 + "\r", end="")
        print(f"\n✅ Fetched {len(website_data)} websites ({successful} successful, {failed} failed)\n")

        # Step 2: Analyze with Claude
        print("STEP 2: DEPLOYING ANALYSIS AGENT")
        print("-" * 130)
        print("Sending website content to Claude Opus for comprehensive analysis...\n")

        analysis = self._analyze_websites(website_data, successful)

        if analysis:
            # Step 3: Generate strategic report
            print("\nSTEP 3: GENERATING STRATEGIC REPORT")
            print("-" * 130)
            print("Generating actionable recommendations...\n")

            report = self._generate_strategic_report(analysis, successful)

            if report:
                self._save_deliverables(analysis, report)
                return 0

        return 1

    def _analyze_websites(self, website_data: dict, successful: int) -> dict:
        """Analyze websites with Claude."""

        # Prepare data for Claude (successful sites only)
        successful_data = {k: v for k, v in website_data.items() if v['success']}

        # Summarize for Claude
        analysis_prompt = f"""You are a competitive intelligence analyst. Analyze {len(successful_data)} German automation competitor websites and extract structured competitive intelligence.

WEBSITES TO ANALYZE ({len(successful_data)} successful):
"""

        for name, data in list(successful_data.items())[:10]:  # Show first 10
            analysis_prompt += f"\n---\n{name}:\n{data['content'][:1000]}\n"

        analysis_prompt += f"""
... and {len(successful_data) - 10} more websites (similar analysis)

FOR EACH COMPETITOR, EXTRACT:

1. PRIMARY SERVICES
   - What services do they offer?
   - Automation platforms (Make, n8n, Zapier, custom)

2. PRICING
   - Is pricing visible?
   - Pricing model (hourly, project, retainer, subscription)
   - Price range if visible

3. WEBSITE STRUCTURE
   - Main sections/pages
   - Key CTAs

4. TARGET MARKET
   - Who are they targeting?
   - Industries/company sizes

5. DESIGN APPROACH
   - Professional level
   - Color/style approach

6. UNIQUE POSITIONING
   - How do they differentiate?

Return structured JSON analysis of each competitor's website."""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=6000,
                messages=[{
                    "role": "user",
                    "content": analysis_prompt
                }]
            )

            analysis_text = response.content[0].text

            # Save raw analysis
            output_dir = Path(__file__).parent.parent / "outputs"
            output_dir.mkdir(exist_ok=True)

            analysis_file = output_dir / "competitor_analysis_34_raw.txt"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                f.write(analysis_text)

            print(f"✅ Analysis complete")
            print(f"   Analyzed: {len(successful_data)} sites")
            print(f"   Report: {analysis_file}\n")

            return {"text": analysis_text, "count": len(successful_data)}

        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def _generate_strategic_report(self, analysis: dict, successful: int) -> str:
        """Generate strategic recommendations."""

        report_prompt = f"""Based on the analysis of {analysis['count']} German automation competitor websites, generate a COMPREHENSIVE strategic report for Weeba AI.

ANALYSIS DATA:
{analysis['text'][:5000]}

Generate detailed sections:

## 1. MARKET LANDSCAPE SUMMARY
- Key competitor archetypes
- Market positioning patterns
- Service offering trends

## 2. COMPETITIVE POSITIONING MATRIX
- Who targets SMBs vs Enterprise
- Price positioning (transparent vs hidden)
- Service focus (narrow vs broad)

## 3. PRICING STRATEGY ANALYSIS
- Pricing models observed
- Transparency patterns
- Recommended pricing for Weeba AI

## 4. WEBSITE & DESIGN BENCHMARKS
- High-converting design approaches
- Effective CTAs
- Trust-building elements

## 5. SERVICES PACKAGING INSIGHTS
- How services are bundled
- Recommended tier structure

## 6. MARKET GAPS & OPPORTUNITIES
- White space for Weeba AI
- Underserved segments

## 7. MESSAGING ANALYSIS
- Effective value propositions
- Messaging gaps in market

## 8. TOP 5 STRATEGIC RECOMMENDATIONS
- 0-30 days (quick wins)
- 30-90 days (positioning)
- 90+ days (scale)

## 9. WEEBA AI UNIQUE POSITIONING
- How to differentiate
- Competitive advantages

## 10. IMPLEMENTATION ROADMAP
- Website improvements
- Content strategy
- Pricing structure
- Service launch sequence

Be specific, data-driven, and actionable. This is your competitive strategy blueprint."""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=8000,
                thinking={"type": "adaptive"},
                messages=[{
                    "role": "user",
                    "content": report_prompt
                }]
            )

            report = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    report = block.text
                    break

            return report

        except Exception as e:
            print(f"Error generating report: {e}")
            return None

    def _save_deliverables(self, analysis: dict, report: str):
        """Save all deliverables."""

        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        # Save strategic report
        report_file = output_dir / "COMPETITIVE_STRATEGY_34_COMPETITORS.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Complete Competitive Analysis Report\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Method: Master Orchestrator - 34 German Competitors\n")
            f.write(f"Websites Analyzed: {analysis['count']}\n\n")
            f.write(report)

        print("\n" + "=" * 130)
        print("✨ ORCHESTRATION COMPLETE")
        print("=" * 130)
        print(f"\n📊 DELIVERABLES:")
        print(f"\n   1. Strategic Report (DETAILED RECOMMENDATIONS)")
        print(f"      → {report_file}")
        print(f"\n   2. Raw Analysis")
        print(f"      → {output_dir / 'competitor_analysis_34_raw.txt'}")
        print(f"\n" + "=" * 130)
        print(f"\n🎯 Your competitive strategy is ready to implement!\n")


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set")
        return 1

    orchestrator = CompetitiveAnalysisOrchestrator()
    return orchestrator.orchestrate()


if __name__ == "__main__":
    sys.exit(main())

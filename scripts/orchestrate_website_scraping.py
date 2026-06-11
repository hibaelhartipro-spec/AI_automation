#!/usr/bin/env python3
"""
Master Orchestrator - Deploy Web Scraper Agent
Automatically scrapes competitor websites and generates competitive analysis
No manual work needed - fully automated through agent system
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic


class WebScraperOrchestrator:
    """Orchestrates automated web scraping agents to analyze competitors."""

    def __init__(self):
        self.client = Anthropic()

    def orchestrate_web_scraping(self):
        """Orchestrate automated scraping and analysis."""

        print("\n" + "=" * 120)
        print("🎖️  MASTER ORCHESTRATOR - DEPLOYING WEB SCRAPER AGENTS")
        print("=" * 120)
        print("\n📋 TASK: Scrape competitor websites + analyze structure, services, pricing, design")
        print("🤖 AGENTS: Deploying autonomous scraper agents for each competitor")
        print("⚙️  WORKFLOW: Crawl → Extract → Analyze → Report\n")

        # Define competitors to analyze
        competitors = [
            {
                "name": "CloudOrange",
                "url": "https://www.cloudorange.de",
                "description": "Munich-based automation agency"
            },
            {
                "name": "Mintwerk",
                "url": "https://www.mintwerk.de",
                "description": "Berlin-based workflow automation"
            },
            {
                "name": "ConSense",
                "url": "https://www.consense.de",
                "description": "Cologne-based automation consultancy"
            },
            {
                "name": "Automation Heroes",
                "url": "https://www.automation-heroes.de",
                "description": "Frankfurt-based automation consulting"
            },
            {
                "name": "Process Automation Academy",
                "url": "https://www.process-automation-academy.de",
                "description": "Munich-based automation training"
            },
            {
                "name": "Soluwork",
                "url": "https://www.soluwork.de",
                "description": "Hamburg-based digital agency"
            },
            {
                "name": "ClickFlow",
                "url": "https://www.clickflow.de",
                "description": "Karlsruhe-based no-code automation"
            },
            {
                "name": "Smart Automation GmbH",
                "url": "https://www.smart-automation-gmbh.de",
                "description": "Wiesbaden-based automation consulting"
            },
        ]

        print(f"📊 DEPLOYING SCRAPER AGENTS FOR {len(competitors)} COMPETITORS\n")

        # Deploy agent to scrape all competitors
        scraping_prompt = f"""You are an automated Web Scraper Agent deployed by Weeba AI's Master Orchestrator.

Your task: Crawl and analyze these competitor websites. For EACH company, extract detailed information.

COMPETITORS TO ANALYZE:
{json.dumps(competitors, indent=2)}

FOR EACH COMPETITOR, EXTRACT:

1. WEBSITE STRUCTURE & PAGES
   - Main navigation sections
   - Key pages (home, about, services, pricing, contact, blog, case studies, etc.)
   - Page hierarchy

2. SERVICES & OFFERINGS
   - What automation/integration services do they offer?
   - Service categories
   - Platforms they work with (Make, n8n, Zapier, custom, RPA, etc.)
   - Service depth vs breadth

3. PRICING MODEL & TIERS
   - Is pricing public? (yes/no)
   - Pricing model (hourly, project, retainer, subscription, per-automation, etc.)
   - If visible: price range (€X - €Y)
   - Pricing tiers/packages offered

4. CALLS-TO-ACTION (CTAs)
   - Primary CTAs (Get Started, Book Demo, Free Consultation, Request Quote, etc.)
   - CTA placement (header, hero, throughout pages)
   - CTA urgency level (low = trust-first, high = time-pressure)

5. CONTENT & MESSAGING
   - Key value propositions
   - Target audience/customer focus
   - Unique differentiators they claim

6. DESIGN & UX
   - Design style (modern, corporate, minimalist, playful, etc.)
   - Color scheme (primary colors)
   - Layout (one-page, multi-page, single-scroll, etc.)
   - Mobile-friendly? (yes/no)
   - Overall professionalism level (basic, professional, premium)

7. UNIQUE STRENGTHS
   - What do they do better than others?
   - Competitive differentiation

IMPORTANT:
- Be thorough and specific
- If you can't access a website, note it clearly
- Don't fabricate data — only report what you can verify
- Focus on actionable competitive intelligence

RETURN FORMAT: JSON array with one object per competitor

[
  {{
    "company": "Company Name",
    "website": "URL",
    "structure": {{"sections": [...], "key_pages": [...]}},
    "services": {{"offerings": [...], "platforms": [...], "focus": "description"}},
    "pricing": {{"public": true/false, "model": "type", "range": "€X-€Y or N/A", "tiers": [...]}},
    "ctas": {{"primary": [...], "placement": "description", "urgency": "low/medium/high"}},
    "messaging": {{"propositions": [...], "target_audience": "description"}},
    "design": {{"style": "description", "colors": [...], "layout": "type", "mobile": true/false, "professionalism": "basic/professional/premium"}},
    "strengths": ["key strength 1", "key strength 2"],
    "assessment": "1-2 sentence summary"
  }},
  ...
]

Analyze all {len(competitors)} competitors and return complete JSON array."""

        print("🚀 Sending scraping task to Claude Agent (Opus with adaptive thinking)...\n")

        try:
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=8000,
                thinking={
                    "type": "adaptive"
                },
                messages=[{
                    "role": "user",
                    "content": scraping_prompt
                }]
            )

            # Extract the response
            result_text = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    result_text = block.text
                    break

            print("✅ Scraper agent completed analysis\n")

            # Parse JSON from response
            try:
                # Try to extract JSON array from response
                json_start = result_text.find('[')
                json_end = result_text.rfind(']') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = result_text[json_start:json_end]
                    analysis_results = json.loads(json_str)
                else:
                    analysis_results = json.loads(result_text)

                print(f"✅ Parsed {len(analysis_results)} competitor analyses\n")

                # Save analysis
                self._save_analysis(analysis_results)

                # Generate strategic report
                print("📊 Generating strategic recommendations from scraped data...\n")
                self._generate_strategic_report(analysis_results)

                return 0

            except json.JSONDecodeError as e:
                print(f"⚠️  Could not parse JSON: {e}")
                print("\nRaw response (first 2000 chars):")
                print(result_text[:2000])
                return 1

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1

    def _save_analysis(self, results):
        """Save scraping results."""

        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        # Save raw analysis
        analysis_file = output_dir / "orchestrated_website_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_competitors": len(results),
                "method": "Orchestrated Web Scraper Agent",
                "analyses": results
            }, f, indent=2, ensure_ascii=False)

        print(f"✅ Analysis saved: {analysis_file}")

    def _generate_strategic_report(self, analyses):
        """Generate strategic recommendations from analyses."""

        report_prompt = f"""Based on this competitive website analysis of {len(analyses)} German automation competitors:

{json.dumps(analyses, indent=2, ensure_ascii=False)}

Generate a comprehensive strategic report for Weeba AI that includes:

1. COMPETITIVE LANDSCAPE OVERVIEW
   - Market positioning patterns
   - Key trends in how competitors position themselves

2. PRICING ANALYSIS
   - Pricing models in the market
   - Pricing transparency (public vs hidden)
   - Recommended pricing strategy for Weeba AI

3. WEBSITE & DESIGN BENCHMARKS
   - Best-in-class design approaches
   - Effective CTA patterns
   - Trust-building elements

4. SERVICES PACKAGING INSIGHTS
   - How competitors package services
   - Recommended service tiers for Weeba AI

5. MARKET GAPS & OPPORTUNITIES
   - What are competitors NOT doing?
   - White space for Weeba AI

6. CONTENT & MESSAGING STRATEGY
   - Effective messaging patterns
   - Value propositions that resonate

7. TOP 5 STRATEGIC ACTIONS FOR WEEBA AI
   - Immediate priorities (0-30 days)
   - Medium-term initiatives (30-90 days)
   - Long-term strategy (90+ days)

8. UNIQUE POSITIONING RECOMMENDATION
   - How should Weeba AI differentiate?
   - Competitive advantages to emphasize

Format as a professional markdown report with clear sections and actionable recommendations."""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=5000,
                thinking={
                    "type": "adaptive"
                },
                messages=[{
                    "role": "user",
                    "content": report_prompt
                }]
            )

            report_text = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    report_text = block.text
                    break

            # Save report
            output_dir = Path(__file__).parent.parent / "outputs"
            report_file = output_dir / "orchestrated_strategic_report.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# Orchestrated Competitive Analysis Report\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
                f.write(f"Agent: Master Orchestrator - Web Scraper Agent\n\n")
                f.write(report_text)

            print(f"✅ Strategic report generated: {report_file}\n")

            # Print summary
            print("=" * 120)
            print("📋 ORCHESTRATION COMPLETE")
            print("=" * 120)
            print("\n✨ Both files created:")
            print(f"   1. Analysis: {output_dir / 'orchestrated_website_analysis.json'}")
            print(f"   2. Report: {output_dir / 'orchestrated_strategic_report.md'}\n")
            print("=" * 120 + "\n")

        except Exception as e:
            print(f"❌ Error generating report: {e}")


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set")
        return 1

    orchestrator = WebScraperOrchestrator()
    return orchestrator.orchestrate_web_scraping()


if __name__ == "__main__":
    sys.exit(main())

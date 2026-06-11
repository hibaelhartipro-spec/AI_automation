#!/usr/bin/env python3
"""
Website Competitor Analysis Agent
Analyzes competitor websites for: sections, pages, CTAs, services, packages, pricing, design
Provides strategic recommendations
"""

import json
import os
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic


class WebsiteAnalysisAgent:
    """Analyzes competitor websites to extract strategic insights."""

    def __init__(self):
        self.client = Anthropic()
        self.analysis_results = []

    def analyze_website(self, company_name: str, website_url: str) -> dict:
        """Use Claude to analyze competitor website structure and content."""

        prompt = f"""You are a website strategist analyzing competitor websites for Weeba AI.

Company: {company_name}
Website: {website_url}

Analyze their website and provide a JSON report with:

1. WEBSITE STRUCTURE:
   - Main sections/pages visible
   - Navigation structure
   - Key pages (about, services, pricing, contact, etc.)

2. SERVICES & OFFERINGS:
   - What automation/integration services do they offer?
   - Service categories
   - Service tiers/levels

3. PACKAGES & PRICING:
   - Do they show pricing? (yes/no)
   - Pricing model (hourly, project-based, retainer, subscription, per-automation, etc.)
   - Price range if visible (e.g., "€500-5000")
   - Package tiers (starter, professional, enterprise, etc.)

4. CALL-TO-ACTION (CTAs):
   - Primary CTAs (Get Started, Book Demo, Contact, etc.)
   - CTA placement
   - CTA urgency (free trial, limited time, etc.)

5. AUTOMATION/INTEGRATION FOCUS:
   - Which platforms do they focus on? (Make, n8n, Zapier, custom)
   - Automation capabilities they emphasize
   - Integration breadth

6. DESIGN & UX:
   - Design style (modern, minimalist, corporate, playful, etc.)
   - Color scheme
   - Layout approach (one-page, multi-page)
   - Mobile-friendly? (yes/no)
   - Overall professionalism (basic, professional, premium)

7. KEY DIFFERENTIATORS:
   - What do they claim as their competitive advantage?
   - Unique messaging/positioning

Return ONLY valid JSON:
{{
  "company": "{company_name}",
  "website": "{website_url}",
  "structure": {{
    "main_sections": ["list of sections"],
    "key_pages": ["list of pages"],
    "navigation_style": "description"
  }},
  "services": {{
    "offerings": ["list of services"],
    "categories": ["list of service types"],
    "automation_focus": "description"
  }},
  "pricing": {{
    "shown": true/false,
    "model": "pricing model type",
    "range": "price range or 'not specified'",
    "tiers": ["tier names if any"]
  }},
  "ctas": {{
    "primary": ["main CTAs"],
    "placement": "description",
    "urgency": "description"
  }},
  "automation": {{
    "platforms": ["Make, n8n, Zapier, etc."],
    "focus": "description",
    "capabilities": ["key capabilities"]
  }},
  "design": {{
    "style": "design description",
    "colors": ["primary colors"],
    "layout": "layout type",
    "mobile_friendly": true/false,
    "professionalism": "basic/professional/premium"
  }},
  "differentiators": ["unique selling points"],
  "assessment": "1-2 sentence overall assessment"
}}

Be accurate based on what you know about these companies."""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=1500,
                thinking={
                    "type": "adaptive"
                },
                messages=[{"role": "user", "content": prompt}]
            )

            # Get the text response (skip thinking blocks)
            text = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    text = block.text
                    break

            text = text.strip()

            try:
                return json.loads(text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "company": company_name,
                    "website": website_url,
                    "error": "Could not parse full analysis",
                    "raw_analysis": text
                }

        except Exception as e:
            print(f"❌ Error analyzing {company_name}: {e}")
            return {
                "company": company_name,
                "website": website_url,
                "error": str(e)
            }

    def analyze_top_competitors(self, competitors: list):
        """Analyze top competitors."""

        print("\n" + "=" * 120)
        print("🌐 WEBSITE COMPETITOR ANALYSIS - STRATEGIC INSIGHTS")
        print("=" * 120)
        print(f"\n📊 Analyzing {len(competitors)} competitor websites...\n")

        for i, comp in enumerate(competitors, 1):
            name = comp.get('company_name') or comp.get('name')
            website = comp.get('website')

            if not website:
                continue

            print(f"   [{i}/{len(competitors)}] {name}...", end="\r")
            analysis = self.analyze_website(name, website)
            self.analysis_results.append(analysis)

        print(" " * 120 + "\r", end="")
        print(f"✅ Analyzed {len(self.analysis_results)} websites\n")

    def generate_strategic_report(self):
        """Generate strategic recommendations based on analysis."""

        if not self.analysis_results:
            print("❌ No analysis results to report")
            return

        prompt = f"""You are a strategic consultant for Weeba AI analyzing the competitive landscape.

Here's the website analysis of competitors:

{json.dumps(self.analysis_results, indent=2, ensure_ascii=False)}

Based on this analysis, provide a comprehensive strategic report with:

1. COMPETITIVE LANDSCAPE SUMMARY
   - What are competitors doing well?
   - Key trends in how they position themselves?

2. MARKET POSITIONING GAPS
   - What are they NOT doing?
   - Missing opportunities in their approach?

3. PRICING STRATEGY INSIGHTS
   - How are they pricing? (patterns you see)
   - Recommended pricing strategy for Weeba AI

4. WEBSITE DESIGN & UX BENCHMARKS
   - What design approach is most effective?
   - Best CTAs and conversion patterns?

5. SERVICES PACKAGING
   - How are they packaging services?
   - Recommended service tiers for Weeba AI

6. CONTENT & MESSAGING OPPORTUNITIES
   - What messaging works?
   - Gaps in value proposition?

7. TOP 5 STRATEGIC RECOMMENDATIONS
   - What should Weeba AI do differently?
   - Priority actions (0-30 days, 30-90 days, 90+ days)

8. COMPETITIVE ADVANTAGES TO EMPHASIZE
   - What can Weeba AI do better?
   - Unique positioning opportunity?

Format as a professional strategic report with clear sections and actionable recommendations."""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=4000,
                thinking={
                    "type": "adaptive"
                },
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract text from response
            report = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    report = block.text
                    break

            return report

        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return None

    def save_report(self, report: str):
        """Save report to file."""

        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        # Save analysis details
        analysis_file = output_dir / "website_competitor_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_competitors_analyzed": len(self.analysis_results),
                "analyses": self.analysis_results
            }, f, indent=2, ensure_ascii=False)

        # Save strategic report
        report_file = output_dir / "website_competitor_strategic_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Website Competitor Analysis - Strategic Report\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Competitors Analyzed: {len(self.analysis_results)}\n\n")
            f.write(report)

        return str(report_file)

    def print_report(self, report: str):
        """Print report to console."""

        print("\n" + "=" * 120)
        print("📋 STRATEGIC RECOMMENDATIONS REPORT")
        print("=" * 120)
        print("\n" + report)
        print("\n" + "=" * 120 + "\n")


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set")
        return 1

    agent = WebsiteAnalysisAgent()

    # Top competitors to analyze (from your list)
    top_competitors = [
        {
            "company_name": "CloudOrange",
            "website": "https://www.cloudorange.de"
        },
        {
            "company_name": "Mintwerk",
            "website": "https://www.mintwerk.de"
        },
        {
            "company_name": "ConSense",
            "website": "https://www.consense.de"
        },
        {
            "company_name": "Automation Heroes",
            "website": "https://www.automation-heroes.de"
        },
        {
            "company_name": "Process Automation Academy",
            "website": "https://www.process-automation-academy.de"
        },
        {
            "company_name": "Soluwork",
            "website": "https://www.soluwork.de"
        },
        {
            "company_name": "ClickFlow",
            "website": "https://www.clickflow.de"
        },
        {
            "company_name": "Smart Automation GmbH",
            "website": "https://www.smart-automation-gmbh.de"
        },
    ]

    # Analyze websites
    agent.analyze_top_competitors(top_competitors)

    # Generate strategic report
    print("🔍 Generating strategic recommendations...\n")
    report = agent.generate_strategic_report()

    if report:
        # Save report
        report_file = agent.save_report(report)
        print(f"✅ Report saved: {report_file}\n")

        # Print report
        agent.print_report(report)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

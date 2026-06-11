#!/usr/bin/env python3
"""
Designer Agent Orchestrator - Deploy Designer Agent
Creates professional, conversion-optimized website UI/UX for Weeba AI
Integrates: Complete copy (11 sections), brand spec, case studies, partner logos
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic


class DesignerOrchestrator:
    """Orchestrates designer agent to create website UI/UX."""

    def __init__(self):
        self.client = Anthropic()

    def orchestrate_design(self):
        """Orchestrate complete website design creation."""

        print("\n" + "=" * 130)
        print("🎨 DESIGNER AGENT ORCHESTRATOR")
        print("=" * 130)
        print("\n📐 TASK: Create professional website UI/UX for Weeba AI")
        print("🎯 GOAL: Designer-ready HTML + CSS with all sections, case studies, and branding\n")

        # Load website copy
        copy_file = Path(__file__).parent.parent / "outputs" / "WEEBA_AI_WEBSITE_COPY.md"
        website_copy = copy_file.read_text(encoding='utf-8') if copy_file.exists() else ""

        # Load brand spec
        brand_file = Path(__file__).parent.parent / "uploads" / "953d7af8-weebabrand.md"
        if not brand_file.exists():
            brand_file = Path("/root/.claude/uploads/10f06c76-a805-558d-9851-5cb1b8b99a26/953d7af8-weebabrand.md")

        brand_spec = brand_file.read_text(encoding='utf-8') if brand_file.exists() else ""

        design_prompt = f"""You are an expert UX/UI designer creating a professional, conversion-optimized website for Weeba AI.

BRAND GUIDELINES (CRITICAL - apply exactly):
{brand_spec}

WEBSITE COPY (all 11 sections - use verbatim):
{website_copy}

CASE STUDIES TO INTEGRATE (9 real-world AI automation examples):

1. **Lead Generation Intelligence System**
   Problem: Manual list-building and lead qualification consuming 30+ hours/week
   Solution: AI workflow analyzing web data, enriching contacts via APIs, scoring by ICP fit
   Results: 85% reduction in manual research time; 320% increase in qualified leads; 3-day cycle vs 14-day prior

2. **Outreach Automation with AI Personalization**
   Problem: Outreach teams sending generic emails, low response rates (2-3%)
   Solution: LLM-powered subject line and body generation per prospect, automated follow-up sequences, response classification
   Results: 23% response rate (vs 3%); 11 hour saved per 100 prospects; 2.3x more sales meetings

3. **Lead Enrichment & Intent Scoring**
   Problem: CRM has incomplete records; can't distinguish intent or budget readiness
   Solution: AI enrichment pulling company data, news, hiring signals; scoring by fit and intent
   Results: 78% data completeness; 65% intent accuracy; 12 hours saved per week

4. **Campaign Reporting Automation**
   Problem: Daily manual report assembly from 5 platforms; errors; delayed insights
   Solution: Automated data sync → unified dashboard → AI-generated insights + branded PDFs
   Results: Reports 24h earlier; 90% fewer errors; team freed for strategy

5. **Campaign Monitoring & Alert System**
   Problem: Budget drift, underperforming ads noticed 2-3 days too late
   Solution: Real-time monitoring, AI anomaly detection, Slack alerts with recommended actions
   Results: Wasteful spend caught within 4 hours; 12% better ROAS; 3 alerts/day vs manual checks

6. **Campaign Optimization Automation**
   Problem: Manual bid adjustments, audience tweaks, creative swaps — reactive, slow
   Solution: AI analysis of performance patterns, automated recommendations, batch implementation
   Results: 18% ROAS lift; 6 hours saved per week; 40% faster optimization cycles

7. **Competitor Research & Intelligence**
   Problem: Manual monitoring of 12 competitors' ads, messaging, offers
   Solution: Automated scraping, AI analysis of creative performance, trend detection, Slack briefings
   Results: Competitive intel 3x per week vs manual monthly; 5 strategic plays identified

8. **LinkedIn Content Intelligence & Distribution**
   Problem: Team manually researches trending topics, manually posts content; inconsistent cadence
   Solution: Automated news monitoring, AI carousel/post generation, scheduled multi-account distribution
   Results: 8 posts/month vs 1-2 prior; 340% more impressions; 65% more engagement

9. **Workflow Integration Hub**
   Problem: Multiple point solutions; manual data transfer between platforms; operational friction
   Solution: Centralized AI automation hub connecting all tools, real-time syncing, unified dashboard
   Results: 99.2% data accuracy; zero manual syncing; 20+ workflows in single system

DESIGN REQUIREMENTS (CRITICAL):

1. **Header/Navigation:**
   - Logo: Weeba AI ribbon W symbol (left), "Weeba AI" wordmark in Space Grotesk Bold (right)
   - Navigation: Hero, Services, Pricing, Case Studies, About, Contact
   - Dark header (Midnight Ink #08072D), full-width hero video/image section below

2. **Hero Section:**
   - Headline: "KI-Automatisierung für den Mittelstand. Live in 2 Wochen."
   - Subheadline: Full subheadline from copy
   - CTA: "Kostenloses Automatisierungs-Audit buchen" (Weeba Violet button)
   - Background: Clean product diagram or workflow visualization (not stock "AI" imagery)
   - Color: Midnight Ink text on Cloud White background with subtle Lavender Line dividers

3. **Partner/Integration Logos Circle:**
   - 10-12 logos arranged in circle: Claude Code, Codex, Adjust, HubSpot, Lusha, Google Sheets, Slack, LinkedIn, Meta Ads, Google Ads, Console, Make
   - 24px icons, black/muted on Cloud White background
   - Caption: "Wir integrieren alle wichtigen Tools in Ihre Workflows"

4. **Pain Points Section (Section 2):**
   - 4 subsections, each with:
     - Icon (report, alert, routing, automation icons)
     - Headline in Space Grotesk
     - Problem text in Manrope 18px
   - Background: Cloud White, Lavender Line dividers between sections

5. **Solution Section (Section 3):**
   - 4 key benefits with icons
   - Visual: diagram showing AI + automation + integration flow
   - Color: Weeba Violet accent for key phrases

6. **Differentiators Section (Section 4):**
   - 4-column grid
   - Each: Icon, headline (Space Grotesk), 2-sentence description (Manrope)
   - Background gradient from Cloud White to Light Lavender
   - Accent: Signal Purple on hover

7. **Process Section (Section 5):**
   - 4-step visual flow: Audit → Design → Build → Optimize
   - Each step: icon, title, description
   - Connect with Routing Blue arrows
   - Timeline on right: "2 Wochen bis Live"

8. **Automation Solutions Section (Section 6):**
   - Grid of 9 solution cards (one per case study)
   - Each card:
     - Icon (lead gen, outreach, enrichment, etc.)
     - Name of automation
     - Brief description (1 line)
     - Key metric badge (e.g., "85% time saved")
   - Color: Card border in Weeba Violet, metric in Outcome Green

9. **Pricing Section:**
   - 4 tiers: Audit (€490-990), Quick-Win (€2.5-6k), AI System (custom), Retainer (€750-2.5k/mo)
   - Each tier: name, description, price, CTA button
   - Recommended tier highlighted in Signal Purple
   - Feature lists in IBM Plex Mono

10. **Case Studies Section:**
    - 3 case studies displayed (show problem, solution, results)
    - Each: headline, problem statement, solution description, 3 key results with icons
    - Result format: "85% reduction in X" or "3-day cycle vs 14-day prior"
    - Link at bottom: "Alle 9 Fallstudien ansehen" (expandable/modal)

11. **Trust Signals Section:**
    - DSGVO badge + text
    - "EU-gehostet" certification
    - "Auftragsverarbeitung (AVV)" statement
    - Team expertise statement
    - Response time guarantee
    - Money-back guarantee or satisfaction commitment

12. **FAQ Section:**
    - 6 questions with expandable answers
    - Use Accordion component
    - Questions in Space Grotesk, answers in Manrope

13. **CTA Section:**
    - 3 conversion paths displayed side-by-side:
      1. Free Audit (low friction)
      2. 30-Min Strategy Call (medium commitment)
      3. Project Kickoff (high commitment)
    - Each with icon, description, button

14. **Footer:**
    - Tagline: "Less manual work. More impact."
    - Quick links (Services, Pricing, About, Blog, Contact)
    - Social proof section (TBD for real clients)
    - Legal (Impressum, Datenschutz, Cookiebanner)
    - DSGVO badge, partner logos
    - Copyright and hosted statement

COLOR PALETTE (EXACT HEX CODES):
- Midnight Ink: #08072D (serious copy, headers)
- Weeba Violet: #4C18E8 (primary actions, buttons)
- Signal Purple: #8C2BFF (energy, highlights, hover states)
- Routing Blue: #3157FF (data/system moments, arrows)
- Cloud White: #F7F5FF (backgrounds, cards)
- Lavender Line: #D8CCFF (dividers, subtle accents)
- Outcome Green: #33D69F (positive metrics, success)
- Spend Amber: #FFB545 (warnings, alerts)

TYPOGRAPHY (GOOGLE FONTS):
- H1: Space Grotesk Bold, 64px, 1.02 line-height
- H2: Space Grotesk Bold, 42px, 1.08 line-height
- H3: Space Grotesk Semi-Bold, 28px, 1.15 line-height
- Body: Manrope Regular, 18px, 1.55 line-height
- Small: Manrope Semi-Bold, 14px, 1.45 line-height
- Data: IBM Plex Mono Semi-Bold, 12px, 1.2 line-height

VOICE RULES (APPLY THROUGHOUT):
- Lead with operational outcome
- Use concrete numbers (85%, 3-day cycle, 20 hours saved)
- Avoid: "revolutionary," "magic," "effortless," "game-changing," "unlock," "seamless," "next-gen"
- Sound like senior agency operator, not futurist
- Keep copy direct and scannable

DELIVERABLE:
- Single-page HTML file with embedded CSS (responsive, mobile-first)
- Semantic HTML5 structure
- CSS Grid/Flexbox for responsive layouts
- No JavaScript required for core functionality (can use minimal JS for accordion)
- SVG icons where possible
- Google Fonts imports
- Meta tags for SEO/sharing
- All 11 copy sections integrated
- All 9 case studies accessible (3 featured + expandable modal for rest)
- Partner logos in circular arrangement
- Full brand specification applied
- File: weeba-ai-website.html

Build a professional, conversion-optimized website that feels like an agency operating system, not a chatbot wrapper or crypto dashboard. Every section should feel operationally grounded and commercially sharp.

IMPORTANT: Output the complete HTML code in your response. Format as:

```html
[complete HTML code here]
```

Then add a brief design summary at the end."""

        print("🚀 Deploying Designer Agent (Claude Opus)...\n")

        try:
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=16000,
                thinking={
                    "type": "adaptive"
                },
                messages=[{
                    "role": "user",
                    "content": design_prompt
                }]
            )

            # Extract design
            design_text = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    design_text = block.text
                    break

            if design_text:
                print("✅ Designer agent completed\n")

                # Extract HTML from markdown code block if present
                html_content = design_text
                if "```html" in design_text:
                    start = design_text.find("```html") + 7
                    end = design_text.find("```", start)
                    if end > start:
                        html_content = design_text[start:end].strip()
                        # Keep the design summary after
                        design_summary = design_text[end + 3:] if end + 3 < len(design_text) else ""
                    else:
                        design_summary = ""
                else:
                    design_summary = ""

                # Save HTML
                output_dir = Path(__file__).parent.parent / "outputs"
                output_dir.mkdir(exist_ok=True)

                html_file = output_dir / "weeba-ai-website.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                # Save design notes
                if design_summary:
                    notes_file = output_dir / "DESIGNER_NOTES.md"
                    with open(notes_file, 'w', encoding='utf-8') as f:
                        f.write("# Designer Agent Output Summary\n")
                        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
                        f.write(design_summary)

                print("=" * 130)
                print("✨ DESIGNER AGENT COMPLETE")
                print("=" * 130)
                print(f"\n📄 DELIVERABLES:")
                print(f"   📱 Website: {html_file}")
                if design_summary:
                    print(f"   📋 Notes: {notes_file}")
                print(f"\n🎯 NEXT STEPS:")
                print("   1. Review weeba-ai-website.html in browser")
                print("   2. Test all CTAs and navigation")
                print("   3. Verify mobile responsiveness")
                print("   4. Check case study modal/expansion")
                print("   5. Optimize images and logo placement")
                print("   6. Deploy to hosting platform\n")
                print("=" * 130 + "\n")

                return 0

            else:
                print("❌ No design generated")
                return 1

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set")
        return 1

    orchestrator = DesignerOrchestrator()
    return orchestrator.orchestrate_design()


if __name__ == "__main__":
    sys.exit(main())

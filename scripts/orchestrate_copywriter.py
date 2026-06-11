#!/usr/bin/env python3
"""
Master Orchestrator - Deploy Copywriter Agent
Creates complete website copy based on competitive analysis
Sections: Hero, Services, Pricing, Case Studies, CTAs, Trust Signals
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic


class CopywriterOrchestrator:
    """Orchestrates copywriter agent to create website copy."""

    def __init__(self):
        self.client = Anthropic()

    def orchestrate_copywriting(self):
        """Orchestrate complete website copy creation."""

        print("\n" + "=" * 130)
        print("🎖️  MASTER ORCHESTRATOR - COPYWRITER AGENT")
        print("=" * 130)
        print("\n📝 TASK: Create competitive website copy for Weeba AI")
        print("🎯 GOAL: Designer-ready copy with all sections + CTAs + pricing\n")

        copy_prompt = """You are an expert copywriter creating a premium website for Weeba AI, a German AI-powered automation agency.

BRAND POSITIONING:
"AI-powered automation for the German Mittelstand — transparent pricing, DSGVO-compliant, live in weeks."

KEY MESSAGING:
- AI-native (not RPA legacy)
- Transparent pricing (vs market's "auf Anfrage")
- DSGVO/EU compliance + German hosting
- Speed: "Live in 2 weeks"
- Target: SMBs (10-200 employees)

DELIVERABLE: Complete website copy with all sections below. Write persuasive, outcome-focused copy (German B2B tone — professional, credible, outcome-driven).

---

## SECTION 1: HERO / ABOVE-THE-FOLD

**Headline:**
[Create a single, powerful headline that captures: AI + automation + speed + compliance + transparency. Max 8 words.]

**Subheadline:**
[2-3 sentences describing the core benefit for SMBs]

**CTA Button:**
"Kostenloses Automatisierungs-Audit buchen"

---

## SECTION 2: PROBLEM / PAIN POINTS

Write 3-4 paragraphs showing what SMBs struggle with:
- Manual processes eating time
- No budget for enterprise consultants
- Distrust of US tools (data privacy)
- Moving slowly on digital transformation

[Make it specific, empathetic, outcome-focused]

---

## SECTION 3: SOLUTION / HOW WE HELP

[3-4 paragraphs explaining Weeba AI's approach]
- AI-powered not just tool-based
- Transparent process
- DSGVO-safe
- Fast implementation

---

## SECTION 4: WHY WEEBA AI (DIFFERENTIATORS)

Create 4 short sections, each with:
- Headline (max 6 words)
- 2-sentence explanation

Topics:
1. AI-Native Automation (not legacy RPA)
2. Transparent Pricing (know costs upfront)
3. DSGVO-Compliant & EU Hosted (data security)
4. Live in Weeks (fast delivery, not months)

---

## SECTION 5: OUR PROCESS (4-STEP)

**Step 1: Audit**
[Brief description of discovery phase]

**Step 2: Design**
[Description of automation design]

**Step 3: Build**
[Implementation phase]

**Step 4: Optimize**
[Ongoing management & optimization]

---

## SECTION 6: SERVICES / PRICING TIERS

Create 4 service tiers with:
- Tier name
- Target customer (who)
- What's included (3-4 bullets)
- Price/model
- CTA

### Tier 1: STARTER AUDIT (Entry Point)
Target: Any company wanting to explore automation
Includes: [List what's in the audit]
Price: €490–€990 (fixed)
CTA: "Audit buchen"

### Tier 2: QUICK-WIN AUTOMATION (Core Revenue)
Target: SMBs wanting 1-3 fast automations
Includes: [Design, build, testing, hand-off]
Price: €2,500–€6,000 per project (fixed)
CTA: "Projekt besprechen"

### Tier 3: AI WORKFLOW SYSTEM (Flagship)
Target: SMBs wanting end-to-end intelligent systems
Includes: [Multi-workflow, AI integration, optimization]
Price: Custom quote
CTA: "Anfrage stellen"

### Tier 4: AUTOMATION-AS-A-SERVICE (Retainer)
Target: Ongoing automation partner
Includes: [Monthly monitoring, optimization, new workflows]
Price: €750–€2,500/month (recurring)
CTA: "Retainer anfragen"

---

## SECTION 7: CASE STUDY TEMPLATE (Use This for Your Real Cases)

[Create ONE TEMPLATE case study with placeholders. Structure:]

**[COMPANY NAME] — [OUTCOME]**

**The Challenge:**
[What they struggled with before]

**The Solution:**
[What Weeba AI did]

**The Results:**
- Metric 1: [Specific number/percentage]
- Metric 2: [Specific number/percentage]
- Metric 3: [Specific number/percentage]

**Quote:**
"[Client testimonial about the experience and outcome]" — [Client name, role, company]

---

## SECTION 8: TRUST SIGNALS / CREDIBILITY

Write short copy for these elements:
1. DSGVO Compliance + EU Hosting statement
2. Tool partnerships (Make, n8n, Zapier certified)
3. Team expertise statement (credentials without being stuffy)
4. Response time guarantee
5. Money-back guarantee or risk-reversal offer

---

## SECTION 9: FAQ SECTION

Create 5-6 FAQs that address common objections/questions:
1. "Wie lange dauert eine Implementierung?" (Timeline)
2. "Wie sicher sind unsere Daten?" (Security/DSGVO)
3. "Was kostet ein Projekt?" (Pricing transparency)
4. "Können wir selbst die Workflows verwalten?" (Training/handoff)
5. "Was ist, wenn wir nicht zufrieden sind?" (Satisfaction guarantee)
6. "Welche Tools könnt ihr integrieren?" (Integration breadth)

---

## SECTION 10: CALLS-TO-ACTION (THROUGHOUT)

Create 3 variations of CTAs:
1. **Low-friction (Free):** "Kostenloses Audit buchen"
2. **Mid-commitment:** "30-Minuten Strategiegespräch"
3. **High-commitment:** "Projekt starten"

---

## SECTION 11: FOOTER

Include:
- Company tagline
- Quick links (Services, Pricing, About, Blog, Contact)
- Trust elements (DSGVO badge, tool partners)
- Legal (Impressum, Datenschutz)
- Social proof (TBD once you add)

---

FORMAT YOUR RESPONSE AS:

# WEEBA AI — WEBSITE COPY

[Then each section as above, clearly labeled]

Be persuasive, specific, outcome-driven. Use German B2B tone (professional, credible, not hype). Include placeholder [LIKE THIS] for sections they'll customize with real case studies/clients."""

        print("🚀 Deploying Copywriter Agent (Claude Opus)...\n")

        try:
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=12000,
                thinking={
                    "type": "adaptive"
                },
                messages=[{
                    "role": "user",
                    "content": copy_prompt
                }]
            )

            # Extract copy
            copy_text = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    copy_text = block.text
                    break

            if copy_text:
                print("✅ Copywriter agent completed\n")

                # Save copy
                output_dir = Path(__file__).parent.parent / "outputs"
                output_dir.mkdir(exist_ok=True)

                copy_file = output_dir / "WEEBA_AI_WEBSITE_COPY.md"
                with open(copy_file, 'w', encoding='utf-8') as f:
                    f.write("# WEEBA AI — COMPLETE WEBSITE COPY\n")
                    f.write(f"Generated: {datetime.now().isoformat()}\n")
                    f.write("Status: READY FOR DESIGNER\n\n")
                    f.write(copy_text)

                print("=" * 130)
                print("✨ COPYWRITER AGENT COMPLETE")
                print("=" * 130)
                print(f"\n📝 DELIVERABLE: Complete website copy")
                print(f"   📄 File: {copy_file}")
                print(f"\n🎯 NEXT STEP:")
                print("   1. Review the copy")
                print("   2. Upload your branding (logo, colors, images)")
                print("   3. Add case study details")
                print("   4. Upload partner logos")
                print("   5. Deploy Designer Agent for UI/UX\n")
                print("=" * 130 + "\n")

                # Display first part of copy
                print("PREVIEW (First 2000 chars):\n")
                print(copy_text[:2000])
                print("\n[... see full copy in outputs/WEEBA_AI_WEBSITE_COPY.md]\n")

                return 0

            else:
                print("❌ No copy generated")
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

    orchestrator = CopywriterOrchestrator()
    return orchestrator.orchestrate_copywriting()


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Demo of talking to the Master Orchestrator
Shows example conversation
"""

import os
from anthropic import Anthropic

def demo_conversation():
    """Run a demo conversation with the Chief Intelligence Officer."""

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set")
        print("\nSet it first in PowerShell:")
        print("  $env:ANTHROPIC_API_KEY='sk-ant-your-key'")
        return

    client = Anthropic()

    print("\n" + "=" * 100)
    print("🎖️  MASTER ORCHESTRATOR - CHIEF INTELLIGENCE OFFICER")
    print("=" * 100)
    print("\nI am your Chief Intelligence Officer for Weeba AI.")
    print("Strategic Goal: Be the #1 automation partner for performance marketing operations")
    print("\nLet's discuss your competitive position and market strategy.\n")
    print("=" * 100 + "\n")

    conversation = []

    # Example 1: Current Status
    print("YOU: What's our current competitive position?\n")
    conversation.append({
        "role": "user",
        "content": """As Chief Intelligence Officer for Weeba AI, provide a brief assessment of our
competitive position. Our goal is to be #1 automation partner for performance marketing.
What's our current standing vs competitors like CloudOrange, AutomationStudio, and IntegrationPro?
Format as bullet points."""
    })

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1500,
        system="""You are the Chief Intelligence Officer for Weeba AI.
Goal: Be the #1 automation partner for performance marketing operations.
Provide strategic executive-level intelligence.
Be concise, analytical, and focused on competitive advantage.""",
        messages=conversation
    )

    answer = response.content[0].text
    conversation.append({"role": "assistant", "content": answer})

    print("CHIEF INTELLIGENCE OFFICER:")
    print(answer)
    print("\n" + "-" * 100 + "\n")

    # Example 2: Recommendations
    print("YOU: What do we need to do to become #1?\n")
    conversation.append({
        "role": "user",
        "content": """Based on competitive analysis, what are the top 3-5 strategic initiatives
we should execute in the next 90 days to become the #1 automation partner for performance marketing?
Focus on what's different, what will give us competitive advantage, and what will accelerate growth."""
    })

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2000,
        system="""You are the Chief Intelligence Officer for Weeba AI.
Provide strategic recommendations to achieve market leadership.
Focus on differentiation, competitive advantage, and execution clarity.
Be bold but grounded in market reality.""",
        messages=conversation
    )

    answer = response.content[0].text
    conversation.append({"role": "assistant", "content": answer})

    print("CHIEF INTELLIGENCE OFFICER:")
    print(answer)
    print("\n" + "-" * 100 + "\n")

    # Example 3: Competitive Threats
    print("YOU: What's the biggest competitive threat right now?\n")
    conversation.append({
        "role": "user",
        "content": """What is the single biggest competitive threat we face in the next 6 months?
Who are we losing business to? What are they doing better? How do we respond?"""
    })

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1500,
        system="""You are the Chief Intelligence Officer analyzing competitive threats.
Be honest about dangers.
Identify specific competitors and specific competitive advantages.
Provide actionable defensive strategies.""",
        messages=conversation
    )

    answer = response.content[0].text
    conversation.append({"role": "assistant", "content": answer})

    print("CHIEF INTELLIGENCE OFFICER:")
    print(answer)
    print("\n" + "-" * 100 + "\n")

    # Example 4: Market Opportunity
    print("YOU: Where's the biggest market opportunity?\n")
    conversation.append({
        "role": "user",
        "content": """What's the biggest untapped market opportunity for Weeba AI in the next 12 months?
What market segment or service are we NOT addressing that competitors are missing?
How much revenue could we capture?"""
    })

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1500,
        system="""You are the Chief Intelligence Officer identifying market opportunities.
Look for underserved segments.
Identify emerging needs.
Quantify opportunity size and timing.
Recommend go-to-market strategy.""",
        messages=conversation
    )

    answer = response.content[0].text
    conversation.append({"role": "assistant", "content": answer})

    print("CHIEF INTELLIGENCE OFFICER:")
    print(answer)
    print("\n" + "-" * 100 + "\n")

    # Example 5: Investment Priorities
    print("YOU: How should we allocate resources?\n")
    conversation.append({
        "role": "user",
        "content": """If we have €200k to invest over the next 90 days, how should we allocate it
to achieve #1 market position fastest? What's the ROI priority?"""
    })

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1500,
        system="""You are the Chief Intelligence Officer allocating investment for market dominance.
Focus on highest ROI initiatives.
Consider both offense (grow faster) and defense (protect position).
Be specific about budget allocation.""",
        messages=conversation
    )

    answer = response.content[0].text
    conversation.append({"role": "assistant", "content": answer})

    print("CHIEF INTELLIGENCE OFFICER:")
    print(answer)
    print("\n" + "=" * 100)
    print("\n✅ This is what it's like to talk to your Chief Intelligence Officer.")
    print("\nTo have a real interactive conversation, run:")
    print("  python3 talk_to_orchestrator.py")
    print("\nOr set up the local script:")
    print("  PowerShell: python talk_to_orchestrator.py")
    print("\n" + "=" * 100 + "\n")


if __name__ == "__main__":
    demo_conversation()

#!/usr/bin/env python3
"""
LinkedIn Intelligence Agent
Reads competitors from shared memory and finds their LinkedIn profiles
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic
from shared_memory import SharedMemory


class LinkedInAgent:
    """Agent that finds and analyzes LinkedIn profiles for competitors."""

    def __init__(self, memory_dir: str = "agents_memory"):
        """Initialize LinkedIn agent with access to shared memory."""
        self.memory = SharedMemory(memory_dir)
        self.client = Anthropic()
        self.agent_name = "linkedin_agent"

    def run(self):
        """Run the LinkedIn intelligence agent."""
        print("\n" + "=" * 70)
        print("🔗 LINKEDIN INTELLIGENCE AGENT")
        print("=" * 70)
        print(f"Timestamp: {datetime.now().isoformat()}\n")

        # Get competitors from shared memory
        competitors = self.memory.get_competitors()

        if not competitors:
            print("❌ No competitors found in shared memory")
            print("   Run the scraper agent first to discover competitors")
            return []

        print(f"📍 Found {len(competitors)} competitors in shared memory")
        print("   Reading from: agents_memory/competitors.json\n")

        # Update status
        self.memory.set_agent_status(
            self.agent_name,
            "running",
            f"Analyzing LinkedIn for {len(competitors)} competitors"
        )

        # Initialize conversation
        messages = []

        # Create prompt with competitor context
        context_prompt = f"""You are a LinkedIn intelligence agent. You have access to a list of discovered competitors.

Here are the competitors you need to find on LinkedIn:

{json.dumps(competitors, indent=2, ensure_ascii=False)}

For each competitor:
1. Find their official LinkedIn company page
2. Get their LinkedIn URL
3. Note any recent posts or engagement patterns
4. Check if they have active content strategy
5. Look for key team members or thought leaders

Return structured data with:
- company_name
- linkedin_url (if found)
- company_size (if available)
- recent_posts (if available)
- engagement_level (low/medium/high)
- key_focus_areas

Search thoroughly for each company."""

        messages.append({
            "role": "user",
            "content": context_prompt
        })

        # First turn: Agent searches LinkedIn
        print("🔍 Agent searching LinkedIn for competitor profiles...\n")
        self.memory.set_agent_status(
            self.agent_name,
            "searching",
            "Searching LinkedIn for competitor profiles"
        )

        response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4000,
            system="""You are a LinkedIn intelligence analyst. Use your knowledge of LinkedIn to help
find competitor company pages and analyze their presence. You have access to real LinkedIn URLs and
profiles from your training data.

For each competitor, provide the LinkedIn company page URL and key intelligence.""",
            messages=messages
        )

        search_response = response.content[0].text
        messages.append({
            "role": "assistant",
            "content": search_response
        })

        # Second turn: Extract structured data
        extraction_prompt = """Now extract the LinkedIn data into JSON format.
For each competitor provide:
{
  "company_name": "...",
  "linkedin_url": "https://linkedin.com/company/...",
  "company_size": "50-200" or null,
  "recent_posts": ["topic1", "topic2"],
  "engagement_level": "low|medium|high",
  "key_focus_areas": ["automation", "integration"],
  "found": true/false
}

Return ONLY valid JSON array."""

        messages.append({
            "role": "user",
            "content": extraction_prompt
        })

        print("📊 Agent extracting LinkedIn data...\n")
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

        # Parse results
        import re
        try:
            json_match = re.search(r'\[\s*{.*?}\s*\]', extraction_response, re.DOTALL)
            if json_match:
                linkedin_data = json.loads(json_match.group(0))
            else:
                linkedin_data = json.loads(extraction_response)
        except json.JSONDecodeError as e:
            print(f"⚠️  Failed to parse LinkedIn data: {e}")
            linkedin_data = []

        # Save to shared memory
        self.memory.save_linkedin_profiles(linkedin_data)

        # Print results
        self._print_results(linkedin_data)

        # Update status
        self.memory.set_agent_status(
            self.agent_name,
            "completed",
            f"Found LinkedIn profiles for {len(linkedin_data)} competitors"
        )

        return linkedin_data

    def _print_results(self, profiles: list):
        """Print LinkedIn search results."""
        print("=" * 70)
        print("📋 LINKEDIN PROFILES FOUND")
        print("=" * 70)

        found = [p for p in profiles if p.get("found")]
        not_found = [p for p in profiles if not p.get("found")]

        print(f"\n✅ Profiles found: {len(found)}")
        for profile in found[:5]:
            print(f"\n  • {profile.get('company_name')}")
            if profile.get('linkedin_url'):
                print(f"    URL: {profile['linkedin_url']}")
            if profile.get('company_size'):
                print(f"    Size: {profile['company_size']}")
            if profile.get('engagement_level'):
                print(f"    Engagement: {profile['engagement_level']}")
            if profile.get('key_focus_areas'):
                print(f"    Focus: {', '.join(profile['key_focus_areas'])}")

        if not_found:
            print(f"\n❌ Profiles not found: {len(not_found)}")
            for profile in not_found[:3]:
                print(f"  • {profile.get('company_name')}")

        print("\n" + "=" * 70)
        print("✅ RESULTS SAVED TO SHARED MEMORY")
        print("   File: agents_memory/linkedin_profiles.json")
        print("=" * 70 + "\n")


def main():
    """Main execution."""
    try:
        agent = LinkedInAgent()
        profiles = agent.run()
        return 0 if profiles else 1
    except Exception as e:
        print(f"❌ LinkedIn Agent failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

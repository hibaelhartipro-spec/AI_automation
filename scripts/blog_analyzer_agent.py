#!/usr/bin/env python3
"""
Blog Analyzer Agent
Reads competitors from shared memory and analyzes their blog content strategy
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic
from shared_memory import SharedMemory


class BlogAnalyzerAgent:
    """Agent that analyzes competitor blog content strategy."""

    def __init__(self, memory_dir: str = "agents_memory"):
        """Initialize blog analyzer agent with access to shared memory."""
        self.memory = SharedMemory(memory_dir)
        self.client = Anthropic()
        self.agent_name = "blog_analyzer"

    def run(self):
        """Run the blog analyzer agent."""
        print("\n" + "=" * 70)
        print("📝 BLOG ANALYZER AGENT")
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
            f"Analyzing blogs for {len(competitors)} competitors"
        )

        # Initialize conversation
        messages = []

        # Create prompt with competitor context
        context_prompt = f"""You are a content strategy analyst. You have access to a list of discovered competitors
and need to analyze their blog/content strategy.

Here are the competitors:

{json.dumps(competitors, indent=2, ensure_ascii=False)}

For each competitor:
1. Identify if they have a blog or content hub
2. Determine their main content topics/categories
3. Analyze their content frequency and depth
4. Identify content gaps (what they DON'T cover)
5. Understand their target audience
6. Note their content format (blog posts, case studies, whitepapers, etc.)

Return structured intelligence about their content strategy."""

        messages.append({
            "role": "user",
            "content": context_prompt
        })

        # First turn: Agent analyzes blogs
        print("🔍 Agent analyzing competitor blog strategies...\n")
        self.memory.set_agent_status(
            self.agent_name,
            "analyzing",
            "Analyzing competitor blog content"
        )

        response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4000,
            system="""You are a content strategist analyzing competitor blogs. Based on the competitor information
provided, identify their blog URLs, content topics, and content strategy.

From company websites and your knowledge, you should be able to infer:
- Where their blog is likely located
- What topics they cover
- Content gaps in their strategy
- Their content calendar patterns""",
            messages=messages
        )

        analysis_response = response.content[0].text
        messages.append({
            "role": "assistant",
            "content": analysis_response
        })

        # Second turn: Extract structured data
        extraction_prompt = """Now extract the blog analysis into JSON format.
For each competitor provide:
{
  "company_name": "...",
  "blog_url": "https://...",
  "has_blog": true/false,
  "main_topics": ["topic1", "topic2", "topic3"],
  "content_gaps": ["gap1", "gap2"],
  "content_formats": ["blog posts", "case studies"],
  "posting_frequency": "weekly|biweekly|monthly",
  "target_audience": "...",
  "content_strategy_strength": "weak|moderate|strong"
}

Return ONLY valid JSON array."""

        messages.append({
            "role": "user",
            "content": extraction_prompt
        })

        print("📊 Agent extracting blog analysis...\n")
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
                blog_data = json.loads(json_match.group(0))
            else:
                blog_data = json.loads(extraction_response)
        except json.JSONDecodeError as e:
            print(f"⚠️  Failed to parse blog data: {e}")
            blog_data = []

        # Save to shared memory
        self.memory.save_blog_analysis(blog_data)

        # Print results
        self._print_results(blog_data)

        # Update status
        self.memory.set_agent_status(
            self.agent_name,
            "completed",
            f"Analyzed blogs for {len(blog_data)} competitors"
        )

        return blog_data

    def _print_results(self, analyses: list):
        """Print blog analysis results."""
        print("=" * 70)
        print("📋 BLOG STRATEGY ANALYSIS")
        print("=" * 70)

        with_blogs = [a for a in analyses if a.get("has_blog")]
        without_blogs = [a for a in analyses if not a.get("has_blog")]

        print(f"\n✅ Competitors with blogs: {len(with_blogs)}")
        for analysis in with_blogs[:5]:
            print(f"\n  • {analysis.get('company_name')}")
            if analysis.get('blog_url'):
                print(f"    Blog: {analysis['blog_url']}")
            if analysis.get('main_topics'):
                print(f"    Topics: {', '.join(analysis['main_topics'])}")
            if analysis.get('posting_frequency'):
                print(f"    Frequency: {analysis['posting_frequency']}")
            if analysis.get('content_gaps'):
                print(f"    Gaps: {', '.join(analysis['content_gaps'][:3])}")
            if analysis.get('content_strategy_strength'):
                print(f"    Strategy Strength: {analysis['content_strategy_strength']}")

        if without_blogs:
            print(f"\n❌ Competitors without blogs: {len(without_blogs)}")
            for analysis in without_blogs[:3]:
                print(f"  • {analysis.get('company_name')} (Opportunity for advantage!)")

        print("\n" + "=" * 70)
        print("✅ ANALYSIS SAVED TO SHARED MEMORY")
        print("   File: agents_memory/blog_analysis.json")
        print("=" * 70 + "\n")


def main():
    """Main execution."""
    try:
        agent = BlogAnalyzerAgent()
        analyses = agent.run()
        return 0 if analyses else 1
    except Exception as e:
        print(f"❌ Blog Analyzer Agent failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

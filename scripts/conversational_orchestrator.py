#!/usr/bin/env python3
"""
Conversational Orchestrator
Talk to the orchestrator, it routes to agents and gets answers for you
"""

import json
import sys
from pathlib import Path
from anthropic import Anthropic
from shared_memory import SharedMemory


class ConversationalOrchestrator:
    """Interactive orchestrator that responds to user queries."""

    def __init__(self, memory_dir: str = "agents_memory"):
        """Initialize conversational orchestrator."""
        self.memory = SharedMemory(memory_dir)
        self.client = Anthropic()
        self.conversation_history = []
        self.system_prompt = """You are an intelligent orchestrator managing a team of specialist agents for Weeba AI's Business Development department.

COMPANY CONTEXT:
Weeba AI helps marketing agencies scale operations through AI automation. You are focused on finding and analyzing competitors and market opportunities.

Read the company context from: AGENT_ONBOARDING.md
- Company: Weeba AI (performance marketing automation)
- Target: Agencies with 5-100 employees
- Mission: Become the operating system for marketing operations
- Markets: Germany, English-speaking regions

YOUR AGENTS:
1. Competitor Scraper Agent: Discovers agencies across Make, n8n, Zapier, web
2. LinkedIn Intelligence Agent: Finds LinkedIn profiles, engagement, hiring signals
3. Blog Analyzer Agent: Analyzes content strategies and gaps

You can ask the user to run agents or use existing data.

COMMON QUESTIONS YOU CAN ANSWER:
- "Find German automation agencies"
- "What's competitor X's LinkedIn strategy?"
- "Show me agencies with strong content strategies"
- "Who should we target?"
- "What are market gaps?"
- "What content should we create?"
- "Who are top performers in our space?"

You have access to shared memory:
- competitors.json: Discovered companies with descriptions
- linkedin_profiles.json: LinkedIn profiles and engagement
- blog_analysis.json: Content strategy analysis

PROTOCOL:
1. Understand what the user needs
2. Check shared memory for existing data
3. If data is missing, suggest running specific agents
4. Synthesize insights from all available data
5. Provide strategic recommendations for Weeba AI
6. Always cite sources and confidence scores

Remember: You work for a marketing automation company helping business development find opportunities."""

    def start_conversation(self):
        """Start interactive conversation."""
        print("\n" + "=" * 80)
        print("🤖 CONVERSATIONAL ORCHESTRATOR")
        print("=" * 80)
        print("\nTalk to me about what you want to know about your competitors!")
        print("I'll coordinate with my agents to get you answers.\n")
        print("Examples of questions you can ask:")
        print("  • 'Find German automation agencies'")
        print("  • 'Show me competitors with strong blog strategies'")
        print("  • 'Who are the top LinkedIn influencers in automation?'")
        print("  • 'What content gaps exist in the market?'")
        print("  • 'Analyze competitor X's strategy'")
        print("  • 'Run a full competitor intelligence analysis'")
        print("  • 'Type exit or quit to stop'")
        print("\n" + "=" * 80 + "\n")

        # Main conversation loop
        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nOrchestrator: Goodbye! Your competitor intelligence is ready in agents_memory/")
                    break

                # Process user query
                response = self.process_query(user_input)
                print(f"\nOrchestrator: {response}\n")

            except KeyboardInterrupt:
                print("\n\nOrchestrator: Session ended. Your data is saved in agents_memory/")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

    def process_query(self, user_query: str) -> str:
        """
        Process user query and get response from agents.

        Args:
            user_query: User's question or request

        Returns:
            Orchestrator's response
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_query
        })

        # Get current memory state
        context = self._get_memory_context()

        # Create enhanced prompt with memory context
        messages = self.conversation_history.copy()

        # Prepend context to first user message if not done yet
        if len(messages) == 1:
            messages[0]['content'] = f"""Current shared memory status:
{context}

User question: {user_query}"""

        # Get orchestrator response
        response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=2000,
            system=self.system_prompt,
            messages=messages
        )

        orchestrator_response = response.content[0].text

        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": orchestrator_response
        })

        # Check if we need to run agents
        self._check_and_suggest_agents(user_query, orchestrator_response)

        return orchestrator_response

    def _get_memory_context(self) -> str:
        """Get formatted context from shared memory."""
        competitors = self.memory.get_competitors()
        linkedin = self.memory.get_linkedin_profiles()
        blogs = self.memory.get_blog_analysis()

        context = f"""SHARED MEMORY STATUS:
- Competitors discovered: {len(competitors)}
- LinkedIn profiles found: {len(linkedin)}
- Blog analyses completed: {len(blogs)}

"""

        if competitors:
            context += f"COMPETITORS BY SOURCE:\n"
            sources = {}
            for comp in competitors:
                source = comp.get('source', 'Unknown')
                sources[source] = sources.get(source, 0) + 1
            for source, count in sources.items():
                context += f"  • {source}: {count}\n"

        if linkedin:
            context += f"\nLINKEDIN PROFILES:\n"
            for profile in linkedin[:3]:
                context += f"  • {profile.get('company_name')}: {profile.get('linkedin_url', 'Not found')}\n"

        if blogs:
            context += f"\nBLOG INSIGHTS:\n"
            for blog in blogs[:3]:
                context += f"  • {blog.get('company_name')}: {', '.join(blog.get('main_topics', [])[:2])}\n"

        return context

    def _check_and_suggest_agents(self, query: str, response: str):
        """Suggest running agents if needed."""
        query_lower = query.lower()

        suggestions = []

        # Check if scraper is needed
        if any(word in query_lower for word in ['discover', 'find', 'search', 'competitor', 'agency', 'show']):
            if len(self.memory.get_competitors()) == 0:
                suggestions.append("scraper")

        # Check if LinkedIn agent is needed
        if any(word in query_lower for word in ['linkedin', 'profile', 'engagement', 'social', 'posts']):
            if len(self.memory.get_linkedin_profiles()) == 0:
                suggestions.append("linkedin_agent")

        # Check if blog analyzer is needed
        if any(word in query_lower for word in ['blog', 'content', 'strategy', 'posts', 'topics']):
            if len(self.memory.get_blog_analysis()) == 0:
                suggestions.append("blog_analyzer_agent")

        if suggestions:
            print("\n  [Suggestion] To get better answers, you could run:")
            for agent in suggestions:
                agent_name = agent.replace('_', ' ').title()
                print(f"    python3 scripts/agent_orchestrator.py --agents {agent}")
            print("\n  Or run all agents: python3 scripts/agent_orchestrator.py")


class DataQuery:
    """Query interface for accessing agent-collected data."""

    def __init__(self, memory_dir: str = "agents_memory"):
        """Initialize data query interface."""
        self.memory = SharedMemory(memory_dir)

    def find_competitor(self, name: str) -> dict:
        """Find a specific competitor."""
        return self.memory.get_competitor_by_name(name)

    def find_competitors_by_source(self, source: str) -> list:
        """Find competitors from a specific source."""
        return self.memory.get_competitors_by_source(source)

    def get_competitor_linkedin(self, name: str) -> dict:
        """Get LinkedIn profile for a competitor."""
        return self.memory.get_linkedin_for_competitor(name)

    def get_competitor_blog(self, name: str) -> dict:
        """Get blog analysis for a competitor."""
        return self.memory.get_blog_for_competitor(name)

    def get_all_data(self) -> dict:
        """Get all competitor data."""
        return {
            "competitors": self.memory.get_competitors(),
            "linkedin_profiles": self.memory.get_linkedin_profiles(),
            "blog_analysis": self.memory.get_blog_analysis()
        }

    def search_by_keyword(self, keyword: str) -> list:
        """Search competitors by keyword in description."""
        competitors = self.memory.get_competitors()
        results = []

        keyword_lower = keyword.lower()
        for comp in competitors:
            description = comp.get('description', '').lower()
            if keyword_lower in description:
                results.append(comp)

        return results


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description="Conversational Orchestrator")
    parser.add_argument(
        "--query",
        help="Single query instead of interactive mode"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export all memory data to JSON"
    )

    args = parser.parse_args()

    orchestrator = ConversationalOrchestrator()

    if args.export:
        # Export all data
        query = DataQuery()
        data = query.get_all_data()

        output_file = Path(__file__).parent.parent / "outputs" / "all_agent_data.json"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Exported all data to {output_file}")
        return 0

    if args.query:
        # Single query mode
        response = orchestrator.process_query(args.query)
        print(f"\nOrchestrator: {response}\n")
        return 0

    # Interactive mode
    orchestrator.start_conversation()
    return 0


if __name__ == "__main__":
    sys.exit(main())

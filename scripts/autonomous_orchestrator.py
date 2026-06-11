#!/usr/bin/env python3
"""
Autonomous Orchestrator with Agent Factory
Creates, manages, and removes agents based on business goals
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
from anthropic import Anthropic
from shared_memory import SharedMemory


class AgentFactory:
    """Factory for creating agents on-the-fly."""

    def __init__(self):
        self.created_agents = []
        self.agent_templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load agent templates for creation."""
        return {
            "scraper_agent": {
                "name": "Scraper Agent",
                "type": "discovery",
                "tools": ["web_scraping", "data_extraction", "api_calls"],
                "description": "Discovers and collects data from web sources",
                "script_template": "scraper_template.py"
            },
            "analysis_agent": {
                "name": "Analysis Agent",
                "type": "analysis",
                "tools": ["data_analysis", "pattern_recognition", "llm"],
                "description": "Analyzes data and identifies patterns",
                "script_template": "analysis_template.py"
            },
            "research_agent": {
                "name": "Research Agent",
                "type": "research",
                "tools": ["web_search", "information_retrieval", "synthesis"],
                "description": "Researches topics and gathers intelligence",
                "script_template": "research_template.py"
            },
            "outreach_agent": {
                "name": "Outreach Agent",
                "type": "communication",
                "tools": ["email", "messaging", "crm_integration"],
                "description": "Manages outreach and communication",
                "script_template": "outreach_template.py"
            },
            "enrichment_agent": {
                "name": "Enrichment Agent",
                "type": "data_enrichment",
                "tools": ["data_lookup", "api_integration", "verification"],
                "description": "Enriches existing data with additional information",
                "script_template": "enrichment_template.py"
            },
            "monitoring_agent": {
                "name": "Monitoring Agent",
                "type": "monitoring",
                "tools": ["tracking", "alerting", "notifications"],
                "description": "Monitors data and alerts on changes",
                "script_template": "monitoring_template.py"
            },
            "optimization_agent": {
                "name": "Optimization Agent",
                "type": "optimization",
                "tools": ["performance_analysis", "recommendations", "testing"],
                "description": "Optimizes processes and strategies",
                "script_template": "optimization_template.py"
            }
        }

    def create_agent(self, name: str, purpose: str, tools: List[str],
                    description: str = "") -> Dict[str, Any]:
        """
        Create a new agent with specified tools.

        Args:
            name: Agent name
            purpose: What the agent does
            tools: Tools available to the agent
            description: Detailed description

        Returns:
            Agent configuration
        """
        agent_config = {
            "id": f"agent_{len(self.created_agents) + 1}",
            "name": name,
            "purpose": purpose,
            "tools": tools,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "effectiveness_score": 1.0,
            "runs_count": 0,
            "success_rate": 0.0
        }

        self.created_agents.append(agent_config)
        return agent_config

    def remove_agent(self, agent_id: str, reason: str = "") -> bool:
        """Remove an agent that's no longer needed."""
        for agent in self.created_agents:
            if agent["id"] == agent_id:
                agent["status"] = "removed"
                agent["removed_at"] = datetime.now().isoformat()
                agent["removal_reason"] = reason
                return True
        return False

    def update_agent_performance(self, agent_id: str, success: bool):
        """Track agent performance."""
        for agent in self.created_agents:
            if agent["id"] == agent_id:
                agent["runs_count"] += 1
                total_successes = int(agent["success_rate"] * (agent["runs_count"] - 1))
                if success:
                    total_successes += 1
                agent["success_rate"] = total_successes / agent["runs_count"]
                agent["effectiveness_score"] = agent["success_rate"]


class AutonomousOrchestrator:
    """Autonomous orchestrator that manages agents and executes strategies."""

    def __init__(self, memory_dir: str = "agents_memory"):
        self.memory = SharedMemory(memory_dir)
        self.client = Anthropic()
        self.factory = AgentFactory()
        self.active_agents = {}
        self.goals = []
        self.conversation_history = []
        self.execution_log = []

    def start_autonomous_mode(self):
        """Start autonomous orchestrator in goal-driven mode."""
        print("\n" + "=" * 80)
        print("🎯 AUTONOMOUS ORCHESTRATOR - GOAL-DRIVEN MODE")
        print("=" * 80)
        print("\nI am your autonomous agent manager. Tell me what you want to achieve,")
        print("and I will decide what agents to create, what tools they need,")
        print("and how to execute the strategy.\n")
        print("Examples of goals:")
        print("  • 'Identify and analyze our top 50 competitors'")
        print("  • 'Find high-fit agency prospects for outreach'")
        print("  • 'Monitor competitor pricing and track changes'")
        print("  • 'Create a complete market intelligence report'")
        print("  • 'Build a lead enrichment and scoring system'")
        print("\nType 'exit' to quit, 'show agents' to see active agents\n")
        print("=" * 80 + "\n")

        while True:
            try:
                user_goal = input("Your Goal: ").strip()

                if not user_goal:
                    continue

                if user_goal.lower() == "exit":
                    print("\nOrchestrator: Shutting down. All results saved.")
                    self._save_execution_log()
                    break

                if user_goal.lower() == "show agents":
                    self._show_agents()
                    continue

                # Process the goal autonomously
                response = self.process_goal_autonomously(user_goal)
                print(f"\nOrchestrator: {response}\n")

            except KeyboardInterrupt:
                print("\n\nSession ended.")
                self._save_execution_log()
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

    def process_goal_autonomously(self, goal: str) -> str:
        """
        Autonomously process a business goal by:
        1. Understanding the goal
        2. Breaking it into tasks
        3. Creating agents as needed
        4. Assigning tools
        5. Executing the strategy
        6. Removing agents if no longer needed
        """

        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": goal
        })

        # Get context
        context = self._get_full_context()

        # Create strategic planning prompt
        planning_prompt = f"""You are an autonomous agent manager for Weeba AI's business development team.

GOAL: {goal}

COMPANY CONTEXT:
{context}

AVAILABLE AGENT TYPES:
1. Scraper Agent - Web scraping and data collection
2. Analysis Agent - Data analysis and pattern recognition
3. Research Agent - Topic research and intelligence gathering
4. Outreach Agent - Communication and engagement
5. Enrichment Agent - Data enrichment and verification
6. Monitoring Agent - Tracking and alerting
7. Optimization Agent - Process optimization and recommendations

YOUR TASK:
1. Analyze the goal and break it into specific tasks
2. Identify what agents you need to create
3. For each agent, specify:
   - Agent name and purpose
   - Specific tools it needs
   - What data it will collect/process
4. Describe the execution strategy (what agents run in what order)
5. Identify any agents that should be removed if they exist
6. Provide a brief execution plan

Respond as JSON with this structure:
{{
  "goal_analysis": "Why this goal matters for Weeba AI",
  "required_agents": [
    {{
      "name": "Agent Name",
      "purpose": "What it does",
      "tools": ["tool1", "tool2"],
      "task": "Specific responsibility"
    }}
  ],
  "execution_strategy": "How agents work together",
  "agents_to_remove": ["agent_id if any"],
  "success_metrics": ["How we measure success"],
  "estimated_timeline": "How long this should take"
}}"""

        messages = self.conversation_history.copy()
        messages[-1] = {"role": "user", "content": planning_prompt}

        # Get strategic plan from Claude
        print("\n🤔 Analyzing goal and creating strategy...")
        response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=3000,
            system="""You are an autonomous agent manager with the power to create, configure, and remove agents.
You think strategically about what's needed to achieve business goals.
You assign tools intelligently based on task requirements.
You decide when agents are no longer needed and remove them.
You always respond with structured JSON for processing.""",
            messages=messages
        )

        strategy_text = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": strategy_text
        })

        # Parse strategy
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', strategy_text, re.DOTALL)
            if json_match:
                strategy = json.loads(json_match.group(0))
            else:
                strategy = json.loads(strategy_text)
        except json.JSONDecodeError:
            return f"Strategy created (couldn't parse JSON): {strategy_text[:200]}..."

        # Execute strategy
        print("🚀 Executing strategy...\n")

        created_agents_list = []
        removed_agents_list = []

        # Create required agents
        for agent_spec in strategy.get("required_agents", []):
            agent = self.factory.create_agent(
                name=agent_spec["name"],
                purpose=agent_spec["purpose"],
                tools=agent_spec["tools"],
                description=agent_spec["task"]
            )
            created_agents_list.append(agent)
            self.active_agents[agent["id"]] = agent
            print(f"  ✅ Created: {agent['name']}")
            print(f"     Purpose: {agent['purpose']}")
            print(f"     Tools: {', '.join(agent['tools'])}\n")

        # Remove agents if needed
        for agent_id in strategy.get("agents_to_remove", []):
            if agent_id in self.active_agents:
                self.factory.remove_agent(agent_id, "No longer needed for current goals")
                removed_agents_list.append(agent_id)
                print(f"  🗑️  Removed: {agent_id} (no longer needed)\n")

        # Save execution log
        execution = {
            "timestamp": datetime.now().isoformat(),
            "goal": goal,
            "strategy": strategy,
            "created_agents": created_agents_list,
            "removed_agents": removed_agents_list
        }
        self.execution_log.append(execution)

        # Generate response
        response_text = f"""✅ Strategy Executed!

📊 PLAN:
{strategy.get('goal_analysis', '')}

🤖 AGENTS CREATED:
"""
        for agent in created_agents_list:
            response_text += f"  • {agent['name']}: {agent['purpose']}\n"

        if removed_agents_list:
            response_text += f"\n🗑️  AGENTS REMOVED: {len(removed_agents_list)} (no longer needed)\n"

        response_text += f"""
⚙️ EXECUTION STRATEGY:
{strategy.get('execution_strategy', '')}

📈 SUCCESS METRICS:
"""
        for metric in strategy.get("success_metrics", []):
            response_text += f"  • {metric}\n"

        response_text += f"\n⏱️  TIMELINE: {strategy.get('estimated_timeline', 'N/A')}"

        return response_text

    def _get_full_context(self) -> str:
        """Get full business context for decision-making."""
        # Read onboarding document
        onboarding_path = Path(__file__).parent.parent / "AGENT_ONBOARDING.md"
        if onboarding_path.exists():
            with open(onboarding_path) as f:
                onboarding = f.read()[:2000]  # First 2000 chars
        else:
            onboarding = "Company context not available"

        # Get memory state
        competitors = self.memory.get_competitors()
        linkedin = self.memory.get_linkedin_profiles()
        blogs = self.memory.get_blog_analysis()

        context = f"""COMPANY INFO:
{onboarding}

CURRENT DATA IN MEMORY:
- Competitors discovered: {len(competitors)}
- LinkedIn profiles found: {len(linkedin)}
- Blog analyses completed: {len(blogs)}

ACTIVE AGENTS: {len(self.active_agents)}
{json.dumps([a['name'] for a in self.active_agents.values()], indent=2)}"""

        return context

    def _show_agents(self):
        """Display active agents and their status."""
        print("\n" + "=" * 70)
        print("🤖 ACTIVE AGENTS")
        print("=" * 70)

        if not self.active_agents:
            print("No active agents. Set a goal to create agents!")
        else:
            for agent_id, agent in self.active_agents.items():
                print(f"\n📍 {agent['name']} (ID: {agent_id})")
                print(f"   Purpose: {agent['purpose']}")
                print(f"   Tools: {', '.join(agent['tools'])}")
                print(f"   Status: {agent['status']}")
                print(f"   Runs: {agent['runs_count']}")
                print(f"   Success Rate: {agent['success_rate']:.1%}")
                print(f"   Effectiveness: {agent['effectiveness_score']:.2f}/1.0")

        print("\n" + "=" * 70 + "\n")

    def _save_execution_log(self):
        """Save execution log to file."""
        output_file = Path(__file__).parent.parent / "outputs" / "orchestrator_execution_log.json"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_executions": len(self.execution_log),
                "agents_created": len(self.factory.created_agents),
                "active_agents": list(self.active_agents.keys()),
                "executions": self.execution_log
            }, f, indent=2)

        print(f"✅ Execution log saved to {output_file}")


def main():
    """Main execution."""
    try:
        orchestrator = AutonomousOrchestrator()
        orchestrator.start_autonomous_mode()
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

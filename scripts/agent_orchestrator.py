#!/usr/bin/env python3
"""
Agent Orchestrator
Coordinates multiple agents and manages shared memory context
"""

import subprocess
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from shared_memory import SharedMemory


class AgentOrchestrator:
    """Orchestrates multiple agents with shared memory."""

    def __init__(self, memory_dir: str = "agents_memory"):
        """Initialize orchestrator."""
        self.memory = SharedMemory(memory_dir)
        self.agents = [
            {
                "name": "competitor_scraper_agent",
                "script": "scripts/competitor_scraper_agent.py",
                "description": "Discovers competitors across platforms",
                "required": True
            },
            {
                "name": "linkedin_agent",
                "script": "scripts/linkedin_agent.py",
                "description": "Finds LinkedIn profiles for competitors",
                "required": False
            },
            {
                "name": "blog_analyzer_agent",
                "script": "scripts/blog_analyzer_agent.py",
                "description": "Analyzes competitor blog strategies",
                "required": False
            }
        ]

    def run_full_orchestration(self, agents_to_run: list = None):
        """
        Run all agents in sequence with shared memory.

        Args:
            agents_to_run: List of agent names to run (None = all)
        """
        print("\n" + "=" * 80)
        print("🎭 MULTI-AGENT ORCHESTRATOR - FULL EXECUTION PIPELINE")
        print("=" * 80)
        print(f"Start time: {datetime.now().isoformat()}\n")

        # Initialize orchestrator status
        self.memory.update_context(
            status="orchestrator_running",
            start_time=datetime.now().isoformat(),
            current_phase="initialization"
        )

        # Determine which agents to run
        agents_to_execute = []
        if agents_to_run:
            agents_to_execute = [a for a in self.agents if a["name"] in agents_to_run]
        else:
            agents_to_execute = self.agents

        print(f"📋 EXECUTION PLAN ({len(agents_to_execute)} agents):")
        print("=" * 80)
        for i, agent in enumerate(agents_to_execute, 1):
            print(f"{i}. {agent['name']:<30} - {agent['description']}")
            print(f"   Script: {agent['script']}")
        print("=" * 80 + "\n")

        results = {}
        failed_agents = []

        # Execute agents in sequence
        for i, agent in enumerate(agents_to_execute, 1):
            print(f"\n{'=' * 80}")
            print(f"🚀 PHASE {i}/{len(agents_to_execute)}: {agent['name'].upper()}")
            print(f"{'=' * 80}")

            # Update orchestrator status
            self.memory.update_context(
                current_phase=agent['name'],
                current_step=f"{i}/{len(agents_to_execute)}"
            )

            # Mark agent as running
            self.memory.set_agent_status(agent['name'], "running", "Starting execution")

            try:
                # Run agent
                print(f"\n📍 Executing: {agent['script']}\n")
                result = self._run_agent(agent)

                if result['success']:
                    results[agent['name']] = result
                    print(f"\n✅ {agent['name']} completed successfully")
                else:
                    results[agent['name']] = result
                    if agent['required']:
                        print(f"\n❌ {agent['name']} failed (REQUIRED)")
                        failed_agents.append(agent['name'])
                    else:
                        print(f"\n⚠️  {agent['name']} failed (optional, continuing)")

                # Small delay between agents
                time.sleep(2)

            except Exception as e:
                print(f"\n❌ Error running {agent['name']}: {e}")
                results[agent['name']] = {
                    'success': False,
                    'error': str(e)
                }
                if agent['required']:
                    failed_agents.append(agent['name'])

        # Print summary
        self._print_summary(results, agents_to_execute, failed_agents)

        # Update final status
        final_status = "completed" if not failed_agents else "failed"
        self.memory.update_context(
            status=f"orchestrator_{final_status}",
            end_time=datetime.now().isoformat(),
            failed_agents=failed_agents,
            total_agents_run=len(agents_to_execute),
            successful_agents=len(agents_to_execute) - len(failed_agents)
        )

        return len(failed_agents) == 0

    def _run_agent(self, agent: dict) -> dict:
        """
        Run a single agent subprocess.

        Returns:
            Dictionary with success status and output
        """
        try:
            result = subprocess.run(
                [sys.executable, agent['script']],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )

            success = result.returncode == 0

            return {
                'success': success,
                'agent': agent['name'],
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'agent': agent['name'],
                'error': f"Agent timed out after 600 seconds"
            }
        except Exception as e:
            return {
                'success': False,
                'agent': agent['name'],
                'error': str(e)
            }

    def _print_summary(self, results: dict, agents: list, failed: list):
        """Print orchestration summary."""
        print("\n" + "=" * 80)
        print("📊 ORCHESTRATION SUMMARY")
        print("=" * 80)

        print(f"\nTotal agents executed: {len(agents)}")
        print(f"Successful: {len(agents) - len(failed)}")
        print(f"Failed: {len(failed)}")

        # Agent results
        print(f"\n📋 Agent Results:")
        for agent in agents:
            name = agent['name']
            result = results.get(name, {})
            status = "✅" if result.get('success') else "❌"
            print(f"  {status} {name}")

        # Show shared memory state
        print(f"\n📚 Shared Memory State:")
        competitors = self.memory.get_competitors()
        linkedin = self.memory.get_linkedin_profiles()
        blogs = self.memory.get_blog_analysis()

        print(f"  • Competitors: {len(competitors)}")
        print(f"  • LinkedIn profiles: {len(linkedin)}")
        print(f"  • Blog analyses: {len(blogs)}")

        # Show execution log
        log = self.memory.get_execution_log()
        if log:
            print(f"\n📝 Recent Actions ({len(log)} total):")
            for entry in log[-5:]:
                print(f"  • [{entry['agent']}] {entry['action']}: {entry['details']}")

        # Memory files location
        print(f"\n💾 Data Location: {self.memory.memory_dir}")
        print(f"  • Competitors: {self.memory.competitors_file}")
        print(f"  • LinkedIn profiles: {self.memory.linkedin_profiles_file}")
        print(f"  • Blog analysis: {self.memory.blog_analysis_file}")
        print(f"  • Execution log: {self.memory.execution_log}")

        # Failed agents warning
        if failed:
            print(f"\n⚠️  Failed Agents: {', '.join(failed)}")
            print("   Run individual agents to debug issues")

        print("\n" + "=" * 80)
        print("✅ ORCHESTRATION COMPLETE")
        print("=" * 80 + "\n")

    def print_memory_contents(self):
        """Print detailed memory contents."""
        print("\n" + "=" * 80)
        print("📚 SHARED MEMORY CONTENTS")
        print("=" * 80)

        # Competitors
        competitors = self.memory.get_competitors()
        print(f"\n🏢 COMPETITORS ({len(competitors)}):")
        for comp in competitors[:3]:
            print(f"  • {comp.get('company_name')}")
            print(f"    Website: {comp.get('website')}")
            print(f"    Source: {comp.get('source')}")

        # LinkedIn profiles
        linkedin = self.memory.get_linkedin_profiles()
        print(f"\n🔗 LINKEDIN PROFILES ({len(linkedin)}):")
        for profile in linkedin[:3]:
            print(f"  • {profile.get('company_name')}")
            print(f"    URL: {profile.get('linkedin_url', 'Not found')}")
            print(f"    Engagement: {profile.get('engagement_level', 'Unknown')}")

        # Blog analysis
        blogs = self.memory.get_blog_analysis()
        print(f"\n📝 BLOG ANALYSIS ({len(blogs)}):")
        for blog in blogs[:3]:
            print(f"  • {blog.get('company_name')}")
            print(f"    Blog: {blog.get('blog_url', 'Not found')}")
            print(f"    Topics: {', '.join(blog.get('main_topics', [])[:2])}")

        print("\n" + "=" * 80 + "\n")


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description="Multi-Agent Orchestrator")
    parser.add_argument(
        "--agents",
        nargs="+",
        help="Specific agents to run (default: all)"
    )
    parser.add_argument(
        "--show-memory",
        action="store_true",
        help="Show shared memory contents after execution"
    )
    parser.add_argument(
        "--clear-memory",
        action="store_true",
        help="Clear shared memory before starting (WARNING: deletes all data)"
    )

    args = parser.parse_args()

    orchestrator = AgentOrchestrator()

    # Clear memory if requested
    if args.clear_memory:
        print("⚠️  Clearing shared memory...")
        orchestrator.memory.clear_memory()
        print("✅ Memory cleared\n")

    # Run orchestration
    success = orchestrator.run_full_orchestration(agents_to_run=args.agents)

    # Show memory if requested
    if args.show_memory:
        orchestrator.print_memory_contents()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

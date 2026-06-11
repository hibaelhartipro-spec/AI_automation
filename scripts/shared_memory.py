#!/usr/bin/env python3
"""
Shared Memory System for Agent Collaboration
Allows multiple agents to read/write context and data
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional


class SharedMemory:
    """Shared context and data store for agent collaboration."""

    def __init__(self, memory_dir: str = "agents_memory"):
        """
        Initialize shared memory system.

        Args:
            memory_dir: Directory to store shared memory files
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)

        # Main data files
        self.competitors_file = self.memory_dir / "competitors.json"
        self.linkedin_profiles_file = self.memory_dir / "linkedin_profiles.json"
        self.blog_analysis_file = self.memory_dir / "blog_analysis.json"
        self.context_file = self.memory_dir / "context.json"
        self.execution_log = self.memory_dir / "execution_log.json"

    # ============================================================================
    # COMPETITORS DATA (Written by Scraper Agent, Read by Blog & LinkedIn Agents)
    # ============================================================================

    def save_competitors(self, competitors: List[Dict[str, Any]]) -> int:
        """
        Save discovered competitors to shared memory.

        Written by: Scraper Agent
        Read by: Blog Analyzer Agent, LinkedIn Agent, Content Agent
        """
        data = {
            "timestamp": datetime.now().isoformat(),
            "total": len(competitors),
            "competitors": competitors
        }

        with open(self.competitors_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self._log_action("scraper", "saved", f"{len(competitors)} competitors")
        return len(competitors)

    def get_competitors(self) -> List[Dict[str, Any]]:
        """
        Get all discovered competitors.

        Read by: Blog Analyzer, LinkedIn Agent, Content Strategy
        """
        if not self.competitors_file.exists():
            return []

        with open(self.competitors_file, encoding='utf-8') as f:
            data = json.load(f)
            return data.get("competitors", [])

    def get_competitor_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific competitor by name."""
        competitors = self.get_competitors()
        for comp in competitors:
            if comp.get("company_name", "").lower() == name.lower():
                return comp
        return None

    def get_competitors_by_source(self, source: str) -> List[Dict[str, Any]]:
        """Get competitors from specific source (Make, n8n, Zapier, etc.)."""
        competitors = self.get_competitors()
        return [c for c in competitors if c.get("source") == source]

    # ============================================================================
    # LINKEDIN PROFILES (Written by LinkedIn Agent, Read by Content/Outreach Agents)
    # ============================================================================

    def save_linkedin_profiles(self, profiles: List[Dict[str, Any]]) -> int:
        """
        Save LinkedIn profiles and URLs for competitors.

        Written by: LinkedIn Scraper Agent
        Read by: Content Strategy Agent, Outreach Agent
        """
        data = {
            "timestamp": datetime.now().isoformat(),
            "total": len(profiles),
            "profiles": profiles
        }

        with open(self.linkedin_profiles_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self._log_action("linkedin_agent", "saved", f"{len(profiles)} LinkedIn profiles")
        return len(profiles)

    def get_linkedin_profiles(self) -> List[Dict[str, Any]]:
        """Get all LinkedIn profiles for competitors."""
        if not self.linkedin_profiles_file.exists():
            return []

        with open(self.linkedin_profiles_file, encoding='utf-8') as f:
            data = json.load(f)
            return data.get("profiles", [])

    def get_linkedin_for_competitor(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Get LinkedIn profile for a specific competitor."""
        profiles = self.get_linkedin_profiles()
        for profile in profiles:
            if profile.get("company_name", "").lower() == company_name.lower():
                return profile
        return None

    def add_linkedin_profile(self, company_name: str, linkedin_url: str, recent_posts: List[str] = None, followers: int = 0):
        """Add or update a LinkedIn profile."""
        profiles = self.get_linkedin_profiles()

        # Check if already exists
        for profile in profiles:
            if profile.get("company_name", "").lower() == company_name.lower():
                profile.update({
                    "linkedin_url": linkedin_url,
                    "recent_posts": recent_posts or [],
                    "followers": followers,
                    "updated_at": datetime.now().isoformat()
                })
                self.save_linkedin_profiles(profiles)
                return profile

        # Add new profile
        new_profile = {
            "company_name": company_name,
            "linkedin_url": linkedin_url,
            "recent_posts": recent_posts or [],
            "followers": followers,
            "added_at": datetime.now().isoformat()
        }
        profiles.append(new_profile)
        self.save_linkedin_profiles(profiles)
        return new_profile

    # ============================================================================
    # BLOG ANALYSIS (Written by Blog Analyzer, Read by Content & Strategy Agents)
    # ============================================================================

    def save_blog_analysis(self, analyses: List[Dict[str, Any]]) -> int:
        """
        Save blog and content analysis for competitors.

        Written by: Blog Analyzer Agent
        Read by: Content Strategy Agent, Blog Writer Agent
        """
        data = {
            "timestamp": datetime.now().isoformat(),
            "total": len(analyses),
            "analyses": analyses
        }

        with open(self.blog_analysis_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self._log_action("blog_analyzer", "saved", f"{len(analyses)} blog analyses")
        return len(analyses)

    def get_blog_analysis(self) -> List[Dict[str, Any]]:
        """Get all blog analyses."""
        if not self.blog_analysis_file.exists():
            return []

        with open(self.blog_analysis_file, encoding='utf-8') as f:
            data = json.load(f)
            return data.get("analyses", [])

    def get_blog_for_competitor(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Get blog analysis for a specific competitor."""
        analyses = self.get_blog_analysis()
        for analysis in analyses:
            if analysis.get("company_name", "").lower() == company_name.lower():
                return analysis
        return None

    def add_blog_analysis(self, company_name: str, blog_url: str, top_topics: List[str] = None, content_gaps: List[str] = None):
        """Add or update blog analysis."""
        analyses = self.get_blog_analysis()

        # Check if already exists
        for analysis in analyses:
            if analysis.get("company_name", "").lower() == company_name.lower():
                analysis.update({
                    "blog_url": blog_url,
                    "top_topics": top_topics or [],
                    "content_gaps": content_gaps or [],
                    "updated_at": datetime.now().isoformat()
                })
                self.save_blog_analysis(analyses)
                return analysis

        # Add new analysis
        new_analysis = {
            "company_name": company_name,
            "blog_url": blog_url,
            "top_topics": top_topics or [],
            "content_gaps": content_gaps or [],
            "added_at": datetime.now().isoformat()
        }
        analyses.append(new_analysis)
        self.save_blog_analysis(analyses)
        return new_analysis

    # ============================================================================
    # SHARED CONTEXT (All agents read/write to understand execution state)
    # ============================================================================

    def get_context(self) -> Dict[str, Any]:
        """Get current execution context."""
        if not self.context_file.exists():
            return self._default_context()

        with open(self.context_file, encoding='utf-8') as f:
            return json.load(f)

    def update_context(self, **kwargs):
        """Update shared context."""
        context = self.get_context()
        context.update(kwargs)
        context["last_updated"] = datetime.now().isoformat()

        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(context, f, indent=2)

    def set_agent_status(self, agent_name: str, status: str, details: str = ""):
        """
        Update status for a specific agent.

        Status: running, completed, failed, waiting
        """
        context = self.get_context()

        if "agents" not in context:
            context["agents"] = {}

        context["agents"][agent_name] = {
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }

        self.update_context(**context)

    # ============================================================================
    # EXECUTION LOG (Track all agent actions)
    # ============================================================================

    def _log_action(self, agent: str, action: str, details: str):
        """Log agent actions for debugging."""
        log = self._read_log()

        log.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "details": details
        })

        with open(self.execution_log, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=2)

    def _read_log(self) -> List[Dict[str, Any]]:
        """Read execution log."""
        if not self.execution_log.exists():
            return []

        with open(self.execution_log, encoding='utf-8') as f:
            return json.load(f)

    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get all execution logs."""
        return self._read_log()

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    def _default_context(self) -> Dict[str, Any]:
        """Create default context structure."""
        return {
            "created_at": datetime.now().isoformat(),
            "agents": {},
            "status": "initialized",
            "current_phase": "discovery"
        }

    def print_summary(self):
        """Print memory summary."""
        competitors = self.get_competitors()
        linkedin = self.get_linkedin_profiles()
        blogs = self.get_blog_analysis()
        context = self.get_context()

        print("\n" + "=" * 70)
        print("📚 SHARED MEMORY SUMMARY")
        print("=" * 70)
        print(f"Competitors discovered: {len(competitors)}")
        print(f"LinkedIn profiles found: {len(linkedin)}")
        print(f"Blog analyses completed: {len(blogs)}")
        print(f"\nCurrent context: {context.get('status')}")
        print(f"Current phase: {context.get('current_phase')}")

        if context.get('agents'):
            print(f"\nAgent Status:")
            for agent_name, agent_data in context.get('agents', {}).items():
                print(f"  • {agent_name}: {agent_data.get('status')}")
                if agent_data.get('details'):
                    print(f"    {agent_data.get('details')}")

        print("=" * 70 + "\n")

    def clear_memory(self):
        """Clear all memory files (use with caution!)."""
        for file in [self.competitors_file, self.linkedin_profiles_file, self.blog_analysis_file]:
            if file.exists():
                file.unlink()
        print("⚠️  Shared memory cleared")


if __name__ == "__main__":
    # Example usage
    memory = SharedMemory()

    # Scraper saves competitors
    sample_competitors = [
        {
            "company_name": "CloudOrange GmbH",
            "website": "https://cloudorange.de",
            "description": "Automation agency",
            "source": "Make"
        }
    ]
    memory.save_competitors(sample_competitors)

    # LinkedIn agent saves profile
    memory.add_linkedin_profile(
        "CloudOrange GmbH",
        "https://linkedin.com/company/cloudorange",
        recent_posts=["Post 1", "Post 2"],
        followers=500
    )

    # Blog analyzer saves analysis
    memory.add_blog_analysis(
        "CloudOrange GmbH",
        "https://cloudorange.de/blog",
        top_topics=["Make", "Automation", "RPA"],
        content_gaps=["AI Agents", "Custom Integrations"]
    )

    # Print summary
    memory.print_summary()

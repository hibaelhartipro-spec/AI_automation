#!/usr/bin/env python3
"""
Interactive interface to talk directly to the Master Orchestrator
Run this locally on your machine
"""

import os
import sys
from pathlib import Path

# Add scripts to path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from master_orchestrator import MasterOrchestrator


def main():
    """Start interactive conversation with Master Orchestrator."""

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set")
        print("\nSet it first:")
        print("  PowerShell: $env:ANTHROPIC_API_KEY='sk-ant-your-key'")
        print("  Bash: export ANTHROPIC_API_KEY='sk-ant-your-key'")
        return 1

    # Start orchestrator
    orchestrator = MasterOrchestrator()
    orchestrator.start_executive_mode()

    return 0


if __name__ == "__main__":
    sys.exit(main())

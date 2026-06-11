# 🎭 Multi-Agent Intelligence System

## Overview

A coordinated system where multiple AI agents work together, sharing context and data:

```
Orchestrator (coordinator)
├── Agent 1: Scraper
│   └── Discovers competitors → Shared Memory
├── Agent 2: LinkedIn Agent
│   └── Reads competitors → Finds profiles → Updates shared memory
├── Agent 3: Blog Analyzer
│   └── Reads competitors → Analyzes blogs → Updates shared memory
└── All agents have access to each other's outputs (shared context)
```

## Architecture

### 1. **Shared Memory** (`shared_memory.py`)
Central context store that all agents read/write to:

```
agents_memory/
├── competitors.json           # Written by Scraper, read by all
├── linkedin_profiles.json     # Written by LinkedIn Agent
├── blog_analysis.json         # Written by Blog Analyzer
├── context.json               # Shared execution context
└── execution_log.json         # Track all agent actions
```

### 2. **Agents**

#### **Scraper Agent** (`competitor_scraper_agent.py`)
- **Writes to**: competitors.json
- **Function**: Discovers competitors from Make, n8n, Zapier, web
- **Output**: `[{company_name, website, description, source, ...}]`

#### **LinkedIn Agent** (`linkedin_agent.py`)
- **Reads from**: competitors.json (shared memory)
- **Writes to**: linkedin_profiles.json
- **Function**: Finds LinkedIn profiles for discovered competitors
- **Output**: `[{company_name, linkedin_url, engagement_level, ...}]`

#### **Blog Analyzer Agent** (`blog_analyzer_agent.py`)
- **Reads from**: competitors.json (shared memory)
- **Writes to**: blog_analysis.json
- **Function**: Analyzes competitor blog strategies
- **Output**: `[{company_name, blog_url, main_topics, content_gaps, ...}]`

### 3. **Orchestrator** (`agent_orchestrator.py`)
Coordinates all agents:
- ✅ Runs agents in sequence
- ✅ Manages shared memory
- ✅ Tracks execution state
- ✅ Handles errors and retries
- ✅ Reports results

## Usage

### Quick Start: Run All Agents

```bash
cd /home/user/AI_automation
python3 scripts/agent_orchestrator.py
```

This will:
1. ✅ Run scraper → discover competitors
2. ✅ Run LinkedIn agent → find profiles
3. ✅ Run blog analyzer → analyze content
4. ✅ All share context through shared memory

### Run Specific Agents

```bash
# Only run scraper and LinkedIn agent
python3 scripts/agent_orchestrator.py --agents competitor_scraper_agent linkedin_agent

# Only run blog analyzer (uses existing competitor data)
python3 scripts/agent_orchestrator.py --agents blog_analyzer_agent
```

### Show Memory Contents After Run

```bash
python3 scripts/agent_orchestrator.py --show-memory
```

Output:
```
📚 SHARED MEMORY CONTENTS
========================

🏢 COMPETITORS (45):
  • CloudOrange GmbH
    Website: https://cloudorange.de
    Source: Make

🔗 LINKEDIN PROFILES (32):
  • CloudOrange GmbH
    URL: https://linkedin.com/company/cloudorange
    Engagement: high

📝 BLOG ANALYSIS (45):
  • CloudOrange GmbH
    Blog: https://cloudorange.de/blog
    Topics: Make, Automation, RPA
```

### Clear Memory (Start Fresh)

```bash
python3 scripts/agent_orchestrator.py --clear-memory
```

⚠️ **Warning**: This deletes all discovered data!

---

## How Agents Share Context

### Example: LinkedIn Agent Using Scraper Data

**Scraper Agent writes:**
```json
{
  "company_name": "CloudOrange GmbH",
  "website": "https://cloudorange.de",
  "description": "Digital automation agency"
}
```

**LinkedIn Agent reads:**
```python
from shared_memory import SharedMemory

memory = SharedMemory()
competitors = memory.get_competitors()  # Reads scraper data!

for comp in competitors:
    print(f"Finding LinkedIn for: {comp['company_name']}")
    # Searches LinkedIn using the company name
```

**LinkedIn Agent writes:**
```python
memory.add_linkedin_profile(
    company_name="CloudOrange GmbH",
    linkedin_url="https://linkedin.com/company/cloudorange",
    recent_posts=["Automation Trends", "Make.com Best Practices"],
    followers=500
)
```

**Blog Analyzer can now access both:**
```python
comp = memory.get_competitor_by_name("CloudOrange GmbH")
linkedin = memory.get_linkedin_for_competitor("CloudOrange GmbH")
blog = memory.get_blog_for_competitor("CloudOrange GmbH")

print(f"{comp['company_name']}")
print(f"  Website: {comp['website']}")
print(f"  LinkedIn: {linkedin['linkedin_url']}")
print(f"  Blog Topics: {blog['main_topics']}")
```

---

## Shared Memory API

### Writing Data

**Competitors (Scraper writes)**
```python
from shared_memory import SharedMemory

memory = SharedMemory()
competitors = [...]
memory.save_competitors(competitors)
```

**LinkedIn Profiles (LinkedIn Agent writes)**
```python
memory.add_linkedin_profile(
    company_name="Company Name",
    linkedin_url="https://linkedin.com/company/...",
    recent_posts=["Topic1", "Topic2"],
    followers=500
)
```

**Blog Analysis (Blog Analyzer writes)**
```python
memory.add_blog_analysis(
    company_name="Company Name",
    blog_url="https://company.com/blog",
    top_topics=["Topic1", "Topic2"],
    content_gaps=["Gap1", "Gap2"]
)
```

### Reading Data

**Get all competitors**
```python
competitors = memory.get_competitors()
```

**Get specific competitor**
```python
comp = memory.get_competitor_by_name("CloudOrange GmbH")
```

**Get by source**
```python
make_partners = memory.get_competitors_by_source("Make")
```

**Get LinkedIn profile**
```python
linkedin = memory.get_linkedin_for_competitor("Company Name")
```

**Get blog analysis**
```python
blog = memory.get_blog_for_competitor("Company Name")
```

### Managing Context

**Update shared context**
```python
memory.update_context(
    status="initialized",
    current_phase="discovery"
)
```

**Set agent status**
```python
memory.set_agent_status(
    agent_name="scraper",
    status="running",
    details="Discovering competitors"
)
```

**Get execution log**
```python
log = memory.get_execution_log()
for entry in log:
    print(f"{entry['agent']}: {entry['action']}")
```

---

## Execution Flow

### Phase 1: Initialization
```
Orchestrator starts
  ↓
Initialize shared memory
  ↓
Create context & execution log
```

### Phase 2: Competitor Discovery
```
Scraper Agent runs
  ↓
Searches Make, n8n, Zapier, web
  ↓
Writes 45 competitors to shared memory
  ↓
Status: "completed"
```

### Phase 3: LinkedIn Intelligence
```
LinkedIn Agent runs
  ↓
Reads 45 competitors from shared memory
  ↓
Searches LinkedIn for each
  ↓
Writes 32 LinkedIn profiles to shared memory
  ↓
Status: "completed"
```

### Phase 4: Blog Analysis
```
Blog Analyzer Agent runs
  ↓
Reads 45 competitors from shared memory
  ↓
Analyzes blog strategies
  ↓
Writes 45 blog analyses to shared memory
  ↓
Status: "completed"
```

### Phase 5: Results
```
All agents complete
  ↓
Aggregated data in shared memory:
  - 45 competitors discovered
  - 32 LinkedIn profiles found
  - 45 blog strategies analyzed
  ↓
Ready for export to Google Sheets
```

---

## File Locations

```
/home/user/AI_automation/
├── scripts/
│   ├── shared_memory.py                # Core memory system
│   ├── agent_orchestrator.py           # Orchestrator
│   ├── competitor_scraper_agent.py     # Scraper
│   ├── linkedin_agent.py               # LinkedIn agent
│   └── blog_analyzer_agent.py          # Blog analyzer
│
├── agents_memory/                      # Shared memory directory
│   ├── competitors.json                # All competitors
│   ├── linkedin_profiles.json          # LinkedIn profiles
│   ├── blog_analysis.json              # Blog analyses
│   ├── context.json                    # Execution context
│   └── execution_log.json              # Action log
│
└── outputs/                            # Export formats
    ├── all_competitors.json            # For Google Sheets
    └── competitors_for_sheets.json     # Import-ready
```

---

## Extending the System

### Add a New Agent

1. **Create agent script** (`my_agent.py`):
```python
from shared_memory import SharedMemory

class MyAgent:
    def __init__(self, memory_dir="agents_memory"):
        self.memory = SharedMemory(memory_dir)
    
    def run(self):
        # Read from shared memory
        competitors = self.memory.get_competitors()
        
        # Do analysis
        results = []
        for comp in competitors:
            results.append(analyze(comp))
        
        # Write back to shared memory
        self.memory.save_my_results(results)
        
        return results
```

2. **Register in orchestrator**:
```python
# In agent_orchestrator.py
self.agents = [
    # ... existing agents ...
    {
        "name": "my_agent",
        "script": "scripts/my_agent.py",
        "description": "My new agent",
        "required": False
    }
]
```

3. **Run orchestrator**:
```bash
python3 scripts/agent_orchestrator.py
```

### Add a New Memory Type

```python
# In shared_memory.py
def save_my_data(self, data: List[Dict[str, Any]]) -> int:
    """Save custom data to shared memory."""
    with open(self.memory_dir / "my_data.json", 'w') as f:
        json.dump(data, f, indent=2)
    return len(data)

def get_my_data(self) -> List[Dict[str, Any]]:
    """Read custom data from shared memory."""
    # ... read from file ...
```

---

## Monitoring & Debugging

### Check Execution Log

```bash
# View all actions taken by agents
python3 -c "
from scripts.shared_memory import SharedMemory
memory = SharedMemory()
log = memory.get_execution_log()
for entry in log:
    print(f'{entry[\"timestamp\"]}: {entry[\"agent\"]} - {entry[\"action\"]}')"
```

### Check Agent Status

```bash
# View status of all agents
python3 -c "
from scripts.shared_memory import SharedMemory
memory = SharedMemory()
context = memory.get_context()
for agent, status in context.get('agents', {}).items():
    print(f'{agent}: {status[\"status\"]}')"
```

### Check Memory Summary

```bash
python3 -c "
from scripts.shared_memory import SharedMemory
memory = SharedMemory()
memory.print_summary()"
```

### Run Single Agent with Debug Output

```bash
python3 scripts/linkedin_agent.py 2>&1 | tee linkedin_debug.log
```

---

## Troubleshooting

### "No competitors found in shared memory"

**Cause**: Scraper agent hasn't run yet

**Solution**:
```bash
python3 scripts/agent_orchestrator.py --agents competitor_scraper_agent
```

### Agent hangs or times out

**Check status**:
```bash
ps aux | grep python3 | grep agent
```

**Kill agent**:
```bash
pkill -f "agent_orchestrator.py"
```

**Run with timeout**:
```bash
timeout 300 python3 scripts/agent_orchestrator.py
```

### Memory corruption or outdated data

**Clear and restart**:
```bash
python3 scripts/agent_orchestrator.py --clear-memory
python3 scripts/agent_orchestrator.py  # Run fresh
```

---

## Scheduling Automatic Runs

### Daily Orchestration (Cron)

```bash
# Add to crontab
crontab -e

# Run every day at 2 AM
0 2 * * * cd /home/user/AI_automation && ANTHROPIC_API_KEY="sk-..." python3 scripts/agent_orchestrator.py
```

### Weekly Orchestration

```bash
# Every Monday at 9 AM
0 9 * * 1 cd /home/user/AI_automation && ANTHROPIC_API_KEY="sk-..." python3 scripts/agent_orchestrator.py
```

### With Notifications

```bash
#!/bin/bash
cd /home/user/AI_automation
python3 scripts/agent_orchestrator.py --show-memory > agent_report.txt 2>&1
mail -s "Agent Orchestration Report" you@email.com < agent_report.txt
```

---

## Next Steps

1. **✅ Run the orchestrator**:
   ```bash
   python3 scripts/agent_orchestrator.py
   ```

2. **📊 Check shared memory**:
   ```bash
   ls -la agents_memory/
   cat agents_memory/competitors.json
   ```

3. **📥 Export to Google Sheets**:
   - Copy from agents_memory files
   - Import to your sheet

4. **📅 Schedule weekly runs**:
   ```bash
   crontab -e
   # Add scheduled run
   ```

5. **🚀 Extend with more agents**:
   - Add outreach agent
   - Add pricing analyzer
   - Add technology stack detector
   - Add custom analysis agents

---

**All agents automatically share context through shared memory!**

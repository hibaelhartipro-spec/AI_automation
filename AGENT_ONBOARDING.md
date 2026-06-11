# 🚀 Agent Onboarding & Company Context Document

**Last Updated:** 2026-06-11  
**Document Version:** 1.0  
**Status:** Live Document - Subject to Change

---

## Table of Contents

1. [Company Overview](#company-overview)
2. [Mission & Vision](#mission--vision)
3. [Target Audience](#target-audience)
4. [Core Services](#core-services)
5. [Business Development Department](#business-development-department)
6. [Agent Team Structure](#agent-team-structure)
7. [How to Add New Agents](#how-to-add-new-agents)
8. [Agent Communication Protocol](#agent-communication-protocol)

---

## Company Overview

### What is Weeba AI?

**Weeba AI** is an AI-powered performance marketing operations company that helps marketing agencies and in-house marketing teams eliminate repetitive operational work through intelligent automation systems.

### The Problem We Solve

Modern marketing teams waste significant time on operational activities instead of strategic growth:

- **Reporting** (15+ hours per client monthly)
- **Campaign Monitoring** (manual dashboard checking)
- **Data Analysis** (repetitive pattern identification)
- **Client Communication** (email/Slack management)
- **Lead Research** (manual prospecting)
- **Competitor Intelligence** (reactive discovery)

As agencies grow, these tasks grow proportionally - forcing companies to hire more staff rather than scale efficiently.

### Our Solution

**Intelligent operational systems** that automate the repetitive layer of performance marketing.

We don't sell software. We sell **outcomes** and **capacity**.

---

## Mission & Vision

### Mission

To become the operating system behind modern performance marketing agencies by automating operational execution and enabling teams to scale revenue without proportional headcount growth.

### Vision

Over the next decade, marketing agencies will transition to AI-enabled organizations where a significant portion of operational execution is performed by intelligent systems.

Every performance marketing team will eventually have a digital operations layer responsible for:

- Monitoring campaigns
- Producing reports
- Detecting anomalies
- Generating recommendations
- Handling client requests
- Researching competitors
- Enriching leads
- Triggering workflows
- Coordinating execution

**Weeba AI aims to become the company that builds and manages this operational layer globally.**

### Long-Term Roadmap

1. **Today**: Custom automation systems for specific clients
2. **Tomorrow**: Productized workflows for common use cases
3. **Future**: Global platform powering performance marketing operations

---

## Target Audience

### Primary Customers

**Performance Marketing Agencies** with:
- 5–100 employees
- Multiple client accounts
- Multi-channel advertising operations
- Established delivery teams

**Profile**: Agency owners with small teams, increasing operational complexity, wanting to scale without hiring.

### Secondary Customers

- **In-house marketing teams** at growth-stage companies
- **Advertising & media buying agencies**
- **Influencer marketing agencies**
- **Companies with internal marketing teams**

### NOT For

- Solopreneurs with single campaigns
- Businesses with minimal marketing activity
- Content creation services
- Social media management agencies
- Generic automation consulting

---

## Core Services

### 1. Reporting Automation

**What**: Automated systems that collect data from multiple platforms and generate client-ready reports

**Saves**: 15+ hours per client monthly

**Capabilities**:
- Google Ads reporting
- Meta Ads reporting
- TikTok Ads reporting
- AppsFlyer reporting
- Adjust reporting
- Cross-channel dashboards
- Executive summaries
- Performance scorecards

---

### 2. Campaign Monitoring Automation

**What**: Real-time systems that continuously evaluate account performance

**Saves**: Hours of manual monitoring, reduces wasted spend

**Capabilities**:
- Budget monitoring
- Spend anomaly detection
- CPA/ROAS monitoring
- Attribution monitoring
- Tracking validation
- Performance alerts
- Slack notifications

---

### 3. Analysis & Optimization Automation

**What**: AI systems that transform raw data into actionable insights

**Saves**: Hours of analysis work

**Capabilities**:
- Performance summaries
- Trend analysis
- Opportunity detection
- Optimization recommendations
- Budget allocation insights
- AI-generated strategic reviews

---

### 4. Client Request Automation

**What**: AI agents that process client communication and trigger workflows

**Saves**: Response time, operational workload

**Capabilities**:
- Email monitoring
- Request classification
- Priority scoring
- Task creation
- Workflow routing
- Automated responses

---

### 5. Lead Generation Automation

**What**: Automated systems that identify, qualify, and engage prospects

**Saves**: Manual prospecting effort

**Capabilities**:
- Prospect identification
- Company research
- Contact sourcing
- Outreach sequencing
- Follow-up automation
- Meeting booking triggers

---

### 6. Lead Enrichment Automation

**What**: AI research systems that gather context about prospects

**Saves**: Research time, improves personalization

**Capabilities**:
- LinkedIn monitoring
- Reddit monitoring
- Twitter/X monitoring
- Website intelligence
- Hiring signal detection
- News monitoring
- Competitive account research

---

### 7. Competitor Intelligence Automation

**What**: Continuous monitoring systems that track competitor activity

**Saves**: Time on market research, enables faster strategic response

**Capabilities**:
- Website monitoring
- Offer tracking
- Pricing monitoring
- Product launch tracking
- Content monitoring
- Positioning analysis
- Hiring intelligence

---

## Business Development Department

### Department Mission

Identify, qualify, and acquire new customers for Weeba AI's services.

### Department Goals (2026)

- Identify 50+ qualified agencies in target markets
- Develop competitive intelligence on 30+ direct competitors
- Create lead lists of 500+ high-fit prospects
- Build personalized outreach sequences
- Generate 20+ qualified meetings/month

### Department Values

- **Data-driven**: Every recommendation backed by research
- **Intelligent**: Use AI to amplify human effort
- **Scalable**: Build systems that work at scale
- **Quality-focused**: Focus on fit, not volume

---

## Agent Team Structure

### 📊 Current Team (Business Development)

All agents have access to shared memory and company context through this document.

---

## 🔎 Agent 1: Competitor Scraper Agent

### Role

Discover and track competitor agencies and automation platforms in the performance marketing space.

### Responsibilities

- Discover competitors across Make, n8n, Zapier, and broader web
- Extract company names, websites, and descriptions
- Identify direct and indirect competitors
- Track German/English-speaking automation agencies
- Monitor Make Partners Directory for potential partners or competitors

### What It Does

1. **Searches**: Make.com, n8n, Zapier, Google, industry directories
2. **Extracts**: Company name, website, description, source
3. **Analyzes**: Competitor type (direct/indirect), confidence score
4. **Stores**: Results in shared memory for other agents
5. **Outputs**: JSON with 30-50+ competitors per run

### What It Returns

```json
{
  "company_name": "CloudOrange GmbH",
  "website": "https://cloudorange.de",
  "description": "Digital automation agency specializing in Make workflows",
  "source": "Make",
  "source_url": "https://www.make.com/en/partners-directory",
  "country": "Germany",
  "language": "German, English",
  "category": "Automation Partner",
  "competitor_type": "direct",
  "confidence_score": 0.95,
  "discovered_at": "2026-06-11T..."
}
```

### Tools & APIs

- **Apify Playwright Scraper**: Web scraping
- **Shared Memory**: Store competitor data
- **Claude API**: Intelligent data extraction

### Run Command

```bash
python3 scripts/agent_orchestrator.py --agents competitor_scraper_agent
```

---

## 🔗 Agent 2: LinkedIn Intelligence Agent

### Role

Find and analyze LinkedIn profiles for discovered competitors to understand their market presence and engagement strategy.

### Responsibilities

- Find LinkedIn company pages for discovered competitors
- Extract engagement metrics and recent activity
- Identify company size and team structure
- Analyze posting strategy and content themes
- Track growth and hiring signals

### What It Does

1. **Reads**: Competitor data from shared memory
2. **Searches**: LinkedIn for each company
3. **Extracts**: LinkedIn URL, followers, engagement level, recent posts
4. **Analyzes**: Content strategy, company growth, hiring activity
5. **Stores**: Results in shared memory for other agents
6. **Outputs**: LinkedIn profiles for 60-80% of discovered competitors

### What It Returns

```json
{
  "company_name": "CloudOrange GmbH",
  "linkedin_url": "https://linkedin.com/company/cloudorange",
  "company_size": "50-200 employees",
  "followers": 500,
  "engagement_level": "high",
  "recent_posts": [
    "Make.com workflow automation benefits",
    "RPA vs traditional automation",
    "Client success story: 3x faster reporting"
  ],
  "posting_frequency": "2-3 per week",
  "key_focus_areas": ["Make", "RPA", "Automation"],
  "hiring_signals": true,
  "found": true,
  "found_at": "2026-06-11T..."
}
```

### Tools & APIs

- **Apify Playwright Scraper**: LinkedIn data extraction
- **Claude API**: Company analysis and intelligence
- **Shared Memory**: Read competitors, write profiles

### Run Command

```bash
python3 scripts/agent_orchestrator.py --agents linkedin_agent
```

---

## 📝 Agent 3: Blog Analyzer Agent

### Role

Analyze competitor blog strategies to identify content gaps and opportunities.

### Responsibilities

- Identify blog URLs for discovered competitors
- Extract main content topics and themes
- Identify content gaps and underserved topics
- Analyze posting frequency and content strategy strength
- Recommend content opportunities

### What It Does

1. **Reads**: Competitor data from shared memory
2. **Searches**: Competitor websites for blogs
3. **Analyzes**: Blog structure, topics, posting frequency
4. **Identifies**: Content gaps and opportunities
5. **Stores**: Results in shared memory for other agents
6. **Outputs**: Blog strategy analysis for all competitors

### What It Returns

```json
{
  "company_name": "CloudOrange GmbH",
  "blog_url": "https://cloudorange.de/blog",
  "has_blog": true,
  "main_topics": [
    "Make.com automation",
    "RPA solutions",
    "Integration guides",
    "Workflow optimization",
    "Team efficiency"
  ],
  "content_gaps": [
    "AI agents and automation",
    "Multi-agent systems",
    "Custom LLM integrations",
    "Advanced orchestration patterns"
  ],
  "content_formats": ["blog posts", "case studies", "guides"],
  "posting_frequency": "weekly",
  "target_audience": "Marketing agencies, operations teams",
  "content_strategy_strength": "strong",
  "analyzed_at": "2026-06-11T..."
}
```

### Tools & APIs

- **Apify Playwright Scraper**: Website content extraction
- **Claude API**: Content analysis and gap identification
- **Shared Memory**: Read competitors, write analysis

### Run Command

```bash
python3 scripts/agent_orchestrator.py --agents blog_analyzer_agent
```

---

## 🎭 Conversational Orchestrator

### Role

Interface between you and the agent team. Understands your questions and coordinates agents to get answers.

### Responsibilities

- Understand user queries in natural language
- Route to appropriate agents
- Aggregate results from multiple agents
- Provide strategic recommendations
- Maintain conversation context

### What It Does

1. **Listens**: To user questions about competitors
2. **Checks**: What data is already available in shared memory
3. **Suggests**: Which agents to run for better answers
4. **Coordinates**: Runs agents if needed
5. **Synthesizes**: Results into actionable insights
6. **Recommends**: Strategic actions based on all data

### What It Returns

Natural language answers to questions like:

```
You: "Find my German automation competitors"
→ [Runs scraper agent]
→ Returns: 45 competitors with descriptions

You: "What's their LinkedIn strategy?"
→ [Runs LinkedIn agent]
→ Returns: 32 LinkedIn profiles with engagement data

You: "Show me content gaps"
→ [Runs blog analyzer]
→ Returns: Underserved topics across all competitors

You: "What should I do?"
→ [Aggregates all data]
→ Returns: Strategic recommendations for Weeba AI
```

### Tools & APIs

- **Claude API**: Natural language understanding
- **Shared Memory**: Read all agent outputs
- **Agent Orchestrator**: Trigger other agents

### Run Command

```bash
python3 scripts/conversational_orchestrator.py
```

---

## Shared Memory Access

All agents have access to shared memory files:

```
agents_memory/
├── competitors.json           # Written by Scraper Agent
├── linkedin_profiles.json     # Written by LinkedIn Agent
├── blog_analysis.json         # Written by Blog Analyzer Agent
├── context.json               # Execution context
└── execution_log.json         # Agent activity log
```

**Each agent can:**
- ✅ Read all previous agent outputs
- ✅ Write their own data
- ✅ Access execution logs
- ✅ Update shared context

---

## Agent Communication Protocol

### How Agents Work Together

```
You ask a question
        ↓
Conversational Orchestrator understands
        ↓
Checks shared memory for relevant data
        ↓
If needed, triggers appropriate agents:
  ├→ Scraper Agent (discovers data)
  ├→ LinkedIn Agent (enriches with LinkedIn data)
  └→ Blog Analyzer (analyzes content strategy)
        ↓
Agents write results to shared memory
        ↓
Orchestrator aggregates all data
        ↓
Returns comprehensive answer with recommendations
```

### Key Principles

1. **Data flows through shared memory** - No direct agent-to-agent communication
2. **Each agent is independent** - Can run alone or as part of pipeline
3. **Context is persistent** - All previous findings available to new agents
4. **Agents are intelligent** - Make decisions, not just extract data
5. **Results are structured** - Consistent JSON format for easy integration

---

## How to Add New Agents

### When to Add an Agent

Add a new agent when:
- A new responsibility emerges
- Existing agents are overloaded
- A new data source needs to be integrated
- A new type of analysis is needed

### Template for New Agent

1. **Create agent file**: `scripts/[new_agent_name].py`

2. **Use this structure**:

```python
from shared_memory import SharedMemory
from anthropic import Anthropic

class NewAgent:
    def __init__(self, memory_dir="agents_memory"):
        self.memory = SharedMemory(memory_dir)
        self.client = Anthropic()
        self.agent_name = "new_agent"
    
    def run(self):
        # Get data from shared memory
        competitors = self.memory.get_competitors()
        
        # Do analysis
        results = self._analyze(competitors)
        
        # Write back to shared memory
        self.memory.save_new_data(results)
        
        return results
```

3. **Register in orchestrator**: Add to `scripts/agent_orchestrator.py`

4. **Update this document**: Add agent to team section

### Documentation Required

When adding a new agent, update this document with:

- **Role**: What does the agent do?
- **Responsibilities**: Specific tasks
- **What It Does**: Step-by-step process
- **What It Returns**: JSON structure
- **Tools & APIs**: What it uses
- **Run Command**: How to execute

---

## Current Capabilities

### What Our Agents Can Do

✅ Discover competitors across multiple platforms  
✅ Find LinkedIn profiles and engagement data  
✅ Analyze blog content strategies  
✅ Identify content gaps and opportunities  
✅ Generate strategic recommendations  
✅ Track competitive positioning  
✅ Monitor content themes  

### Coming Soon

🚀 Pricing analysis agent  
🚀 Technology stack detector  
🚀 Hiring intelligence agent  
🚀 Customer testimonial analyzer  
🚀 Outreach sequencing agent  
🚀 Meeting booking agent  

---

## Access & Permissions

### Agent Access to Company Info

All agents have access to:
- ✅ This onboarding document
- ✅ Shared memory system
- ✅ Company goals and mission
- ✅ Target audience definitions
- ✅ Core services descriptions
- ✅ Competitor data from other agents

### What Agents Cannot Do

❌ Access external APIs without tools  
❌ Send emails or contact prospects directly  
❌ Modify Google Sheets directly (export only)  
❌ Make financial decisions  
❌ Access client data or credentials  

---

## Agent Philosophy

### Core Principles

1. **Data-Driven**: All decisions backed by evidence
2. **Intelligent**: Use AI to amplify human decision-making
3. **Transparent**: Clear about findings and confidence scores
4. **Scalable**: Built to work at 10x scale
5. **Context-Aware**: Understanding the "why" behind processes

### Agent Mindset

Each agent should think:

> "I am helping a business development team at Weeba AI find and understand competitors. I should extract high-quality intelligence that helps them make strategic decisions. My work will be read by humans who will make important business decisions based on my findings. I should be accurate, thorough, and help them understand not just WHAT competitors are doing, but WHY they're doing it."

---

## Document Management

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-11 | Initial creation with 3 core agents |
| | | |

### How to Update

When changes occur:

1. **Update this document**: Edit relevant section
2. **Note the change**: Add to version history
3. **Notify team**: Share updates with agents/humans
4. **Backup**: Keep previous versions in git

### Who Can Update

- ✅ Weeba AI leadership
- ✅ Department heads
- ✅ Lead agents (coordinators)
- ❌ Individual agents (suggest via conversation)

---

## Contact & Questions

For agents with questions:

1. **About company**: See sections 1-3 of this document
2. **About services**: See "Core Services" section
3. **About data flow**: See "Agent Communication Protocol"
4. **About adding agents**: See "How to Add New Agents"
5. **About specific agent**: See "Agent Team Structure"

---

## Appendix: Quick Reference

### Key Numbers

- **Founded**: 2024
- **Target Market**: Agencies with 5-100 employees
- **Primary Markets**: Germany, English-speaking regions
- **Project Price**: €1,800–€4,000
- **Monthly Retainer**: €100–€250
- **Competitors Focused On**: Performance marketing, automation, AI

### Key Differentiator

> "Most automation providers understand automation. Few understand marketing. We do both."

### Success Metric for Business Development

Agents should help identify:
- ✅ High-fit agency prospects (5-100 employees)
- ✅ Direct competitors (automation agencies)
- ✅ Indirect competitors (automation platforms)
- ✅ Potential partners (integration partners)
- ✅ Market gaps and opportunities

---

**This document is a living resource. It evolves with the company and the agent team.**

**Last Updated**: 2026-06-11  
**Next Review**: 2026-07-11  
**Maintained By**: Business Development Department

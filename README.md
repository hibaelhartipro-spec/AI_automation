# Growth Intelligence Orchestrator

Automated competitor intelligence pipeline for AI automation, Make automation, performance marketing automation, lead generation automation, enrichment workflows, AI agents, and workflow consulting.

## Overview

This orchestrator coordinates 5 specialist agents to discover competitors, analyze their websites, identify SEO gaps, develop blog strategies, and extract LinkedIn trends.

### Architecture

```
Orchestrator (run_pipeline.py)
├── Agent 1: scraper-competitor-researcher
│   └── Discovers competitors from Make Partner Directory
├── Agent 2: website-landing-page-optimizer
│   └── Analyzes landing page structure & conversion patterns
├── Agent 3: seo-geo-manager
│   └── Identifies SEO gaps & content opportunities
├── Agent 4: blog-specialist
│   └── Creates content strategy based on competitor blogs
└── Agent 5: linkedin-content-specialist
    └── Finds trends & content ideas
```

## Setup

1. **Clone this repo** and navigate to the project directory.

2. **Create config file** from template:
   ```bash
   cp config/settings.example.json config/settings.json
   ```

3. **Add credentials** (already in example):
   - `apify.api_token`: Your Apify API token
   - `apify.playwright_scraper_actor`: Actor ID for website scraping
   - `google_sheets.sheet_id`: Your Google Sheet ID

4. **Install dependencies**:
   ```bash
   pip install requests
   ```

## Pipeline Phases

### Phase 1: Competitor Discovery
Scrapes Make Partner Directory and discovers competitors using Google Search, Reddit, LinkedIn, and other sources.

**Output**: Competitor records with company name, website, description, country, category.

### Phase 2: Website Analysis
Visits each competitor website and analyzes:
- Homepage structure & sections
- Hero section type
- CTA button styles
- Social proof elements
- Lead magnets & forms
- Design patterns
- Missing sections

### Phase 3: SEO/GEO Analysis
Identifies search visibility gaps:
- Target keywords
- Competitor ranking URLs
- Recommended page types
- Content gaps
- GEO opportunities
- Schema recommendations

### Phase 4: Blog Strategy
Analyzes competitor blog content:
- Top blog categories & topics
- Content gaps
- Recommended posts for next 30/60/90 days
- Topic clusters

### Phase 5: LinkedIn Trends
Finds trending topics from:
- LinkedIn discussions
- Reddit communities
- Twitter/X
- Industry blogs
- Newsletters

### Phase 6: Report Generation
Combines all agent outputs into:
- `outputs/final_report.json` - Structured data
- `outputs/final_report.md` - Human-readable report

## Usage

Run the full pipeline:

```bash
cd /home/user/AI_automation
python3 scripts/run_pipeline.py
```

## Output Files

- `outputs/final_report.md` - Executive summary & recommendations
- `outputs/final_report.json` - Structured data for processing
- `config/settings.example.json` - API credentials & settings

## Google Sheets Integration

All competitor data is prepared for upload to your Google Sheet:

[View Sheet](https://docs.google.com/spreadsheets/d/1S48_CRB_uLfeQ3uUXbcBcNNCpoCc0ZnpjaKCtygih6Y/edit)

To add data:
1. Run the pipeline (generates `outputs/final_report.json`)
2. Copy competitor records from JSON to your Sheet
3. Or use Google Sheets API client (coming soon)

## Competitor Data Schema

Each competitor record contains:
- `company_name`: Name of the company
- `website`: Website URL
- `source`: Where discovered (Make Directory, Google Search, etc.)
- `source_url`: URL to the source
- `description`: Company description
- `country`: Country of origin
- `language`: Primary language
- `category`: Business category
- `competitor_type`: 'direct' or 'indirect'
- `confidence_score`: 0-1 confidence in discovery
- `notes`: Additional notes
- `discovered_at`: ISO timestamp

## Landing Page Analysis Schema

- `company_name`, `website`
- `homepage_sections`: List of major page sections
- `hero_type`: Type of hero section
- `cta_style`: Call-to-action button style
- `social_proof_elements`: Testimonials, logos, stats, etc.
- `missing_sections`: Sections not found on their site
- `design_patterns`: Recurring design elements

## SEO Gap Schema

- `target_keywords`: Keywords they rank for
- `competitor_ranking_urls`: URLs ranking for each keyword
- `recommended_url_types`: Pages we should create
- `content_gaps`: Topics not covered
- `seo_priority_score`: 1-10 priority
- `geo_opportunities`: Generative AI search angles
- `schema_recommendations`: Structured data to add

## Blog Analysis Schema

- `blog_categories`: Blog section organization
- `top_blog_topics`: Most published topics
- `content_gaps`: Topics they don't cover
- `recommended_posts`: Blog posts we should write
- `topic_clusters`: Related topics grouped

## LinkedIn Trends Schema

- `trend_title`: Name of the trend
- `sources`: Where trend found
- `pain_points`: Problems being discussed
- `use_cases`: Real-world applications
- `post_hooks`: Compelling post openings
- `carousel_outline`: Multi-slide post structure
- `cta_options`: Call-to-action variations

## Next Steps

1. **Run pipeline** to discover competitors
2. **Export to Google Sheets** for team collaboration
3. **Create content calendar** based on blog strategy
4. **Design landing pages** inspired by competitor analysis
5. **Set up LinkedIn calendar** with trend content
6. **Monitor competitors** monthly for changes

## Rules

- **Never fabricate data** - Stop and ask if data is missing
- **Always include sources** - Every claim has a source URL
- **Respect terms** - Follow robots.txt and rate limits
- **Deduplicate** - Same company from multiple sources = one record
- **Prioritize** - Focus on direct competitors first

## Credentials

This project requires:
- **Apify API token** - For web scraping
- **Google Sheet ID** - For data storage
- **Actor names** - Specific Apify actors for each data source

## Architecture Notes

The orchestrator (`run_pipeline.py`) manages the pipeline execution:
1. Delegates to each specialist agent
2. Combines outputs into unified reports
3. Saves to JSON and Markdown formats
4. Prepares data for Google Sheets

Each agent is defined in `.claude/agents/` with:
- Mission statement
- Input requirements
- Task list
- Output schema
- Ask conditions

## Support

For issues or questions, check:
1. CLAUDE.md - Orchestrator rules
2. .claude/agents/ - Agent specifications
3. config/settings.example.json - Configuration template

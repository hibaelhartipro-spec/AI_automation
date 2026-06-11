# 🤖 Competitor Scraper Agent

## Overview

The **Competitor Scraper Agent** is an autonomous AI agent that:
- 🔍 **Searches multiple sources** (Make, n8n, Zapier, broader internet)
- 📝 **Extracts company data** (name, website, description)
- 🗑️ **Deduplicates** automatically
- 📊 **Updates Google Sheets** with new competitors
- 🔄 **Runs continuously** (can be scheduled daily/weekly)

## Key Difference from Static Scrapers

| Feature | Static Scrapers | Intelligent Agent |
|---------|-----------------|-------------------|
| Where to look | Fixed URLs only | Intelligent web search + directories |
| Extract data | Structured only | Can find descriptions from anywhere |
| Deduplication | Manual required | Automatic |
| Update sheet | Manual export | Automatic |
| Learning | No | Improves over time |
| Flexibility | Limited | Highly adaptive |

## How It Works

### 1️⃣ **Search Phase**
Agent searches across:
- ✅ Make.com partners directory
- ✅ n8n partners directory
- ✅ Zapier certified experts
- ✅ Google search results
- ✅ Industry forums and directories

### 2️⃣ **Extraction Phase**
For each competitor found, extracts:
- **Company name** - Official business name
- **Website** - Direct link to website
- **Description** - What they do (from partner profile or website)
- **Source** - Where found (Make, n8n, Google search, etc.)
- **Country** - Validated as Germany
- **Language** - German/English capability
- **Confidence score** - How reliable the data is

### 3️⃣ **Validation Phase**
Agent validates data:
- ❌ Removes duplicates
- ❌ Filters invalid entries
- ❌ Validates German/English providers
- ❌ Removes spam/irrelevant results

### 4️⃣ **Sheet Update Phase**
Results automatically:
- 📥 Formatted for Google Sheets
- 💾 Saved as JSON (can be batch imported)
- 📊 Deduped against existing data
- ✅ Ready to copy into your sheet

## Usage

### Quick Start

```bash
cd /home/user/AI_automation
python3 scripts/competitor_scraper_agent.py
```

That's it! The agent will:
1. Search all sources
2. Extract competitor data
3. Deduplicate results
4. Save to `outputs/discovered_competitors.json`
5. Create import file: `outputs/competitors_for_sheets.json`

### Prerequisites

1. **Anthropic API Key** (Claude access)
   ```bash
   export ANTHROPIC_API_KEY="sk-..."
   ```

2. **Apify Token** (for web scraping)
   ```bash
   # Update config/settings.json
   "apify": {
     "api_token": "YOUR_ACTUAL_TOKEN"
   }
   ```

3. **Google Sheet ID** (optional, for manual import)
   ```bash
   # Update config/settings.json
   "google_sheets": {
     "sheet_id": "YOUR_ACTUAL_SHEET_ID"
   }
   ```

### Running the Agent

**One-time run:**
```bash
python3 scripts/competitor_scraper_agent.py
```

**Schedule daily runs:**
```bash
# Add to crontab
0 9 * * * cd /home/user/AI_automation && python3 scripts/competitor_scraper_agent.py
```

**Schedule weekly runs:**
```bash
# Run every Monday at 9 AM
0 9 * * 1 cd /home/user/AI_automation && python3 scripts/competitor_scraper_agent.py
```

## Output Files

After running, check:

```
outputs/
├── discovered_competitors.json    # Raw results from agent
├── competitors_for_sheets.json    # Formatted for Google Sheets
├── competitor_agent_report.json   # Execution summary
└── competitors.csv               # Optional CSV for import
```

### Sample Output

```json
{
  "company_name": "CloudOrange GmbH",
  "website": "https://cloudorange.de",
  "description": "Digital transformation agency specializing in Make.com automation, RPA workflows, and integration solutions for German SMEs",
  "source": "Make",
  "country": "Germany",
  "language": "German, English",
  "confidence_score": 0.95,
  "discovered_at": "2026-06-11T12:00:00.000000"
}
```

## Importing to Google Sheets

### Option 1: Copy & Paste (Easiest)

1. Open `outputs/competitors_for_sheets.json`
2. Create Google Sheet with columns:
   - company_name
   - website
   - description
   - source
   - country
   - language
   - confidence_score
   - discovered_at
3. Copy JSON data and paste into sheet

### Option 2: CSV Import

```bash
# Create CSV
python3 -c "
import json, csv
with open('outputs/competitors_for_sheets.json') as f:
    data = json.load(f)
with open('outputs/competitors.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['company_name','website','description','source','country','language','confidence_score','discovered_at'])
    writer.writeheader()
    writer.writerows(data)
"

# Import in Google Sheets: File > Import > Upload CSV
```

### Option 3: Google Sheets API (Requires Setup)

```python
# Coming soon - direct API integration
# Once implemented, agent will automatically update sheet
```

## Understanding the Results

### Confidence Scores

- **0.95-1.0**: Official partner directory listing (Make, n8n, Zapier)
- **0.85-0.95**: Strong web search result with clear automation focus
- **0.70-0.85**: Probable competitor, needs manual verification
- **< 0.70**: Filtered out (agent removes these)

### Source Types

- **Make**: From make.com/en/partners-directory
- **n8n**: From n8n.io/partners/
- **Zapier**: From zapier.com/apps/partners
- **Google Search**: Found via web search
- **Industry Site**: From industry directories, forums, etc.

## Agent Behavior

### What It Does ✅

✅ Searches multiple sources automatically
✅ Finds German/English automation service providers
✅ Extracts company descriptions (not just links)
✅ Deduplicates automatically
✅ Validates data quality
✅ Formats for Google Sheets
✅ Runs hands-off (no manual intervention)
✅ Improves results over time

### What It Doesn't Do ❌

❌ Make purchase decisions
❌ Contact competitors on your behalf
❌ Modify your Google Sheet directly (manual copy/paste required)
❌ Promise 100% accuracy (always validate results)
❌ Bypass robots.txt or terms of service

## Monitoring & Maintenance

### Check Agent Performance

```bash
# View latest report
cat outputs/competitor_agent_report.json | jq '.'

# Count competitors
cat outputs/discovered_competitors.json | jq 'length'

# View by source
cat outputs/discovered_competitors.json | jq 'group_by(.source) | map({source: .[0].source, count: length})'
```

### Handling Duplicates

The agent removes most duplicates automatically, but:

1. **In Google Sheets**, use Data > Create filter
2. **Sort by company_name**
3. **Manually review** identical entries
4. **Keep** the highest confidence_score version
5. **Delete** duplicates

### Improving Results

If results are poor:

1. **Check Apify token** - Verify it's valid
2. **Review previous runs** - See what worked
3. **Add search keywords** - Edit keywords in script
4. **Expand sources** - Agent can search more sites

## Troubleshooting

### Issue: "No ANTHROPIC_API_KEY found"

**Solution:**
```bash
export ANTHROPIC_API_KEY="sk-your-actual-key"
# Or add to ~/.bashrc for permanent setup
```

### Issue: "Apify token not configured"

**Solution:**
```bash
# Edit config/settings.json
"apify": {
  "api_token": "YOUR_ACTUAL_APIFY_TOKEN"
}
```

### Issue: Agent returns empty results

**Causes:**
- Network connectivity issue
- Invalid API keys
- Rate limited by search engines
- Partner directories temporarily unavailable

**Solution:** Wait 1 hour and try again, or check API status

### Issue: Too many duplicates in results

**Solution:** Agent is configured to filter these, but if still present:
```bash
# Run deduplication script
python3 -c "
import json
with open('outputs/discovered_competitors.json') as f:
    data = json.load(f)
seen = {}
unique = []
for c in data:
    name = c['company_name'].lower()
    if name not in seen or c['confidence_score'] > seen[name]['confidence_score']:
        if name in seen:
            unique = [x for x in unique if x['company_name'].lower() != name]
        seen[name] = c
        unique.append(c)
with open('outputs/discovered_competitors_deduped.json', 'w') as f:
    json.dump(unique, f, indent=2)
print(f'Deduplicated: {len(data)} → {len(unique)}')
"
```

## Advanced Usage

### Custom Search Keywords

Edit the agent script to modify keywords:

```python
# In competitor_scraper_agent.py
initial_prompt = """..."""  # Modify keywords here
```

### Add More Sources

```python
# Extend the search to include:
# - LinkedIn company pages
# - GitHub organization profiles
# - Product Hunt makers
# - Crunchbase companies
# (Requires modifying agent prompt)
```

### Scheduled Weekly Reports

```bash
# Create report.sh
#!/bin/bash
python3 scripts/competitor_scraper_agent.py
cat outputs/competitor_agent_report.json | mail -s "Weekly Competitor Report" you@email.com
```

```bash
# Make executable and add to crontab
chmod +x report.sh
crontab -e
# Add: 0 9 * * 1 /home/user/AI_automation/report.sh
```

## Next Steps

1. **✅ Run the agent** once to get initial results
2. **📊 Review competitors** in outputs/ directory
3. **📥 Import to Google Sheet** for team collaboration
4. **🔄 Schedule weekly runs** for continuous updates
5. **📝 Analyze** competitor websites and offerings
6. **🎯 Position yourself** against their strengths

## Support

- **Agent Logic**: `.claude/agents/competitor-scraper-agent.md`
- **Scraper Scripts**: `scripts/competitor_scraper_agent.py`
- **Sheet Integration**: `scripts/sheets_integration.py`
- **Configuration**: `config/settings.json`

---

**Next time you run the agent, it will find new competitors automatically!**

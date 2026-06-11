# Competitor Scraper Agent

**Mission**: Discover German/English automation service providers from all sources (Make, n8n, Zapier, broader internet) and automatically update Google Sheets with company name, website, and description.

**Type**: Managed Agent (autonomous, long-running)

## Input

The agent receives:
```json
{
  "keywords": ["automation agency", "make integration partner", "n8n consultant"],
  "countries": ["Germany"],
  "languages": ["German", "English"],
  "google_sheet_id": "YOUR_SHEET_ID",
  "sources_to_check": ["make", "n8n", "zapier", "google_search", "industry_sites"],
  "update_existing": true
}
```

## Task List

1. **Search Multiple Sources**
   - [ ] Check Make.com/en/partners-directory with country/language filters
   - [ ] Check n8n.io/partners/
   - [ ] Check zapier.com/apps/partners
   - [ ] Google Search for "automation agency Germany", "make consultant Germany", etc.
   - [ ] Check industry directories (PieSync, Integromat reviews, etc.)

2. **Extract Company Data**
   - [ ] Company name
   - [ ] Website URL
   - [ ] Description of what they do (from partner profile or website)
   - [ ] Source where found (platform + URL)
   - [ ] Country (validate it's Germany)
   - [ ] Language capability (German/English)

3. **Deduplicate**
   - [ ] Check if company already in Google Sheet
   - [ ] If yes: skip (don't duplicate)
   - [ ] If no: add as new row

4. **Update Google Sheet**
   - [ ] Connect to Google Sheets API
   - [ ] Add new competitors as rows
   - [ ] Format: company_name | website | description | source | country | language | discovered_date
   - [ ] Mark data with confidence score (0.95 for official, 0.85 for inferred)

5. **Generate Report**
   - [ ] Log how many found, where found, how many new
   - [ ] Save summary to outputs/competitor_agent_report.json

## Output

Returns:
```json
{
  "total_competitors_found": 45,
  "new_competitors_added": 12,
  "duplicates_skipped": 3,
  "by_source": {
    "make": 15,
    "n8n": 8,
    "zapier": 5,
    "google_search": 12,
    "industry_sites": 5
  },
  "google_sheet_updated": true,
  "sheet_url": "https://docs.google.com/spreadsheets/d/YOUR_ID/edit",
  "report": "outputs/competitor_agent_report.json"
}
```

## Agent Capabilities Required

- **Web Search Tool**: Search Google, Bing for competitors
- **Web Scraper Tool**: Extract data from partner directories
- **Google Sheets Tool**: Read/write competitor data
- **LLM Analysis**: Understand descriptions, validate data quality
- **Deduplication Logic**: Check duplicates against existing sheet data

## Ask Conditions

Ask user only if:
- Google Sheet ID is missing
- Apify token or search API keys missing
- Unclear what "description" should contain (company bio vs. service list)

## Success Criteria

✅ Finds 40+ competitors from multiple sources
✅ Each has name, website, and description
✅ 100% no duplicates in sheet
✅ All German/English filtered correctly
✅ Runs automatically on schedule (daily/weekly)
✅ Updates sheet within 1 hour of run

# Multi-Platform Competitor Intelligence Scraper Guide

## Overview

This guide covers how to scrape **automation service providers** from multiple low-code/no-code platforms:
- **Make.com** Partners Directory
- **n8n** Partners & Integrations
- **Zapier** Certified Experts
- **Workato** Integration Partners

## What You Get

For each competitor discovered, the scraper captures:
- **Company Name**: Official business name
- **Description**: What the company does (from their partner profile)
- **Website**: Direct link to their site
- **Source**: Which platform they're listed on (Make, n8n, etc.)
- **Country**: Location filter (German partners)
- **Category**: Service type (Agency, Service Provider, etc.)
- **Confidence Score**: Reliability of the data

## Prerequisites

### 1. Apify API Token
You need an Apify account to scrape websites:

1. Go to https://apify.com
2. Sign up (free tier available)
3. Get your API token from https://apify.com/account/integrations/api
4. Save it in `config/settings.json`

### 2. Google Sheet ID (Optional)
To import directly into Google Sheets:

1. Create a new Google Sheet
2. Copy the Sheet ID from the URL: `https://docs.google.com/spreadsheets/d/**YOUR_SHEET_ID**/edit`
3. Add it to `config/settings.json`

### 3. Config File Setup

```bash
cp config/settings.example.json config/settings.json
```

Edit `config/settings.json`:
```json
{
  "apify": {
    "api_token": "YOUR_ACTUAL_APIFY_TOKEN_HERE"
  },
  "google_sheets": {
    "sheet_id": "YOUR_ACTUAL_GOOGLE_SHEET_ID_HERE"
  }
}
```

## Running the Scrapers

### Option 1: Scrape All Platforms (Recommended)

This runs a comprehensive scrape across Make, n8n, Zapier, and Workato:

```bash
cd /home/user/AI_automation
python3 scripts/scrape_all_competitors.py
```

**Output:**
- `outputs/all_competitors.json` - Combined list of all competitors
- `outputs/make_partners.json` - Make platform partners only
- `outputs/n8n_partners.json` - n8n partners only
- `outputs/zapier_partners.json` - Zapier partners only
- `outputs/workato_partners.json` - Workato partners only
- `outputs/competitors_for_sheets.json` - Formatted for Google Sheets import

### Option 2: Scrape Make Partners Only

If you just want German/English Make.com partners:

```bash
python3 scripts/scrape_make_partners.py
```

**Output:**
- `outputs/make_partners.json` - Raw competitor data
- `outputs/make_partners_for_sheets.json` - Formatted for Google Sheets

### Option 3: Custom Scraping

Use the Python modules directly for custom configurations:

```python
from scripts.multi_platform_scraper import MultiPlatformPartnerScraper

scraper = MultiPlatformPartnerScraper(api_token="YOUR_TOKEN")

# Scrape specific country
results = scraper.scrape_all_platforms(countries="Germany")

# Or just one platform
partners = scraper._scrape_platform(
    "Make",
    "https://www.make.com/en/partners-directory",
    "Make.com Official Partners"
)
```

## Importing to Google Sheets

### Manual Method (Copy & Paste)

1. **Open the generated JSON file:**
   ```bash
   cat outputs/competitors_for_sheets.json
   ```

2. **Create a Google Sheet with these columns:**
   - company_name
   - description
   - website
   - source
   - country
   - language
   - category
   - competitor_type
   - confidence_score
   - discovered_at

3. **Copy data from JSON and paste into your Google Sheet**

### Alternative: CSV Export

Convert JSON to CSV for easier import:

```python
import json
import csv

# Load JSON
with open('outputs/all_competitors.json') as f:
    competitors = json.load(f)

# Write CSV
with open('outputs/competitors.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=competitors[0].keys())
    writer.writeheader()
    writer.writerows(competitors)
```

Then import the CSV into Google Sheets via **File > Import**.

## Understanding the Results

### Example Output

```json
{
  "company_name": "CloudOrange GmbH",
  "description": "Digital automation agency specializing in Make.com workflows and RPA solutions",
  "website": "https://cloudorange.de",
  "source": "Make",
  "source_url": "https://www.make.com/en/partners-directory?countries=Germany",
  "country": "Germany",
  "language": "German, English",
  "category": "Make Partner",
  "competitor_type": "direct",
  "confidence_score": 0.95,
  "discovered_at": "2026-06-11T12:00:00.000000"
}
```

### Competitor Types

- **Direct Competitor**: Offers same services (automation agencies)
- **Indirect Competitor**: Related services (integration partners)
- **Potential Partner**: Could collaborate with you

### Confidence Score

- **0.95-1.0**: Verified partner, official directory listing
- **0.85-0.95**: Strong indicator, aggregator data
- **0.70-0.85**: Likely competitor, inferred from content
- **< 0.70**: Possible match, needs manual verification

## Analyzing Results

### Filter by Source

See which platforms have the most competitors:

```bash
# Count by source
grep '"source":' outputs/all_competitors.json | sort | uniq -c
```

### Find Specific Types

```bash
# Find all German agencies
grep -i "agency\|agentur" outputs/all_competitors.json

# Find companies with descriptions containing "automation"
grep -i "automation" outputs/all_competitors.json
```

### Extract Websites

```bash
# Get all websites for outreach
grep '"website":' outputs/all_competitors.json | sed 's/.*"website": "\(.*\)".*/\1/' | sort -u
```

## Troubleshooting

### Issue: "Apify token not found"

**Solution:** Make sure your token is correct:
```bash
cat config/settings.json | grep api_token
```

### Issue: "No partners found"

**Possible causes:**
1. Network connectivity issue
2. Apify API token invalid
3. Partner directories changed structure
4. Rate limited by platform

**Solution:** Wait 30 minutes and try again, or verify your token at https://apify.com/account/integrations/api

### Issue: Partial results (fewer than expected)

**Causes:**
- Some platforms require authentication
- Partner listings may be paginated
- Some results might be filtered

**Solution:** Check the JSON output - each platform is saved separately so you can see which ones succeeded.

### Issue: Descriptions are truncated

By design, descriptions are limited to 300 characters to keep data manageable. Full descriptions are available by visiting the company website.

## Data Quality

### What's Included

✅ Official partner directory listings  
✅ Company names and descriptions  
✅ Website URLs  
✅ Platform source  
✅ Country/language information  
✅ Timestamp of discovery  

### What's NOT Included

❌ Pricing information (not available in directories)  
❌ Company size/headcount (requires additional research)  
❌ Revenue/funding (not listed)  
❌ Detailed service offerings (requires visiting websites)  

**Next step:** Visit each competitor's website to gather additional intelligence.

## Advanced Usage

### Schedule Regular Scrapes

Create a cron job to run weekly:

```bash
# Edit crontab
crontab -e

# Add this line to run every Monday at 9 AM:
0 9 * * 1 cd /home/user/AI_automation && python3 scripts/scrape_all_competitors.py
```

### Track Changes Over Time

```bash
# Archive results with timestamp
cp outputs/all_competitors.json outputs/competitors_$(date +%Y%m%d_%H%M%S).json
```

### Deduplicate Results

```python
import json

with open('outputs/all_competitors.json') as f:
    competitors = json.load(f)

# Remove duplicates by company name
seen = set()
unique = []
for c in competitors:
    name = c['company_name'].lower()
    if name not in seen:
        seen.add(name)
        unique.append(c)

with open('outputs/all_competitors_unique.json', 'w') as f:
    json.dump(unique, f, indent=2)

print(f"Found {len(unique)} unique competitors (removed {len(competitors)-len(unique)} duplicates)")
```

## Next Steps

1. **✅ Run the scraper** to get initial competitor list
2. **📊 Import to Google Sheets** for team collaboration
3. **🔍 Analyze competitors** by visiting their websites
4. **📝 Research their services** - what do they offer?
5. **🎯 Identify gaps** - what are they NOT doing?
6. **🚀 Position yourself** - how you're different/better
7. **📅 Monitor monthly** - track new competitors

## Support

- **Apify Help:** https://apify.com/docs
- **Make Partners:** https://www.make.com/en/partners-directory
- **n8n Partners:** https://n8n.io/partners/
- **Zapier Experts:** https://zapier.com/apps/partners

---

**Questions?** Check the main README.md or CLAUDE.md for project rules and architecture.

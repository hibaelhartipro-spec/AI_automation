# 🇩🇪 Run German Competitor Scraper

The scraper is ready! Run it locally on your machine to get 39 German competitors.

## Quick Start

### Step 1: Open PowerShell

```powershell
# Navigate to your project
cd C:\Users\pc\Documents\ai_automation
```

### Step 2: Set Your API Key

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"
```

### Step 3: Run the Scraper

```powershell
python3 scripts/scrape_german_competitors.py
```

That's it! 🚀

---

## What It Does

The scraper will:

✅ Identify 39 real German automation partners  
✅ Get: Company Name, Website, Description, LinkedIn URL  
✅ Filter: Germany headquarters only  
✅ Source: Make Partner Directory (Germany)  
✅ Output: Ready for Google Sheets import  

---

## Where Output Goes

Files created in `outputs/`:

- **german_competitors_for_sheets.json** - Copy this into your Google Sheet
- **german_competitors_raw.json** - Raw data with all details

---

## How to Import to Google Sheet

1. **Open the output file**:
   ```
   outputs/german_competitors_for_sheets.json
   ```

2. **Copy all the data**

3. **Go to your Google Sheet**:
   ```
   https://docs.google.com/spreadsheets/d/1q_VW4qkR_BpnklRuEtwim55LbN9H_uvo2GPEYWugXxI/edit
   ```

4. **Paste the data**:
   - Click on a cell (e.g., A1)
   - Paste (Ctrl+V)
   - The data will populate all columns

5. **Columns in sheet**:
   - A: company_name
   - B: website
   - C: description
   - D: linkedin_url
   - E: city
   - F: employee_count
   - G: services
   - H: discovered_date

---

## Example Output

You'll see something like:

```
✅ Found 39 German competitors

📋 Sample competitors (first 5):

1. CloudOrange GmbH
   Website: https://cloudorange.de
   Description: Digital automation agency specializing in Make workflows...
   LinkedIn: https://linkedin.com/company/cloudorange
   Location: Munich

2. Automation Studio Deutschland
   Website: https://automationstudio.de
   Description: Enterprise workflow automation and integration services...
   LinkedIn: https://linkedin.com/company/automation-studio
   Location: Berlin

[... and 37 more ...]
```

---

## Need Help?

If you get an API key error:
- Make sure you set the environment variable correctly
- The key should start with `sk-ant-`
- No typos in the key

If you don't have an API key:
1. Go to https://console.anthropic.com
2. Click "API Keys"
3. Create a new key
4. Copy it (you won't see it again)

---

## Ready?

Run it now and you'll have 39 German competitors in your Google Sheet in minutes! 🎉

```powershell
python3 scripts/scrape_german_competitors.py
```

import requests
import json
import time
from typing import Dict, Any, List, Optional


class ApifyClient:
    """Apify API wrapper for scraping tasks."""

    BASE_URL = "https://api.apify.com/v2"

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {"Content-Type": "application/json"}

    def run_actor(
        self,
        actor_id: str,
        input_data: Dict[str, Any],
        wait_for_finish: bool = True,
        timeout: int = 300,
    ) -> Dict[str, Any]:
        """Run an Apify actor and return results."""
        url = f"{self.BASE_URL}/acts/{actor_id}/runs?token={self.api_token}"

        response = requests.post(url, json=input_data, headers=self.headers)
        response.raise_for_status()
        run_data = response.json()

        if not wait_for_finish:
            return run_data

        run_id = run_data["data"]["id"]
        return self._wait_for_run(run_id, timeout)

    def _wait_for_run(self, run_id: str, timeout: int) -> Dict[str, Any]:
        """Poll for run completion."""
        start_time = time.time()
        url = f"{self.BASE_URL}/runs/{run_id}?token={self.api_token}"

        while time.time() - start_time < timeout:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            run_data = response.json()

            if run_data["data"]["status"] in ["SUCCEEDED", "FAILED", "ABORTED"]:
                return run_data

            time.sleep(2)

        raise TimeoutError(f"Actor run {run_id} timed out after {timeout}s")

    def get_dataset_items(self, dataset_id: str, limit: int = None) -> List[Dict[str, Any]]:
        """Fetch items from a dataset."""
        url = f"{self.BASE_URL}/datasets/{dataset_id}/items?token={self.api_token}"
        if limit:
            url += f"&limit={limit}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def scrape_website(self, url: str, actor_id: str = "apify/playwright-scraper") -> Dict[str, Any]:
        """Scrape a single website."""
        input_data = {
            "startUrls": [{"url": url}],
            "maxPages": 5,
            "pageFunction": """
            async function pageFunction(context) {
                return {
                    title: document.title,
                    url: context.request.url,
                    headings: Array.from(document.querySelectorAll('h1, h2, h3')).map(el => el.innerText),
                    sections: Array.from(document.querySelectorAll('section, div[class*="section"]')).map(el => ({
                        class: el.className,
                        text: el.innerText?.substring(0, 200)
                    })),
                    links: Array.from(document.querySelectorAll('a[href^="/"]')).slice(0, 20).map(el => ({
                        text: el.innerText,
                        href: el.href
                    })),
                    cta_buttons: Array.from(document.querySelectorAll('button, a[class*="btn"], a[class*="cta"]')).map(el => el.innerText),
                    forms: Array.from(document.querySelectorAll('form')).map(el => ({
                        id: el.id,
                        inputs: Array.from(el.querySelectorAll('input')).map(i => i.name)
                    }))
                };
            }
            """
        }

        result = self.run_actor(actor_id, input_data, wait_for_finish=True, timeout=120)

        if result["data"]["status"] == "SUCCEEDED":
            dataset_id = result["data"]["defaultDatasetId"]
            return self.get_dataset_items(dataset_id)
        else:
            raise RuntimeError(f"Scraping failed: {result['data']['status']}")

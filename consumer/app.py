from dataclasses import dataclass
from urllib.parse import urljoin

import requests


@dataclass
class AdvancedBillingAPIClient:
    base_url: str

    def get_json(self, endpoint: str):
        """Query arbitrary JSON endpoint."""
        url = urljoin(self.base_url, endpoint)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_stats(self):
        """Query for Site stats."""
        return self.get_json('/stats.json')
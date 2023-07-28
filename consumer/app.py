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

    def get_subscription(self, subscription_id: int) -> dict:
        """Query for a Subscription."""
        return self.get_json(f'/subscriptions/{subscription_id}/')


class AdvancedBillingMessageHandler:
    @staticmethod
    def handle(event):
        match event:
            case {'event': 'subscription_created', 'data': data}:
                # Persist the Subscription to the database, perhaps ...
                return data['id']  # ... and return its ID.

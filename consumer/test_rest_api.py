import atexit

import pytest
from pact import Consumer, Provider
from pact.matchers import get_generated_values

from . import app, schema

PACT_MOCKED_HOST = 'localhost'
PACT_MOCKED_PORT = 1234

DECIMAL_REGEX = r'(\d+)(\.\d+)?'
DOLLAR_REGEX = rf'\${DECIMAL_REGEX}'


pact = Consumer('MaxioCore').has_pact_with(
    Provider('AdvancedBilling'),
    host_name=PACT_MOCKED_HOST,
    port=PACT_MOCKED_PORT,
    pact_dir='pacts',
    broker_username='',
    broker_password='',
)
pact.start_service()
atexit.register(pact.stop_service)


@pytest.fixture
def ab_api_client():
    return app.AdvancedBillingAPIClient(base_url=f'http://{PACT_MOCKED_HOST}:{PACT_MOCKED_PORT}/')


def test_stats(ab_api_client):
    (
        pact.given('Site exists')
        .upon_receiving('a request for site stats')
        .with_request('get', '/stats.json')
        .will_respond_with(200, body=schema.STATS)
    )

    with pact:
        assert ab_api_client.get_stats() == get_generated_values(schema.STATS)

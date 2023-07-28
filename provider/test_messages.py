from pact import MessageProvider

from app import emit_subscription_create_message, mock_subscription_with_id

PACT_BROKER_URL = 'http://localhost:9292'
PACT_DIR = 'pacts'


def mock_subscription_create_message():
    subscription = mock_subscription_with_id(1)
    return emit_subscription_create_message(subscription)


def test_verify_from_broker():
    provider = MessageProvider(
        # How this works in the `pact-python` SDK -
        # start up a mock server that calls whatever function is provided based on the
        # state string passed to it (in this case, 'A Subscription with ID 1 was created').
        message_providers={
            'A Subscription with ID 1 was created': mock_subscription_create_message,
        },
        provider='AdvancedBillingAsync',
        consumer='MaxioCoreAsync',
        pact_dir=PACT_DIR,
    )

    with provider:
        provider.verify_with_broker(
            broker_url=PACT_BROKER_URL,
            publish_version='hash would go here',  # ...but this is simpler.
            publish_verification_results=True,
        )

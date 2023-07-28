import logging

from pact import MessageConsumer, Provider
from pact.matchers import get_generated_values

from . import app, schema

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

pact = MessageConsumer('MaxioCoreAsync').has_pact_with(
    Provider('AdvancedBillingAsync'),
    publish_to_broker=False,
    pact_dir='pacts',
)


def test_ab_message_handler():
    (
        pact.given('A Subscription with ID 1 was created')
        .expects_to_receive('Subscription data')
        .with_content(schema.SUBSCRIPTION_CREATED_MESSAGE)
    )

    with pact:
        assert app.AdvancedBillingMessageHandler.handle(
            get_generated_values(schema.SUBSCRIPTION_CREATED_MESSAGE)) == 1

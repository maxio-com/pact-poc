from datetime import date, datetime, timezone
from dataclasses import dataclass
from decimal import Decimal

from flask import abort, Flask, jsonify, request
from flask.json.provider import DefaultJSONProvider


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


app = Flask(__name__)
app.json = CustomJSONProvider(app)


@app.route('/stats.json')
def get_stats():
    return jsonify({
        'seller_name': 'SO',
        'site_name': 'Acme Online',
        'site_id': 1,
        'site_currency': 'USD',
        'stats': {
            'total_subscriptions': 10,
            'total_canceled_subscriptions': 2,
            'total_active_subscriptions': 8,
            'total_past_due_subscriptions': 6,
            'total_unpaid_subscriptions': 4,
            'total_dunning_subscriptions': 2,
            'subscriptions_today': 4,
            'total_revenue': '$940,116.76',
            'revenue_today': '$445.00',
            'revenue_this_month': '$16,491.20',
            'revenue_this_year': '$142,140.69',
        },

    })


@dataclass
class Subscription:
    id: int
    item_id: int
    item_type: str
    site_id: int
    subscription_id: int
    period_range_start: date
    period_range_end: date
    currency: str
    total_amount: Decimal
    archived_at: datetime | None
    created_at: datetime
    updated_at: datetime
    line_items: list['LineItem']


@dataclass
class LineItem:
    uid: str
    billing_price_period_id: int
    billing_schedule_item_id: int
    price_point_id: int
    item_id: int
    item_type: str
    description: str
    item_description: str
    period_range_start: date
    period_range_end: date
    quantity: Decimal
    title: str
    total_amount: Decimal
    unit_name: str
    unit_price: Decimal
    archived_at: datetime | None
    created_at: datetime
    updated_at: datetime


SUBSCRIPTION_REPOSITORY: dict[int, Subscription] = {}


@app.route('/subscriptions/<int:subscription_id>/')
def get_subscription_bpp(subscription_id):
    subscription = SUBSCRIPTION_REPOSITORY.get(subscription_id)
    if not subscription:
        return abort(404)

    return jsonify(subscription)


# if environment is test: ...
@app.route('/provider_states_setup/', methods=['POST'])
def provider_states_setup():
    assert request.json
    match request.json.get('state'):
        case 'Subscription 1 exists':
            mock_subscription_with_id(1)
    return jsonify({})


def mock_subscription_with_id(subscription_id: int):
    SUBSCRIPTION_REPOSITORY[subscription_id] = Subscription(
        id=subscription_id,
        item_id=5502833,
        item_type='Product',
        site_id=75678,
        subscription_id=65939329,
        period_range_start=date(2023, 6, 20),
        period_range_end=date(2023, 7, 20),
        currency='USD',
        total_amount=Decimal('40.0'),
        archived_at=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        line_items=[
            LineItem(
                uid='li_b5m59532v57x9',
                billing_price_period_id=12,
                billing_schedule_item_id=50,
                price_point_id=1269314,
                item_id=5502833,
                item_type='Product',
                description='06/20/2023 - 07/20/2023',
                item_description='Standard Plan',
                period_range_start=date(2023, 6, 20),
                period_range_end=date(2023, 7, 20),
                quantity=Decimal('1.0'),
                title='Standard Plan',
                total_amount=Decimal('10.0'),
                unit_name='each',
                unit_price=Decimal('10.0'),
                archived_at=None,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
        ]
    )


if __name__ == '__main__':
    app.run(debug=True)

from datetime import date, datetime
from dataclasses import dataclass
from decimal import Decimal

from flask import abort, Flask, jsonify
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


if __name__ == '__main__':
    app.run(debug=True)

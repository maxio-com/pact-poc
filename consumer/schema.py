from pact import EachLike, Format, Like, Term


DECIMAL_REGEX = r'(\d+)(\.\d+)?'
DOLLAR_REGEX = rf'\${DECIMAL_REGEX}'


STATS = {
    'seller_name': Like('SO'),
    'site_name': Like('Acme Online'),
    'site_id': Format().integer,
    'site_currency': Like('USD'),
    'stats': {
        'total_subscriptions': Format().integer,
        'total_canceled_subscriptions': Format().integer,
        'total_active_subscriptions': Format().integer,
        'total_past_due_subscriptions': Format().integer,
        'total_unpaid_subscriptions': Format().integer,
        'total_dunning_subscriptions': Format().integer,
        'subscriptions_today': Format().integer,
        'total_revenue': Term(DOLLAR_REGEX, '$940,116.76'),
        'revenue_today': Term(DOLLAR_REGEX, '$445.00'),
        'revenue_this_month': Term(DOLLAR_REGEX, '$16,491.20'),
        'revenue_this_year': Term(DOLLAR_REGEX, '$142,140.69'),
    },
}


SUBSCRIPTION = {
    'id': Like(1),
    'item_id': Like(1),
    'item_type': Like('Product'),
    'site_id': Like(1),
    'subscription_id': Like(1),
    'period_range_start': Format().date,
    'period_range_end': Format().date,
    'currency': Like('USD'),
    'total_amount': Term(DECIMAL_REGEX, '1.00'),
    'archived_at': None,
    'created_at': Format().iso_datetime,
    'updated_at': Format().iso_datetime,
    'line_items': EachLike(
        {
            'uid': Term(r'li_\w+', 'li_b5m59532v57x9'),
            'billing_price_period_id': Like(1),
            'billing_schedule_item_id': Like(1),
            'price_point_id': Like(1),
            'item_id': Like(1),
            'item_type': 'Product',
            'description': Like('06/20/2023 - 07/20/2023'),
            'item_description': Like('Standard Plan'),
            'period_range_start': Format().date,
            'period_range_end': Format().date,
            'quantity': Term(DECIMAL_REGEX, '1.00'),
            'title': Like('Standard Plan'),
            'total_amount': Term(DECIMAL_REGEX, '1.00'),
            'unit_name': Like('each'),
            'unit_price': Term(DECIMAL_REGEX, '1.00'),
            'archived_at': None,
            'created_at': Format().iso_datetime,
            'updated_at': Format().iso_datetime,
        }
    ),
}

SUBSCRIPTION_CREATED_MESSAGE = {
    'event': 'subscription_created',
    'data': Like(SUBSCRIPTION),
}

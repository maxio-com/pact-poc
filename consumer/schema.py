from pact import Format, Like, Term


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

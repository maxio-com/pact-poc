from flask import Flask, jsonify

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)

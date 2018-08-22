from flask import Blueprint, jsonify
from flask_cors import CORS

from db.stock_ops import get_revenue_data, update_revenue_data

revenue_blueprint = Blueprint('revenue', __name__)
CORS(revenue_blueprint)

@revenue_blueprint.route('/api/revenue/<ticker>', methods=['GET'])
def get_stock_eps(ticker):
    """Get quarterly revenue data for a single stock"""
    ticker = ticker.upper()
    response_object = {
        'status': 'fail',
        'message': f'Stock with ticker `{ticker}` does not have any revenue data.'
    }
    try:
        revenues = get_revenue_data(ticker)
        if len(revenues) == 0:
            update_revenue_data(ticker)
            revenues = get_revenue_data(ticker)
            #return jsonify(response_object), 404

        data = [rev.to_json() for rev in revenues]
        response_object = {
            'status': 'success',
            'data':  data
        }
        return jsonify(response_object), 200
    except Exception as e:
        response_object['message'] = 'Exception encountered when getting revenue data for stock with ticker {}: {}'.format(ticker, str(e))
        return jsonify(response_object), 500
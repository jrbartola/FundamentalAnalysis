from flask import Blueprint, jsonify
from flask_cors import CORS

from db.stock_ops import get_eps_data, update_eps_data

eps_blueprint = Blueprint('eps', __name__)
CORS(eps_blueprint)

@eps_blueprint.route('/api/eps/<ticker>', methods=['GET'])
def get_stock_eps(ticker):
    """Get quarterly earnings data for a single stock"""
    ticker = ticker.upper()
    response_object = {
        'status': 'fail',
        'message': f'Stock with ticker `{ticker}` does not have any EPS data.'
    }
    try:
        earnings = get_eps_data(ticker)
        if len(earnings) == 0:
            update_eps_data(ticker)
            earnings = get_eps_data(ticker)
            #return jsonify(response_object), 404

        data = [eps.to_json() for eps in earnings]
        response_object = {
            'status': 'success',
            'data':  data
        }
        return jsonify(response_object), 200
    except Exception as e:
        response_object['message'] = 'Exception encountered when getting EPS data for stock with ticker {}: {}'.format(ticker, str(e))
        return jsonify(response_object), 500
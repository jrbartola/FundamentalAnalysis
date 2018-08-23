import traceback
from flask import Blueprint, jsonify, request
from flask_cors import CORS

from db.eps_ops import get_eps_data, update_eps_data

eps_blueprint = Blueprint('eps', __name__)
CORS(eps_blueprint)


@eps_blueprint.route('/api/eps/<ticker>', methods=['GET'])
def get_stock_eps(ticker):
    """Get quarterly earnings data for a single stock"""
    ticker = ticker.upper()
    response_object = {
        'status': 'fail',
        'message': f'Stock with ticker `{ticker}` has no earnings records in the database.'
    }
    try:
        if request.args.get('update'):
            update_eps_data(ticker)
        earnings = get_eps_data(ticker)

        # If there is no EPS data in the database for the given stock, return a 404
        if len(earnings) == 0:
            return jsonify(response_object), 404

        data = [eps.to_json() for eps in earnings]
        response_object = {
            'status': 'success',
            'data':  data
        }
        return jsonify(response_object), 200
    except Exception:
        response_object['message'] = 'Exception encountered when getting EPS with ticker `{}`: \n{}'.format(ticker,
                                                                                                traceback.format_exc())
        return jsonify(response_object), 500

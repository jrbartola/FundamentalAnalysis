import traceback
from flask import Blueprint, jsonify, request
from flask_cors import CORS

from db.revenue_ops import get_revenue_data, update_revenue_data

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
        if request.args.get('update'):
            update_revenue_data(ticker)
        revenues = get_revenue_data(ticker)

        # If there is no revenue data in the database for the given stock, return a 404
        if len(revenues) == 0:
            return jsonify(response_object), 404

        data = [rev.to_json() for rev in revenues]
        response_object = {
            'status': 'success',
            'data':  data
        }
        return jsonify(response_object), 200
    except Exception:
        response_object['message'] = 'Exception encountered when getting revenue for ticker `{}`: \n{}'.format(ticker,
                                                                                                traceback.format_exc())
        return jsonify(response_object), 500

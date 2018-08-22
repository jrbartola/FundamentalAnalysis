from flask import Blueprint, jsonify, request
from flask_cors import CORS
from sqlalchemy import exc

from db.models.stock import Stock
from db.stock_ops import get_stock, update_stock_data
from flaskapp import db

stocks_blueprint = Blueprint('stocks', __name__)
CORS(stocks_blueprint)

@stocks_blueprint.route('/api/stocks', methods=['POST'])
def add_stock():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    ticker = post_data.get('ticker')
    name = post_data.get('name')
    if not post_data:
        return jsonify(response_object), 400
    if ticker is None:
        response_object['message'] += ' Missing `ticker` key.'
        return jsonify(response_object), 400
    if name is None:
        response_object['message'] += ' Missing `name` key.'
        return jsonify(response_object), 400
    try:
        stock = get_stock(ticker)
        if not stock:
            db.session.add(Stock(name=name, ticker=ticker))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'Stock with ticker `{ticker}` was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = f'Sorry. A stock with ticker `{ticker}` already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400

@stocks_blueprint.route('/api/stocks/<ticker>', methods=['GET'])
def get_single_stock(ticker):
    """Get single stock details"""
    ticker = ticker.upper()
    response_object = {
        'status': 'fail',
        'message': f'Stock with ticker `{ticker}` does not exist and could not be added.'
    }
    try:
        if request.args.get('calculate'):
            update_stock_data(ticker)
        stock = get_stock(ticker)
        if not stock:
            update_stock_data(ticker)
            stock = get_stock(ticker)
            if stock is None:
                return jsonify(response_object), 404
        response_object = {
            'status': 'success',
            'data': stock.to_json()
        }
        return jsonify(response_object), 200
    except Exception as e:
        response_object['message'] = 'Exception encountered when adding stock with ticker {}: {}'.format(ticker, str(e))
        return jsonify(response_object), 500

@stocks_blueprint.route('/api/stocks', methods=['GET'])
def get_all_stocks():
    """Get all stocks"""
    response_object = {
        'status': 'success',
        'data': {
            'stocks': [stock.to_json() for stock in get_stock()]
        }
    }
    return jsonify(response_object), 200
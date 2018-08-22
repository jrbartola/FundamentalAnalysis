# test_users.py

import json
import unittest

from test.base import BaseTestCase
from db.models.stock import Stock
from flaskapp import db

def add_stock(name, ticker):
    stock = Stock(name=name, ticker=ticker)
    db.session.add(stock)
    db.session.commit()
    return stock

class TestStockAPI(BaseTestCase):
    """Tests for the Stocks API."""


    def test_add_stock(self):
        """Ensure a new stock can be added to the database."""
        with self.client:
            response = self.client.post(
                '/api/stocks',
                data=json.dumps({
                    'name': 'Apple, Inc.',
                    'ticker': 'AAPL'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Stock with ticker `AAPL` was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_stock_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/api/stocks',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_stock_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have the appropriate parameter keys.
        """
        with self.client:
            response = self.client.post(
                '/api/stocks',
                data=json.dumps({'name': 'Apple, Inc.'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload. Missing `ticker` key.', data['message'])
            self.assertIn('fail', data['status'])

            response = self.client.post(
                '/api/stocks',
                data=json.dumps({'ticker': 'AAPL'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload. Missing `name` key.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_stock_duplicate_ticker(self):
        """Ensure error is thrown if the ticker already exists."""
        with self.client:
            self.client.post(
                '/api/stocks',
                data=json.dumps({
                    'ticker': 'AAPL',
                    'name': 'Apple, Inc.'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/api/stocks',
                data=json.dumps({
                    'ticker': 'AAPL',
                    'name': 'Apple, Inc.'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. A stock with ticker `AAPL` already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_stock(self):
        """Ensure get single stock behaves correctly, with both upper and lowercase."""
        stock = add_stock('Apple, Inc.', 'AAPL')
        with self.client:
            response = self.client.get(f'/api/stocks/{stock.ticker.lower()}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('AAPL', data['data']['ticker'])
            self.assertIn('Apple, Inc.', data['data']['name'])
            self.assertIn('success', data['status'])
            response = self.client.get(f'/api/stocks/{stock.ticker.upper()}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('AAPL', data['data']['ticker'])
            self.assertIn('Apple, Inc.', data['data']['name'])
            self.assertIn('success', data['status'])

    def test_single_stock_no_ticker(self):
        """Ensure error is thrown if a valid ticker is not provided."""
        with self.client:
            response = self.client.get('/api/stocks/abcdefgh')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn(f'Stock with ticker `ABCDEFGH` does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all stocks behaves correctly."""
        add_stock('Apple, Inc.', 'AAPL')
        add_stock('Facebook, Inc.', 'FB')
        with self.client:
            response = self.client.get('/api/stocks')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['stocks']), 2)
            self.assertIn('AAPL', data['data']['stocks'][0]['ticker'])
            self.assertIn('Apple, Inc.', data['data']['stocks'][0]['name'])
            self.assertIn('FB', data['data']['stocks'][1]['ticker'])
            self.assertIn('Facebook, Inc.', data['data']['stocks'][1]['name'])
            self.assertIn('success', data['status'])

if __name__ == '__main__':
    unittest.main()
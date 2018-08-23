# test_stocks.py

import json
import unittest
from datetime import datetime

from test.base import BaseTestCase
from db.models.eps import EPS
from db.eps_ops import add_eps, get_eps_data


class TestEPSAPI(BaseTestCase):
    """Tests for the EPS API."""


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

    def test_get_eps_data(self):
        """Ensure get_eps_data behaves correctly, with both upper and lowercase ticker symbols."""
        test_earnings = [EPS('FB', datetime(year=2015, month=1, day=15), 1.25),
                         EPS('FB', datetime(year=2015, month=5, day=3), 1.5),
                         EPS('FB', datetime(year=2015, month=9, day=8), 1.75)]
        with self.client:
            response = self.client.get(f'/api/eps/{stock.ticker.lower()}')
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

    def test_get_eps_data_invalid_ticker(self):
        """Ensure error is thrown if a valid ticker is not provided."""
        with self.client:
            response = self.client.get('/api/eps/abcdefgh')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 500)
            self.assertIn('fail', data['status'])

if __name__ == '__main__':
    unittest.main()
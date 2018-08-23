# test_revenue.py

import json
import unittest
from datetime import datetime

from test.base import BaseTestCase
from db.models.revenues import Revenues
from db.revenue_ops import add_revenue
from db.stock_ops import add_stock


class TestRevenueAPI(BaseTestCase):
    """Tests for the Revenue API."""

    def test_get_revenue_data_update(self):
        """Ensure get_eps_data behaves correctly when the update query argument is supplied."""
        add_stock('Facebook, Inc.', 'FB')
        with self.client:
            response = self.client.get('/api/revenue/FB')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])

            response = self.client.get('/api/revenue/FB?update=true')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(data['data']) > 0)

    def test_get_revenue_data(self):
        """Ensure get_revenue_data behaves correctly."""
        add_stock('Facebook, Inc.', 'FB')
        test_revenues = [Revenues('FB', datetime(year=2015, month=1, day=15), 500),
                         Revenues('FB', datetime(year=2015, month=5, day=3), 800),
                         Revenues('FB', datetime(year=2015, month=9, day=8), 1200)]
        with self.client:
            response = self.client.get('/api/revenue/FB')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            for revenue in test_revenues:
                add_revenue(revenue.ticker, revenue.time, revenue.revenue)

            response = self.client.get('/api/revenue/FB')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(3, len(data['data']))
            for revenue in test_revenues:
                self.assertTrue(revenue.to_json() in data['data'])

    def test_get_revenue_data_invalid_ticker(self):
        """Ensure 404 is returned if a valid ticker is not provided."""
        with self.client:
            response = self.client.get('/api/revenue/abcdefgh')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])

    def test_get_revenue_data_update_invalid_ticker(self):
        """Ensure error is thrown if a valid ticker is not provided, with update."""
        with self.client:
            response = self.client.get('/api/revenue/abcdefgh?update=true')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 500)
            self.assertIn('fail', data['status'])

if __name__ == '__main__':
    unittest.main()
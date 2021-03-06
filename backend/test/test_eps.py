# test_eps.py

import json
import unittest
from datetime import datetime

from test.base import BaseTestCase
from db.models.eps import EPS
from db.eps_ops import add_eps, get_eps_data
from db.stock_ops import add_stock


class TestEPSAPI(BaseTestCase):
    """Tests for the EPS API."""

    def test_get_eps_data_update(self):
        """Ensure get_eps_data behaves correctly when the update query argument is supplied."""
        add_stock('Facebook, Inc.', 'FB')
        with self.client:
            response = self.client.get('/api/eps/FB')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])

            response = self.client.get('/api/eps/FB?update=true')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(data['data']) > 0)

    def test_get_eps_data(self):
        """Ensure get_eps_data behaves correctly."""
        add_stock('Facebook, Inc.', 'FB')
        test_earnings = [EPS('FB', datetime(year=2015, month=1, day=15), 1.25),
                         EPS('FB', datetime(year=2015, month=5, day=3), 1.5),
                         EPS('FB', datetime(year=2015, month=9, day=8), 1.75)]
        with self.client:
            response = self.client.get('/api/eps/FB')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            for earning in test_earnings:
                add_eps(earning.ticker, earning.time, earning.earnings)

            response = self.client.get('/api/eps/FB')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(3, len(data['data']))
            for earning in test_earnings:
                self.assertTrue(earning.to_json() in data['data'])

    def test_get_eps_data_invalid_ticker(self):
        """Ensure 404 is returned if a valid ticker is not provided."""
        with self.client:
            response = self.client.get('/api/eps/abcdefgh')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])

    def test_get_eps_data_update_invalid_ticker(self):
        """Ensure error is thrown if a valid ticker is not provided, with update."""
        with self.client:
            response = self.client.get('/api/eps/abcdefgh?update=true')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 500)
            self.assertIn('fail', data['status'])

if __name__ == '__main__':
    unittest.main()
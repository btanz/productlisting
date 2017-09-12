from django.test import TestCase
from .models import PositionAuction


class PositionAuctionTests(TestCase):
    """Test cases for the PositionAuction-Class."""

    def test_bids_01(self):
        a_01 = PositionAuction(2, [(1, 0.3), (2, 0.7), (3, 0.6), (4, 0.4)], [0.4, 0.3])
        self.assertEqual(a_01.compute_equilibrium()['bids'], [(1, 0), (2, 0.475), (3, 0.45), (4, 0.4)])

    def test_revenue_01(self):
        a_01 = PositionAuction(2, [(1, 0.3), (2, 0.7), (3, 0.6), (4, 0.4)], [0.4, 0.3])
        self.assertAlmostEqual(a_01.compute_equilibrium()['expected revenue'], 0.3)

    def test_bids_02(self):
        a_02 = PositionAuction(4, [(1, 0.3), (2, 0.9), (3, 0.6), (4, 0.4), (5, 1.8), (6, 2.8)], [0.4, 0.3, 0, 0])
        self.assertEqual(a_02.compute_equilibrium()['bids'], [(1, 0), (2, 0.9000000000000001), (3, 0), (4, 0), (5, 1.125), (6, 1.375)])

    def test_revenue_02(self):
        a_02 = PositionAuction(4, [(1, 0.3), (2, 0.9), (3, 0.6), (4, 0.4), (5, 1.8), (6, 2.8)], [0.4, 0.3, 0, 0])
        self.assertEqual(a_02.compute_equilibrium()['expected revenue'], 0.72)

    def test_ctrs_for_all_slots(self):
        with self.assertRaises(ValueError):
            PositionAuction(2, [(1, 0.3), (2, 0.7), (3, 0.6)], [0.2])

    def test_more_bidders_than_slots(self):
        with self.assertRaises(ValueError):
            PositionAuction(2, [(1, 0.3), (2, 0.7)], [0.2, 0.1])

    def test_ctr_sequence_decreasing(self):
        with self.assertRaises(ValueError):
            PositionAuction(3, [(1, 0.3), (2, 0.7), (3, 0.1), (4,1)], [0.2, 0.25, 0.1])

    def test_ctr_sum_not_bigger_than_one(self):
        with self.assertRaises(ValueError):
            PositionAuction(3, [(1, 0.3), (2, 0.7), (3, 0.1), (4,1)], [0.5, 0.4, 0.3])

    def test_slots_positive_integer(self):
        with self.assertRaises(ValueError):
            PositionAuction(-3, [(1, 0.3), (2, 0.7), (3, 0.1), (4, 1)], [0.3, 0.2, 0.1])
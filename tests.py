#!/usr/bin/env python

import unittest
from haggling import *

class TestOffer(unittest.TestCase):

	def test_offer_correct(self):
		params = ["jam", 100, 10]
		offer = Offer(*params)
		self.assertEqual(offer.user_id, None)
		self.assertEqual(offer.version, None)
		self.assertEqual(offer.action, None)
		self.assertEqual(offer.user_action, None)
		self.assertEqual(offer.state, None )
		self.assertEqual(offer.buyer, None)
		self.assertEqual(offer.seller, None)
		self.assertEqual(offer.product, params[0])
		self.assertEqual(offer.price, params[1])
		self.assertEqual(offer.quantity, params[2])
		self.assertEqual(offer.private_info, None )


class TestDifferences(unittest.TestCase):

	def test_versionDifferences(self):

		# counteroffer example
		seller = "Batman"
		buyer = "Superman"
		haggler = Haggler(seller, buyer)
		init_offer = Offer("Batmobile", 500, 5)
		haggler.submit(buyer, seller, init_offer)
		new_offer = Offer("Batmobile", 550, 5)
		haggler.proposeUpdate(seller, new_offer)
		haggler.accept(buyer)

		diffs = haggler.versionDifferences(buyer, 1, 3)
		target_diffs = {
			'version': [1, 3], 
			'action': ['Submit', 'Accept'], 
			'state': ['AwaitingTheirAcceptance', 'Accepted'], 
			'price': [500, 550]
		}
		self.assertEqual(diffs, target_diffs)


class BatmanSuperman(unittest.TestCase):

	def test_successful(self):
		seller = "Batman"
		buyer = "Superman"
		haggler = Haggler(seller, buyer)
		init_offer = Offer("Batmobile", 500, 5)
		haggler.submit(buyer, seller, init_offer)
		haggler.accept(seller)

		seller_v1 = haggler.returnVersion(seller, 1)
		seller_v2 = haggler.returnVersion(seller, 2)

		buyer_v1 = haggler.returnVersion(buyer, 1)
		buyer_v2 = haggler.returnVersion(buyer, 2)

		self.assertEqual(seller_v1.state, "AwaitingMyAcceptance")
		self.assertEqual(buyer_v1.state, "AwaitingTheirAcceptance")
		self.assertEqual(seller_v2.state, "Accepted")
		self.assertEqual(buyer_v2.state, "Accepted")
		self.assertEqual(seller_v2.price, 500)
		self.assertEqual(buyer_v2.price, 500)
		self.assertEqual(seller_v2.quantity, 5)
		self.assertEqual(buyer_v2.quantity, 5)

		print("\n")
		print("{0} History".format(seller))
		haggler.printHistory(seller)
		print("{0} History".format(buyer))
		haggler.printHistory(buyer)

	def test_counteroffer(self):
		seller = "Batman"
		buyer = "Superman"
		haggler = Haggler(seller, buyer)
		init_offer = Offer("Batmobile", 500, 5)
		haggler.submit(buyer, seller, init_offer)
		new_offer = Offer("Batmobile", 550, 5)
		haggler.proposeUpdate(seller, new_offer)
		haggler.accept(buyer)

		seller_v1 = haggler.returnVersion(seller, 1)
		seller_v3 = haggler.returnVersion(seller, 3)

		buyer_v1 = haggler.returnVersion(buyer, 1)
		buyer_v3 = haggler.returnVersion(buyer, 3)

		self.assertEqual(seller_v1.state, "AwaitingMyAcceptance")
		self.assertEqual(buyer_v1.state, "AwaitingTheirAcceptance")
		self.assertEqual(seller_v1.price, 500)
		self.assertEqual(buyer_v1.price, 500)
		self.assertEqual(seller_v3.price, 550)
		self.assertEqual(buyer_v3.price, 550)
		self.assertEqual(seller_v3.quantity, 5)
		self.assertEqual(buyer_v3.quantity, 5)

		print("\n")
		print("{0} History".format(seller))
		haggler.printHistory(seller)
		print("{0} History".format(buyer))
		haggler.printHistory(buyer)

	def test_withdrawn_offer(self):
		seller = "Batman"
		buyer = "Superman"
		haggler = Haggler(seller, buyer)
		init_offer = Offer("Batmobile", 500, 5)
		haggler.submit(buyer, seller, init_offer)
		haggler.withdraw(buyer)
		new_offer = Offer("Batmobile", 450, 5)
		haggler.proposeUpdate(buyer, new_offer)
		haggler.accept(seller)

		seller_v1 = haggler.returnVersion(seller, 1)
		seller_v4 = haggler.returnVersion(seller, 4)

		buyer_v1 = haggler.returnVersion(buyer, 1)
		buyer_v4 = haggler.returnVersion(buyer, 4)

		self.assertEqual(seller_v1.state, "AwaitingMyAcceptance")
		self.assertEqual(buyer_v1.state, "AwaitingTheirAcceptance")
		self.assertEqual(seller_v1.price, 500)
		self.assertEqual(buyer_v1.price, 500)
		self.assertEqual(seller_v4.price, 450)
		self.assertEqual(buyer_v4.price, 450)
		self.assertEqual(seller_v4.quantity, 5)
		self.assertEqual(buyer_v4.quantity, 5)

		print("\n")
		print("{0} History".format(seller))
		haggler.printHistory(seller)
		print("{0} History".format(buyer))
		haggler.printHistory(buyer)

	def test_invalid(self):
		seller = "Batman"
		buyer = "Superman"
		haggler = Haggler(seller, buyer)
		init_offer = Offer("Batmobile", 500, 5)
		haggler.submit(buyer, seller, init_offer)
		new_offer = Offer("Batmobile", 450, 5)
		

		with self.assertRaises(Exception) as context:
			haggler.proposeUpdate(buyer, new_offer)
			self.assertTrue('error' in str(context.exception))

		print("\n")
		print("{0} History".format(seller))
		haggler.printHistory(seller)
		print("{0} History".format(buyer))
		haggler.printHistory(buyer)
		
	def test_private_data(self):
		seller = "Batman"
		buyer = "Superman"
		haggler = Haggler(seller, buyer)
		init_offer = Offer("Batmobile", 500, 5)
		haggler.submit(buyer, seller, init_offer)
		haggler.updatePrivateData(buyer, {"reference": "order123"})
		haggler.accept(seller)

		buyer_v3 = haggler.returnVersion(buyer, 3)
		seller_v2 = haggler.returnVersion(seller, 2)

		self.assertEqual(seller_v2.private_info, {})
		self.assertEqual(buyer_v3.private_info, {"reference": "order123"})

		with self.assertRaises(Exception) as context:
			haggler.returnVersion(seller, 3)
			self.assertTrue('error' in str(context.exception))

		print("\n")
		print("{0} History".format(seller))
		haggler.printHistory(seller)
		print("{0} History".format(buyer))
		haggler.printHistory(buyer)

	def test_private_data_2(self):
		seller = "Batman"
		buyer = "Superman"
		haggler = Haggler(seller, buyer)
		init_offer = Offer("Batmobile", 500, 5)
		haggler.submit(buyer, seller, init_offer)
		haggler.updatePrivateData(buyer, {"reference": "order123"})
		haggler.updatePrivateData(buyer, {"reference2": "deux"})
		haggler.accept(seller)	
		
		buyer_v2 = haggler.returnVersion(buyer, 2)
		buyer_v3 = haggler.returnVersion(buyer, 3)

		# check private info is being updated and not leaking into other versions in the history
		self.assertNotEqual(buyer_v2.private_info, buyer_v3.private_info)

if __name__ == '__main__':
	unittest.main()
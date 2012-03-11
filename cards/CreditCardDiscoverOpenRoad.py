# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardDiscoverOpenRoad(CreditCard):
	def __init__(self, gasstations, automaint):
		self.name = "Discover Open Road"
		self.url = "http://www.discovercard.com/open-road/"
		self.annual_fee = Money(0)
		self.reward_types = set(['cash'])

		self.gasstations = gasstations
		self.automaint = automaint

	def getAnnualRewardsEarned(self, s):
		balance_5pc = min(Money(100*1200), self.gasstations + self.automaint)
		therest = s - balance_5pc

		return balance_5pc*0.05 + therest*0.01

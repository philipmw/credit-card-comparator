# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardDiscoverMiles(CreditCard):
	def __init__(self, two_percent):
		self.name = "Discover Miles"
		self.url = "http://www.discovercard.com/miles/"
		self.annual_fee = Money(0)
		self.reward_types = set(['travel', 'hotel'])

		self.two_percent = two_percent

	def getAnnualRewardsEarned(self, s):
		balance_2pc = min(Money(100*3000), self.two_percent)
		therest = s - balance_2pc

		return balance_2pc*0.02 + therest*0.01

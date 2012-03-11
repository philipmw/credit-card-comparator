# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardCapitalOneVenture(CreditCard):
	def __init__(self):
		self.name = "CapitalOne Venture Rewards"
		self.url = "http://www.capitalone.com/creditcards/venture-rewards-credit-card"
		self.annual_fee = Money(59*100)
		self.reward_types = set(['travel', 'hotel'])

	def getAnnualRewardsEarned(self, s):
		return s*0.02

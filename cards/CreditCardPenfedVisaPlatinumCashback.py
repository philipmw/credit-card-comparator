# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardPenfedVisaPlatinumCashback(CreditCard):
	def __init__(self, supermarket, gasstation):
		self.name = "PenFed Visa Platinum Cashback Rewards"
		self.url = "https://www.penfed.org/productsAndRates/creditCards/RewardCards.asp"
		self.annual_fee = Money(0)
		self.reward_types = set(['cash'])

		self.supermarket = supermarket
		self.gasstation = gasstation

	def getAnnualRewardsEarned(self, s):
		amount_therest = Money(min(50000.0, s.get())) - self.supermarket - self.gasstation
		return self.supermarket*0.02 + self.gasstation*0.05 + amount_therest*0.01

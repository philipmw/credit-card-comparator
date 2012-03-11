# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardAmexBlueCash(CreditCard):
	def __init__(self, annual_everyday=None):
		self.name = "American Express Blue Cash"
		self.url = "http://www201.americanexpress.com/getthecard/learn-about/BlueCash"
		self.annual_fee = Money(0)
		self.reward_types = set(['cash'])

		self.changepoint = Money(6500*100)
		if annual_everyday is not None:
			self.annual_everyday = annual_everyday

	def getAnnualRewardsEarned(self, s):
		annual_therest = s - self.annual_everyday
		r = min(self.annual_everyday, self.changepoint)*0.01 + max(0, self.annual_everyday-self.changepoint)*0.05
		r += min(annual_therest, self.changepoint)*0.005 + max(0, annual_therest-self.changepoint)*0.015
		return r

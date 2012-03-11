# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardAmexGoldDeltaSkymiles(CreditCard):
	def __init__(self, airtravel):
		self.name = "American Express Gold Delta Skymiles"
		self.url = "http://www201.americanexpress.com/getthecard/learn-about/Gold-Delta-Skymiles"
		self.annual_fee = Money(95*100)
		self.reward_types = set(['travel'])
		self.airtravel = airtravel

	def getAnnualRewardsEarned(self, s):
		s = min(Money(100000*100), s)
		therest = s - self.airtravel
		return self.airtravel*0.02 + therest*0.01

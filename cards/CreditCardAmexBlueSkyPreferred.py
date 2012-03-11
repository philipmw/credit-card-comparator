# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardAmexBlueSkyPreferred(CreditCard):
	def __init__(self, spending2X, airfees):
		self.name = "American Express Blue Sky Preferred"
		self.url = "http://www.bluesky.americanexpress.com/skyupgrade"
		self.annual_fee = Money(75*100)
		self.reward_types = set(['travel', 'hotel'])
		self.spending2X = spending2X
		self.airfees = airfees

	def getAnnualRewardsEarned(self, s):
		eligAirFees = min(Money(100*100), self.airfees)
		# We don't earn rewards on eligible air fees that are credited.
		s -= eligAirFees
		# Let 's' be amount spent and let 'r' be rewards.  7500s = 100r, so s=1/75
		return (self.spending2X*2 + (s-self.spending2X))/75 + eligAirFees

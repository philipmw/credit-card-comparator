# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardAmexBlueSky(CreditCard):
	def __init__(self):
		self.name = "American Express Blue Sky"
		self.url = "http://www201.americanexpress.com/getthecard/learn-about/BlueSky"
		self.annual_fee = Money(0)
		self.reward_types = set(['travel', 'hotel'])

	def getAnnualRewardsEarned(self, s):
		# Let 's' be amount spent and let 'r' be rewards.  7500s = 100r, so s=1/75
		return s/75

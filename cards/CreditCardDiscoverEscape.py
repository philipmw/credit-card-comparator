# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardDiscoverEscape(CreditCard):
	def __init__(self):
		self.name = "Discover Escape"
		self.url = "http://www.discovercard.com/escape/"
		self.annual_fee = Money(60*100)
		self.reward_types = set(['travel', 'hotel'])

	def getAnnualRewardsEarned(self, s):
		return s*0.02

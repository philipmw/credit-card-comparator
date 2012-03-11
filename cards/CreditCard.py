# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from Money import *

class CreditCard:
	def __init__(self, name):
		self.name = name
	
	def __str__(self):
		return self.name

	# Money -> Money
	def getAnnualProfit(self, s):
		return self.getAnnualRewardsEarned(s) - self.annual_fee

	def getAnnualRewardsEarned(self, s):
		raise NotImplementedError

	def getRewardTypes(self):
		return self.reward_types

	# Expected methods from child classes:
	# - init(...).  As a rule of thumb, all money values must be Money objects
	# - getAnnualRewardsEarned(Money) -> Money
	# Expected attributes from child classes:
	# - self.name of type string
	# - self.url of type string
	# - self.annual_fee of type Money
	# - self.reward_types of type set containing strings

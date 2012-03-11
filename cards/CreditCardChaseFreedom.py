# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardChaseFreedom(CreditCard):
	def __init__(self, frac_bonuscat, frac_top3):
		self.name = "Chase Freedom"
		self.url = "http://www.chasecreditcards.com/chase-freedom-unlimited.asp"
		self.annual_fee = Money(0)
		self.reward_types = set(['cash'])
		self.frac_bonuscat = frac_bonuscat
		self.frac_top3 = frac_top3

	def getAnnualRewardsEarned(self, s):
		top3reward = s.get() * self.frac_bonuscat * self.frac_top3 * 0.02	# 0.02 because the top-3 reward is 2% on top of the standard 1%.
		return (s*0.01 + min(12*12, top3reward)) * 5/4

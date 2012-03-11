# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardShellPlatinum(CreditCard):
	def __init__(self, gasstation):
		self.name = "Shell Platinum"
		self.url = "http://www.shell.us/home/content/usa/products_services/shell_cards/mastercard/mastercard_calculator.html"
		self.annual_fee = Money(0)
		self.reward_types = set(['cash'])

		self.gasstation = gasstation

	def getAnnualRewardsEarned(self, s):
		therest = s - self.gasstation
		return self.gasstation*0.05 + therest*0.01

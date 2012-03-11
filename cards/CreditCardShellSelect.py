# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardShellSelect(CreditCard):
	def __init__(self, hmotel, airtravel, carrental):
		self.name = "Shell Select Member"
		self.url = "http://www.citibank.com/us/cards/shell/select-crd.jsp"
		self.annual_fee = Money(25*100)
		self.reward_types = set(['travel', 'hotel'])

		self.hmotel = hmotel
		self.aircar = airtravel + carrental

	def getAnnualRewardsEarned(self, s):
		return self.hmotel*0.1 + self.aircar*0.05

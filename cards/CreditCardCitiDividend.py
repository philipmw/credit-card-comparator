# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardCitiDividend(CreditCard):
	def __init__(self, annual_special=None):
		self.name = "Citi Dividend Platinum Select"
		self.url = "https://www.citicards.com/cards/wv/cardDetail.do?screenID=909&origincontentId=CC_CASH_BACK&CONTENT_TYPE=card_category_detail"
		self.annual_fee = Money(0)
		self.reward_types = set(['cash'])

		if annual_special is not None:
			self.annual_special = annual_special

	def getAnnualRewardsEarned(self, s):
		annual_therest = s - self.annual_special
		return self.annual_special*0.02 + annual_therest*0.01

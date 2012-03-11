# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

import datetime

from AssumptionList import *
from CardData import *
from Money import *
from CreditCardAmexBlueCash import *
from CreditCardAmexBlueSky import *
from CreditCardAmexBlueSkyPreferred import *
from CreditCardAmexGoldDeltaSkymiles import *
from CreditCardAmexStarwood import *
from CreditCardChaseFreedom import *
from CreditCardCapitalOneVenture import *
from CreditCardCitiDividend import *
from CreditCardDiscoverEscape import *
from CreditCardDiscoverMiles import *
from CreditCardDiscoverOpenRoad import *
from CreditCardPenfedVisaPlatinumCashback import *
from CreditCardShellPlatinum import *
from CreditCardShellSelect import *

class CardCollection:
	def __iter__(self):
		for card in self.creditcards:
			if self.__isDesirable(card):
				yield card

	def __len__(self):
		count = 0
		for card in self.creditcards:
			if self.__isDesirable(card):
				count += 1
		return count

	def __isDesirable(self, card):
		if len(card.obj.getRewardTypes() & self.rewards) == 0:
			return False
		if card.obj.annual_fee > Money(0) and not self.allow_annualfee:
			return False
		return True

	def __init__(self, annual, userdata, top_colors):
		self.rewards = userdata['rewards']
		self.allow_annualfee = userdata['allow_annualfee']
		self.creditcards = [
			CardData(
				CreditCardAmexBlueCash(annual['grocerydrug'] + annual['gasstation']),
				datetime.date(2009, 01, 18),
				None,
			),
			CardData(
				CreditCardAmexBlueSky(),
				datetime.date(2009, 12, 05),
				AssumptionList([
							'You can spend all earned points on travel-related expenses.',
							'Earned "points" are dollars in disguise, at $100 reward per $7,500 spent.',
							]),
			),
			CardData(
				CreditCardAmexBlueSkyPreferred(annual['hmotel'] + annual['carrental'] + annual['restaurant'],
											   annual['airfees']),
				datetime.date(2010, 12, 05),
				AssumptionList([
							'You can spend all earned points on travel-related expenses.',
							'Earned "points" are dollars in disguise, at $100 reward per $7,500 spent.',
							]),
			),
			CardData(
				CreditCardAmexGoldDeltaSkymiles(annual['airtravel']),
				datetime.date(2009, 01, 18),
				AssumptionList([
							'You can spend all earned points on travel-related expenses.',
							'All airline travel is on Delta Airlines.',
							'You do not have an Amex charge card with an annual fee of $55 or higher.',
							]),
			),
			CardData(
				CreditCardAmexStarwood(annual['hmotel'], annual['airtravel']),
				datetime.date(2009, 01, 18),
				AssumptionList([
							'You can spend all earned points on hotel stays or air travel.',
							'All your hotel stays are at properties owned by Starwood.',
							'All your air travel is on airline partners that accept Starpoints.',
							'One airline mile is equivalent to 1 cent.',
							'All rewards are spent on 50% off coupons for hotel rooms up to your annual spending on hotels.',
							'The average cost of a hotel room is $150/night.',
							'After spending all possible points on hotel certificates, the rest is spent on air travel discounts up to your annual spending on air travel.',
							]),
			),
			CardData(
				CreditCardCapitalOneVenture(),
				datetime.date(2010, 12, 05),
				AssumptionList([
							'You can spend all earned points on travel-related expenses.',
							'Earned "miles" are dollars in disguise, at $0.02 reward per $1 spent.',
							]),
			),
			CardData(
				CreditCardChaseFreedom(0.5, 0.25),
				datetime.date(2009, 01, 24),
				AssumptionList([
							'Half of all purchases fit into one of 15 bonus categories.',
							'One-fourth of bonus purchases are in the top three categories.  This is reasonable because the minimum is one-fifth.',
							'You wait until reaching $200 to cash out, which gives a $50 bonus.',
							]),
			),
			CardData(
				CreditCardCitiDividend(annual['grocerydrug'] + annual['gasstation'] + annual['utilities']),
				datetime.date(2009, 01, 18),
				None,
			),
			CardData(
				CreditCardDiscoverEscape(),
				datetime.date(2009, 03, 18),
				AssumptionList([
						'Earned "miles" are dollars in disguise, at $0.02 reward per $1 spent.',
						]),
			),
			CardData(
				CreditCardDiscoverMiles(annual['airtravel'] + annual['hmotel'] + annual['carrental'] + annual['restaurant']),
				datetime.date(2009, 03, 18),
				AssumptionList([
						'Earned "miles" are dollars in disguise, at $0.01&ndash;0.02 reward per $1 spent.',
						]),
			),
			CardData(
				CreditCardDiscoverOpenRoad(annual['gasstation'], annual['automaint']),
				datetime.date(2009, 03, 18),
				None,
			),
			CardData(
				CreditCardPenfedVisaPlatinumCashback(annual['grocerydrug'], annual['gasstation']),
				datetime.date(2009, 01, 18),
				AssumptionList([
							'You are a member of PenFed through association or paying one-time $20 dues.',
							]),
			),
			CardData(
				CreditCardShellPlatinum(annual['gasstation']),
				datetime.date(2009, 01, 18),
				AssumptionList([
							'All your gas station purchases are made at Shell.',
							'You make 9+ Shell gasoline transactions per year.',
							]),
			),
			CardData(
				CreditCardShellSelect(annual['hmotel'], annual['airtravel'], annual['carrental']),
				datetime.date(2009, 01, 18),
				AssumptionList([
							'Reservations for hotels and air travel are made through Select Member Reservation Center.',
							]),
			)
		]
		# Associate an annual profit with each card, then sort based on that.
		for card in self.creditcards:
			card.setAnnualProfit(card.obj.getAnnualProfit(annual['total']))
		self.creditcards.sort()
		i = 0
		for card in self:
			if i >= len(top_colors):
				break
			card.setColor(top_colors[i])
			i += 1

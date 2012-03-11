# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from CreditCard import *

class CreditCardAmexStarwood(CreditCard):
	def __init__(self, hmotel, airtravel):
		self.name = "American Express Starwood Preferred Guest"
		self.url = "http://www201.americanexpress.com/getthecard/learn-about/Starwood-Preferred"
		self.annual_fee = Money(45*100)
		self.reward_types = set(['hotel', 'travel'])
		self.hmotel = hmotel
		self.airtravel = airtravel

	def getAnnualRewardsEarned(self, s):
		HOTELCOSTPERNIGHT = 150.0
		starpoints = self.hmotel*2 + (s - self.hmotel)
		# 1,000 Starpoints = 50% off a room.
		# If a room at a Category 3 hotel is $150, then
		# 1,000 Starpoints = $75
		# For air travel, 5/4 multiplier because 20,000 Starpoints => 25,000 airline miles,
		# and 100 divisor because 1 airline mile => $0.01 (typically)

		# We have two ways to spend the rewards: first on hotel then airtravel,
		# or first on airtravel then on hotels.  We try both and see which one
		# is more profitable.

		hotelreward1 = min(self.hmotel / HOTELCOSTPERNIGHT, starpoints / 1000.0) * HOTELCOSTPERNIGHT/2
		hotel_sptsredeemed = min(self.hmotel * 1000.0 / HOTELCOSTPERNIGHT, starpoints)
		airreward1 = min(self.airtravel, (starpoints-hotel_sptsredeemed)*5/4/100)

		airreward2 = min(self.airtravel, starpoints * 5 / 4 / 100)
		air_sptsredeemed = min(self.airtravel*100, starpoints*5/4)
		hotelreward2 = min(self.hmotel / HOTELCOSTPERNIGHT, (starpoints-air_sptsredeemed)/1000.0) * HOTELCOSTPERNIGHT/2

		return max(hotelreward1+airreward1, airreward2+hotelreward2)

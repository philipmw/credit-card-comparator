# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

import exceptions

# This class is immutable.
# Can be initialized in one of two ways:
# - float: assumes the integer part is dollars and the remainder is cents
#		In this case rounding to the nearest cent will occur.
# - int: assumes the integer is cents
class Money:
	def __init__(self, v):
		self.__setv(v)

	def __cmp__(self, o):
		if isinstance(o, float):
			return self.get() - o
		elif isinstance(o, int):
			return self.v - o
		elif isinstance(o, Money):
			return self.v - o.v
		else:
			raise exception.TypeError, "Only float, int, and Money types can be compared with Money"

	def __add__(self, o):
		if isinstance(o, float):
			return Money(self.v + int(o*100+0.5))
		elif isinstance(o, int):
			return Money(self.v + o)
		elif isinstance(o, Money):
			return Money(self.v + o.v)
		else:
			raise exception.TypeError, "Only float, int, and Money types can be added to Money"

	def __sub__(self, o):
		if isinstance(o, float) or isinstance(o, int):
			return self.__add__(o * -1)
		elif isinstance(o, Money):
			return Money(self.v - o.v)
		else:
			raise exception.TypeError, "Only float, int, and Money types can be subtracted from Money"

	def __mul__(self, o):
		if isinstance(o, int):
			return Money(self.v * o)
		elif isinstance(o, float):
			return Money(int(self.v * o + 0.5))
		else:
			raise exception.TypeError, "Only float and int types can multiply Money"

	def __div__(self, o):
		return self.__mul__(1.0/o)

	def __float__(self):
		return self.get()

	def __str__(self):
		def monetize(value):
			# value is an integer that represents cents
			def commaize(value):
				newvalue = ""
				count=0
				for i in range(len(value)-1, -1, -1):
					count += 1
					newvalue = value[i]+newvalue
					if count == 3 and i > 0:
						newvalue = ","+newvalue
						count=0
				return newvalue
			
			if value < 0:
				return "-"+monetize(value*-1)
			if value < 10:
				return "0.0"+str(value)
			if value < 100:
				return "0."+str(value)
			value = str(value)
			value = value[:-2]+"."+value[-2:]
			dotidx = len(value)-3
			return "%s.%s" % (commaize(value[0:dotidx]), value[dotidx+1:])
		return monetize(self.v)

	def __setv(self, v):
		if isinstance(v, int):
			self.v = v
		elif isinstance(v, float):
			self.v = int(v*100+0.5)
		else:
			raise exceptions.TypeError, "a Money value is expected to be string, int, or float"

	def get(self):
		return self.v/100.0

	def getint(self):
		return int(self.get())

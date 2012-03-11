class CardData:
	def __init__(self, obj, update, assump):
		self.obj = obj
		self.update = update
		self.assump = assump
		self.color = None

	def setAnnualProfit(self, ap):
		self.ap = ap

	def setColor(self, color):
		self.color = color

	def __cmp__(self, other):
		return (other.ap - self.ap).getint()

import threading

class CardLine(threading.Thread):
	def __init__(self, thname, card, v_in):
		threading.Thread.__init__(self, name=thname)
		self.card = card
		self.v_in = v_in

	def run(self):
		self.rewardvector = map(self.card.obj.getAnnualProfit, self.v_in['money'])

from HTMLList import *

class AssumptionList(HTMLList):
	def __init__(self, list):
		HTMLList.__init__(self, 'ol', 'class="assump"', list)

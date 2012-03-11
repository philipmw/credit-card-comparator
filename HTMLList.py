class HTMLList:
	def __init__(self, type, listargs, list):
		self.type = type
		self.listargs = listargs
		self.list = list

	def __str__(self):
		str = '<%s%s>' % (self.type, ' '+self.listargs if self.listargs is not None else '')
		for e in self.list:
			str += '<li>%s</li>' % e
		str += '</%s>' % self.type
		return str

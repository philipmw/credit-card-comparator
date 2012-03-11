# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from Cookie import SimpleCookie
import datetime, os, random, stat, time

from Settings import *

class Session:
	def __init__(self):
		self.sid = None
		try:
			cookies = SimpleCookie(os.environ['HTTP_COOKIE'])
		except KeyError:
			cookies = {}
	
		try:
			sid = cookies['sid'].value
		except KeyError:
			self.sid = self.remake_sid()
			return
	
		try:
			self.verify_sid(sid)
		except ValueError:
			self.sid = self.remake_sid()
			return
		# Beyond this point the value of 'sid' is trusted.
	
		if not os.access(Settings.tempdir+"/"+sid, os.W_OK | os.X_OK):
			self.sid = self.remake_sid()
			return
		self.sid = sid

	def verify_sid(self, sid):
		if len(sid) != 40:
			raise ValueError("length is incorrect")
		for i in range(0, len(sid)):
			if not (sid[i] >= '0' and sid[i] <= '9') and not (sid[i] >= 'a' and sid[i] <= 'f'):
				raise ValueError("an invalid character was found")
	
	def generate_sid(self):
		import hashlib, random, time
		return hashlib.sha256(str(time.time())+str(random.randint(0, 10000))).hexdigest()
	
	def remake_sid(self):
		sid = self.generate_sid()
		print("Set-Cookie: sid=%s; expires=%s" % (sid, (datetime.datetime.now()+datetime.timedelta(1)).strftime("%a, %d-%b-%Y %H:%M:%S GMT")))
		os.mkdir(Settings.tempdir+"/"+sid)
		os.chmod(Settings.tempdir+"/"+sid, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
		return sid

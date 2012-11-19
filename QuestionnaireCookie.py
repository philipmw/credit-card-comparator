# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

from Cookie import SimpleCookie
import base64, datetime, os, re

from Money import *

class QuestionnaireCookie:
	def __init__(self):
		self.cookie_lifetime_days = 365/2
		self.cookie_version = 1
		self.cleared = False

	def get(self):
		if self.cleared:
			raise Exception, "data was cleared"
		cookies = SimpleCookie(os.environ['HTTP_COOKIE'])
		s_enc = cookies['questionnaire'].value
		s = base64.b64decode(s_enc)
		# verify data
		regex = re.compile('v=[0-9]+,[0-9]+,[0-9]+,([a-z_]+=[0-9]+)+')
		if re.match(regex, s) is None:
			raise Exception, "the questionnaire cookie is malformed"
		# remove the first three elements, as they're special
		values = s.split(',')
		version = int(values[0][len("v="):])
		num_annual = int(values[1])
		num_userdata = int(values[2])
		values = values[3:]
		# check the recentness of the cookie
		if version != self.cookie_version:
			raise ValueError("Cookie is obsolete")
		# save the rest into their respective dictionaries
		annual = {}
		userdata_packed = {}
		regex_annual = re.compile('([a-z_]+)=([0-9]+)+')
		regex_userdata = re.compile('([a-z_]+)=([a-z0-9]+)+')
		count = 0
		for i in range(len(values)):
			if count < num_annual:
				result = re.match(regex_annual, values[i])
				if result is None:
					raise Exception, ('the string "%s" is malformed' % values[i])
				container = annual
				value = Money(100*int(result.group(2)))
			else:
				result = re.match(regex_userdata, values[i])
				if result is None:
					raise Exception, ('the string "%s" is malformed' % values[i])
				container = userdata_packed
				value = result.group(2)
			container[result.group(1)] = value
			count += 1
		userdata = self.userdata_unpack(userdata_packed)
		return annual, userdata

	def userdata_pack(self, userdata):
		userdata_packed = {}
		s = ''
		for r in userdata['rewards']:
			if r == 'cash':
				s += 'c'
			elif r == 'hotel':
				s += 'h'
			elif r == 'travel':
				s += 't'
		userdata_packed['rew'] = s
		if userdata['allow_annualfee']:
			userdata_packed['af'] = 'y'
		else:
			userdata_packed['af'] = 'n'
		userdata_packed['ds'] = userdata['date_submitted'].strftime("%y%m%d")
		return userdata_packed

	def userdata_unpack(self, userdata_packed):
		userdata = {}
		userdata['rewards'] = set()
		for c in userdata_packed['rew']:
			if c == 'c':
				userdata['rewards'] |= set(['cash'])
			elif c == 'h':
				userdata['rewards'] |= set(['hotel'])
			elif c == 't':
				userdata['rewards'] |= set(['travel'])
		if userdata_packed['af'] == 'y':
			userdata['allow_annualfee'] = True
		else:
			userdata['allow_annualfee'] = False
		userdata['date_submitted'] = datetime.datetime.strptime(userdata_packed['ds'], "%y%m%d")
		return userdata

	def set(self, annual, userdata):
		s = "v=%d" % self.cookie_version
		s += ",%d,%d" % (len(annual), len(userdata))
		for (k,v) in annual.iteritems():
			s += ",%s=%d" % (k, v.getint())
		userdata_packed = self.userdata_pack(userdata)
		for (k,v) in userdata_packed.iteritems():
			s += ",%s=%s" % (k, v)
		s_enc = base64.b64encode(s)
		self.write_cookie(s_enc)

	def write_cookie(self, s):
		cookie_ts_format = "%a, %d-%b-%Y %H:%M:%S GMT"
		if s is None:
			print("Set-Cookie: questionnaire=; expires=%s" % (datetime.datetime.now()-datetime.timedelta(1)).strftime(cookie_ts_format))
		else:
			print("Set-Cookie: questionnaire=%s; expires=%s" % (s, (datetime.datetime.now()+datetime.timedelta(self.cookie_lifetime_days)).strftime(cookie_ts_format)))

	def clear(self):
		self.write_cookie(None)
		self.cleared = True

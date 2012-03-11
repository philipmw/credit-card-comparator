#!/bin/env python

# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

import cgi, datetime, os, random, stat, sys, types

from CardCharter import *
from Money import *
from QuestionnaireCookie import *
from Session import *
from Settings import *

sys.path.insert(0, 'cards')
from CardCollection import *
del sys.path[0]

def integerify(input, default=None):
	if input is None or len(input) == 0:
		if default is not None:
			return default
		else:
			raise ValueError("no value")
	for i in range(0, len(input)):
		if input[i] < '0' or input[i] > '9':
			if default is not None:
				return default
			else:
				raise ValueError("a non-integer character was found")
	return int(input)

def make_filepath(name=None):
	if name is None:
		return "%s/%s" % (Settings.tempdir, sid)
	else:
		return "%s/%s/%s" % (Settings.tempdir, sid, name)

def print_page_top(titlesuff):
	print('Content-Type: text/html; charset=utf-8\n')
	print('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n<head>\n\t<link rel="stylesheet" type="text/css" href="static/style.css"/>\n\t<title>Credit Card Comparator: %s</title>\n</head>\n<body>' % titlesuff)
	print('<h1>Credit Card Comparator: %s</h1>' % titlesuff)

def print_page_bottom():
	print('<div id="footer">')
	print('<p>If you have criticism, praise, or suggestions, <a href="http://www.qnan.org/~pmw/contact">contact the author</a>.</p>')
	print('<p>This software is open-source under the BSD license.  <a href="git://qnan.org/pmw/ccc">Get it with git</a> or <a href="http://git.qnan.org/g/ccc">browse its source</a>.</p>')
	print('</div>')
	print('</body>\n</html>')

def print_error(msg):
	print_page_top("error")
	print('<p class="error">%s</p>' % (msg))
	print_page_bottom()

def make_random_string(len):
	s = ""
	for i in range(0, len):
		s += chr(random.randrange(ord('a'), ord('z'), 1))
	return s

def make_peryear_str(val):
	return "%s /yr" % val

#################################

if not os.access(Settings.tempdir, os.W_OK | os.X_OK):
	print('Content-Type: text/plain\n')
	print('ERROR: Cannot write to the temporary directory.')
	sys.exit(1)

qcook = QuestionnaireCookie()
sid = Session().sid

form = cgi.FieldStorage()
userdata = {}
annual = {}

if form.getvalue('form_submitted') is None:
	# This page is being loaded directly; let's see if we can read the cookie.
	try:
		annual, userdata = qcook.get()
	except Exception, msg:
		print_error("You did not submit the questionnaire.")
		print('<!-- Exception: %s -->' % msg)
		sys.exit(1)
else:
	try:
		annual['total'] = Money(100*integerify(form.getvalue('m-total')) * 12)
		annual['grocerydrug'] = Money(100*integerify(form.getvalue('m-grocerydrug'), 0) * 12)
		annual['restaurant'] = Money(100*integerify(form.getvalue('m-restaurant'), 0) * 12)
		annual['gasstation'] = Money(100*integerify(form.getvalue('m-gasstation'), 0) * 12)
		annual['automaint'] = Money(100*integerify(form.getvalue('m-automaint'), 0) * 12)
		annual['utilities'] = Money(100*integerify(form.getvalue('m-utilities'), 0) * 12)
		annual['hmotel'] = Money(100*integerify(form.getvalue('y-hmotel'), 0))
		annual['airtravel'] = Money(100*integerify(form.getvalue('y-airtravel'), 0))
		annual['airfees'] = Money(100*integerify(form.getvalue('y-airfees'), 0))
		annual['carrental'] = Money(100*integerify(form.getvalue('y-carrental'), 0))
	except ValueError, msg:
		print_error("One of your responses to the questionnaire is inadequate: %s." % msg)
		sys.exit(1)
	
	userdata['rewards'] = form.getvalue('rewards')
	if userdata['rewards'] is None:
		userdata['rewards'] = set()
	elif type(userdata['rewards']) is not types.ListType:
		userdata['rewards'] = set([userdata['rewards']])
	else:
		userdata['rewards'] = set(userdata['rewards'])
	
	if form.getvalue('allow_annualfee') is None or form.getvalue('allow_annualfee') != "yes":
		userdata['allow_annualfee'] = False
	else:
		userdata['allow_annualfee'] = True

	userdata['date_submitted'] = datetime.datetime.today()
	qcook.set(annual, userdata)

annual_misc = annual['total'] -  (annual['grocerydrug']+annual['restaurant']+annual['gasstation']+annual['automaint']+annual['utilities']+annual['hmotel']+annual['airtravel']+annual['carrental'])
if annual_misc < 0:
	print_error("Your responses are inconsistent.  Your total chargeable expenses must be no less than the sum of your expenses on groceries, fuel, utilities, and so on.")
	sys.exit(2)
if len(userdata['rewards']) == 0:
	print_error("You've unchecked all reward types, indicating that no reward card suits you.  Please select at least one reward type.")
	sys.exit(3)

top_colors = ['#000000', '#00ff00', '#0000ff', '#ff0000', '#ffff00']
cc = CardCollection(annual, userdata, top_colors)
have_chart = len(cc) > 0
if have_chart:
	imgfn = make_random_string(5)+".png"
	charter = CardCharter(make_filepath(imgfn))
	charter.draw(cc, int(annual['total'].get()))
	os.chmod(make_filepath(imgfn), stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
print_page_top("results")
# Display the questionnaire, in case the person loaded the results with a stored questionnaire
print('<h2>Your spending patterns</h2>')
print('<table id="stored-questionnaire">')
print('<tr>')
print('\t<td class="cat">Grocery stores, supermarkets, drug stores:</td>\n\t<td class="val">%s</td>' % make_peryear_str(annual['grocerydrug']))
print('\t<td class="cat">Restaurants:</td>\n\t<td class="val">%s</td>' % make_peryear_str(annual['restaurant']))
print('</tr>')
print('<tr>')
print('\t<td class="cat">Gas stations:</td>\n\t<td class="val">%s</td>' % make_peryear_str(annual['gasstation']))
print('\t<td class="cat">Automotive maintenance:</td>\n\t<td class="val">%s</td>' % make_peryear_str(annual['automaint']))
print('</tr>')
print('<tr>')
print('\t<td class="cat">Utilities:</td>\n\t<td class="val">%s</td>' % make_peryear_str(annual['utilities']))
print('\t<td class="cat">Hotels and motels:</td>\n\t<td class="val">%s</td>' % make_peryear_str(annual['hmotel']))
print('</tr>')
print('<tr>')
print('\t<td class="cat">Airline travel:</td>\n\t<td class="val">%s</td>' % make_peryear_str(annual['airtravel']))
print('\t<td class="cat">Airline fees:</td>\n\t<td class="val">%s</td>' % make_peryear_str(annual['airfees']))
print('</tr>')
print('<tr>')
print('\t<td class="cat">Car rental:</td>\n\t<td class="val">%s</td>' % make_peryear_str(annual['carrental']))
print('\t<td class="cat">Everything else:</td>\n\t<td class="val">%s</td>' % make_peryear_str(annual_misc))
print('</tr>')
print('<tr>')
print('\t<td colspan="2" class="cat-total">Total:</td>\n\t<td colspan="2" class="val-total">%s</td>' % make_peryear_str(annual['total']))
print('</tr>')
print('</table>')

print('<h2>Rewards</h2>')
print('<p>With your spending patterns, this table shows how much you would gain (or lose) annually with each of the cards.  Below the table is a chart of rewards for your spending patterns, and below the chart are <a href="#details">details</a>.</p>')
print('<table id="rewards">')
annualProfitMax = None
for card in cc:
	annualProfitCurr = card.obj.getAnnualProfit(annual['total'])
	if annualProfitMax is None or annualProfitMax < annualProfitCurr:
		annualProfitMax = annualProfitCurr

print('\t<tr><th>Card</th><th>Reward type(s)</th><th>Annual<br/>profit/loss</th><th>Effective<br/>cashback</th><th>Chart color</th></tr>')
for card in cc:
	annualProfit = card.obj.getAnnualProfit(annual['total'])
	print('\t<tr%s><td class="cardname"><a href="%s">%s</a></td><td class="rewardtype">%s</td><td class="amount">%s</td><td class="cashback">%.2f</td><td class="colorid"%s></td></tr>' % (
		'' if annualProfit < annualProfitMax else ' class="best"',
		card.obj.url,
		card.obj,
		", ".join(card.obj.getRewardTypes()),
		annualProfit,
		100 * annualProfit.get() / annual['total'].get(),
		'' if card.color is None else (' style="background-color: %s"' % card.color)
	)
)
print('</table>')
print('<p>Do you know of another credit card worthy of being in the list above?  <a href="http://www.qnan.org/~pmw/contact">Let me know!</a></p>')
if have_chart:
	print('<p>Here is a chart of rewards for your spending patterns.</p>')
	print('<p><img src="%s/%s/%s"/></p>' % (Settings.urlrel, sid, imgfn))
else:
	print('<p>We did not generate a chart for you because there are no cards that meet your reward type criteria.</p>')
print('<h2><a name="details">Details</a></h2>')
print('<table id="details">')
print('<tr><th>Card</th><th>Last updated</th><th>Assumption</th></tr>')
for card in cc:
	print('<tr><td class="card">%s</td><td class="updated">%s</td><td class="assumption">%s</td></tr>' % (card.obj, card.update.strftime("%b %Y"), card.assump if card.assump is not None else 'none'))
print('</table>')
print_page_bottom()

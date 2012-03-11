#!/bin/env python

import cgi

from QuestionnaireCookie import *

def get(annual, name, divisor=1):
	return annual[name].getint()/divisor if annual.has_key(name) else ''

def get_rewardbox(userdata, name):
	return ' checked="checked"' if not userdata.has_key('rewards') or name in userdata['rewards'] else ''

qcook = QuestionnaireCookie()
form = cgi.FieldStorage()
if form.getvalue('clear') is not None:
	qcook.clear()
	
print('Content-Type: text/html\n')
try:
	annual, userdata = qcook.get()
except Exception, msg:
	annual = {}
	userdata = {}

print('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
	'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n'
	'<head>\n'
	'	<title>Credit Card Comparator</title>\n'
	'	<link rel="stylesheet" type="text/css" href="static/style.css"/>\n'
	'	<meta http-equiv="Author" content="Philip M. White"/>\n'
	'</head>\n'
	'<body>\n'
	'<div id="cardimg">\n'
	'	<p><img src="static/credit_cards.jpg" alt="Photo of a collection of credit cards"/></p>\n'
	'</div>\n'
	'<h1>Credit Card Comparator</h1>\n'
	'<div id="questionnaire">\n'
	'<form method="post" action="result.cgi">\n'
	'<input type="hidden" name="form_submitted" value="y"/>\n'
	'<table>\n'
	'<tr>\n'
	'	<td class="q">Total monthly expenses chargeable on a credit card?</td>\n'
	'	<td class="a">$&nbsp;<input type="text" name="m-total" size="6" maxlength="6" value="%s"/>/month</td>\n'
	'	<td rowspan="9" class="rewards">Acceptable rewards:'
	% (get(annual, 'total', 12)))
print('		<ul>\n'
	'			<li><input type="checkbox" name="rewards" value="cash"%s/> cash</li>\n'
	'			<li><input type="checkbox" name="rewards" value="travel"%s/> discounted travel</li>\n'
	'			<li><input type="checkbox" name="rewards" value="hotel"%s/> discounted hotels</li>\n'
	'		</ul>\n'
	'		<p><input type="checkbox" name="allow_annualfee" value="yes"%s/> Include cards with an annual fee?</p>'
	% (
		get_rewardbox(userdata, 'cash'),
		get_rewardbox(userdata, 'travel'),
		get_rewardbox(userdata, 'hotel'),
		' checked="checked"' if not userdata.has_key('allow_annualfee') or userdata['allow_annualfee'] else ''
	))
print('	</td>\n'
	'</tr>\n'
	'<tr>\n'
	'	<td class="q">Monthly spending in grocery stores, supermarkets, and drug stores?  Do not include warehouses and membership clubs.</td>\n'
	'	<td class="a">$&nbsp;<input type="text" name="m-grocerydrug" size="6" maxlength="6" value="%s"/>/month</td>\n'
	'</tr>\n'
	'<tr>\n'
	'	<td class="q">Monthly spending at restaurants, including full-service, cafeterias, and fast food?</td>\n'
	'	<td class="a">$&nbsp;<input type="text" name="m-restaurant" size="6" maxlength="6" value="%s"/>/month</td>\n'
	'</tr>\n'
	'<tr>\n'
	'	<td class="q">Monthly spending at gas stations?</td>\n'
	'	<td class="a">$&nbsp;<input type="text" name="m-gasstation" size="6" maxlength="6" value="%s"/>/month</td>\n'
	'</tr>\n'
	'<tr>\n'
	'	<td class="q">Monthly spending on automotive maintenance?</td>\n'
	'	<td class="a">$&nbsp;<input type="text" name="m-automaint" size="6" maxlength="6" value="%s"/>/month</td>\n'
	'</tr>\n'
	'<tr>\n'
	'	<td class="q">Monthly spending on utilities?</td>\n'
	'	<td class="a">$&nbsp;<input type="text" name="m-utilities" size="6" maxlength="6" value="%s"/>/month</td>\n'
	'</tr>\n'
	'<tr>\n'
	'	<td class="q">Annual spending on hotels and motels?</td>\n'
	'	<td class="a">$&nbsp;<input type="text" name="y-hmotel" size="6" maxlength="6" value="%s"/>/year</td>\n'
	'</tr>\n'
	'<tr>\n'
	'	<td class="q">Annual spending on airline travel?</td>\n'
	'	<td class="a">$&nbsp;<input type="text" name="y-airtravel" size="6" maxlength="6" value="%s"/>/year</td>\n'
	'</tr>\n'
	'<tr>\n'
	'	<td class="q">Annual spending on airline fees?</td>\n'
	'	<td class="a">$&nbsp;<input type="text" name="y-airfees" size="6" maxlength="6" value="%s"/>/year</td>\n'
	'</tr>\n'
	'<tr>\n'
	'	<td class="q">Annual spending on car rental?</td>\n'
	'	<td class="a">$&nbsp;<input type="text" name="y-carrental" size="6" maxlength="6" value="%s"/>/year</td>\n'
	'</tr>\n'
	'<tr>\n'
	'	<td class="buttons" colspan="2"><input type="reset" class="reset"/> <input type="submit" value="Compare rewards &gt;"/></td>\n'
	'</tr>\n'
	'</table>\n'
	'</form>\n'
	'</div>\n'
	'\n'
	'<div id="descr">\n'
	'<p>Many credit card companies offer cards that accumulate cash, airline miles, and "points".  Which card is the best for you?</p>\n'
	'<p>I developed this comparator to settle the debate.  This program tracks popular cards from different providers.  Just fill out this questionnaire, and you will find out which credit card will yield you the most rewards.</p>\n'
	'<p>Answer all questions, and round your answers to the nearest dollar.</p>\n'
	'<p>Your responses are used only for calculating your rewards and are not stored on the server.</p>'
	% (
		get(annual, 'grocerydrug', 12),
		get(annual, 'restaurant', 12),
		get(annual, 'gasstation', 12),
		get(annual, 'automaint', 12),
		get(annual, 'utilities', 12),
		get(annual, 'hmotel'),
		get(annual, 'airtravel'),
		get(annual, 'airfees'),
		get(annual, 'carrental')
	)
)
if userdata.has_key('date_submitted'):
	print('<p class="last-submitted">(The questionnaire has been pre-filled with your responses from %s.  <a href="?clear=y">Clear them.</a>)</p>' % userdata['date_submitted'].strftime('%a, %b %d'))
print('</div>\n'
	'<div id="footer">\n'
	'<p>This software was written by <a href="http://www.qnan.org/~pmw">Philip M. White</a>.  It is powered by <a href="http://www.python.org">Python</a> and <a href="http://matplotlib.sourceforge.net/">matplotlib</a>.</p>\n'
	'</div>\n'
	'</body>\n'
	'</html>'
)

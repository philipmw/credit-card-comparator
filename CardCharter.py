# Written by Philip M. White <pmw@qnan.org>
# Copyright 2009.
# Licensed under the BSD license.

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

from Money import *
from Settings import *
sys.path.insert(0, 'cards')
from CardCollection import *
from CardLine import *
del sys.path[0]

class CardCharter():
	def __init__(self, outfn, dpi=100):
		self.outfn = outfn
		self.dpi = dpi

	def draw_legend(self, plt, x_val, max_reward):
		legend_x = x_val['left'] + min(50, x_val['right']/20)
		legend_y = max_reward * 29/30
		plt.text(legend_x, legend_y, "See table above for the color reference.", size=10)
		# The actual legend is turned off because I cannot find a way
		# to make it look acceptable under every circumstance.

		# legend_y_delta = max_reward / 29
		# plt.text(legend_x, legend_y, "Legend:", size=10)
		# legend_y -= legend_y_delta
		# legend_x += 100
		# for card in crcards:
		# 	plt.text(legend_x, legend_y, ("---- %s" % card['obj']), color=card['color'], size=9)
		# 	legend_y -= legend_y_delta

	def draw(self, cc, x_point):
		rangex = int(max(1500, x_point*0.25))
		x_val = {'point': x_point, 'left': max(0, x_point-rangex/2), 'right': x_point+rangex/2}
		v_in_raw = range(x_val['left'], x_val['right'])
		v_in = {'raw': v_in_raw, 'money': map(Money, map(lambda x: x*100, v_in_raw))}
		
		max_reward = None
		for card in cc:
		#for i in range(0, len(cc.creditcards)):
			#r = cc.creditcards[i]['obj'].getAnnualProfit(v_in['money'][-1]).getint()
			r = card.obj.getAnnualProfit(v_in['money'][-1]).getint()
			if max_reward is None or r > max_reward:
				max_reward = r

		threadlist = []
		for card in cc:
			if card.color is None:
				continue
			th = CardLine(str(card), card, v_in)
			th.start()
			threadlist.append(th)

		# Format the image while threads are running
		plt.title('Credit Card Comparator: personalized comparison for your spending patterns')
		plt.xlabel('Amount charged in a year ($)')
		plt.ylabel('Annual profit or loss ($)')
		plt.axvline(x_val['point'], linestyle=':', color='#c0c0c0')
		self.draw_legend(plt, x_val, max_reward)

		for th in threadlist:
			th.join()
			plt.plot(
				v_in['raw'],
				th.rewardvector,
				color=th.card.color,
				linewidth=4)

		plt.savefig(self.outfn, dpi=self.dpi)

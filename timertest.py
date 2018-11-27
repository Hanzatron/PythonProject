#!/usr/bin/python

#####################################################################################
# TIMERTEST																		HANS
# V0.1
#
# V0.0		11/02/15		created
# V0.1		20/03/15		Pulstrein bijgevoegd
#####################################################################################
#
#
#####################################################################################

import time #sleep functie
import datetime

class Ondelay(object):
	"""Ondelay"""
	def __init__(self,m, s, ms):
		self.ms = ms	#milliseconden
		self.s = s		#seconden
		self.m = m		#minuten
		self.trigger = False
		self.triggertijd = datetime.datetime.now()
		self.out = False
		self.tijd = datetime.timedelta(0,self.s, 0, self.ms, self.m) # days, seconds, microseconds, milliseconds, minutes, hours, weeks,...
	def start(self):
		if not self.trigger:
			self.triggertijd = datetime.datetime.now()
		if datetime.datetime.now() >= (self.triggertijd + self.tijd):
			self.out = True
		else:
			self.out = False
class Offdelay(object):
	"""Offdelay"""
	def __init__(self,m, s, ms):
		self.ms = ms	#milliseconden
		self.s = s		#seconden
		self.m = m		#minuten
		self.trigger = False
		self.triggertijd = datetime.datetime.now()
		self.out = False
		self.tijd = datetime.timedelta(0,self.s, 0, self.ms, self.m) # days, seconds, microseconds, milliseconds, minutes, hours, weeks,...
	def start(self):
		if self.trigger:
			self.triggertijd = datetime.datetime.now()
		if self.trigger or (datetime.datetime.now() >= (self.triggertijd + self.tijd)):
			self.out = True
		else:
			self.out = False
class Pulsetimer(object):
	"""Pulsetimer"""
	def __init__(self,m, s, ms):
		self.ms = ms	#milliseconden
		self.s = s		#seconden
		self.m = m		#minuten
		self.trigger = False
		self.trigger_mem =False
		self.triggertijd = datetime.datetime(1900,1,1,0)
		self.out = False
		self.tijd = datetime.timedelta(0,self.s, 0, self.ms, self.m) # days, seconds, microseconds, milliseconds, minutes, hours, weeks,...
	def start(self):
		if self.trigger and not self.trigger_mem: #trigger_mem laat output niet hoog staan als trigger hoog blijft.
			self.triggertijd = datetime.datetime.now()
			self.trigger_mem = True
		if not self.trigger:
			self.trigger_mem = False
		if (datetime.datetime.now() < (self.triggertijd + self.tijd)):
			self.out = True
		else:
			self.out = False

class Pulstrein(object):
	"""Pulsetimer"""
	def __init__(self,m, s, ms):
		self.ms = ms	#milliseconden
		self.s = s		#seconden
		self.m = m

		self.vorigepuls = datetime.datetime.now()
		self.out = False
		self.tijd = datetime.timedelta(0,self.s, 0, self.ms, self.m) # days, seconds, microseconds, milliseconds, minutes, hours, weeks,...

	def start(self):
		if datetime.datetime.now() >= (self.vorigepuls + self.tijd):
			self.out = True
			self.vorigepuls = datetime.datetime.now()
		else:
			self.out = False

def Main():
	t1 = Pulsetimer(0, 10, 0)
	t2 = Ondelay(0,6,0)
	cyclus_1s = Pulstrein(0,1,0)
	t2.trigger = True
	starttijd = datetime.datetime.now()
	print "start: t1: %s op %s" % ( t1.out, datetime.datetime.now())
	while True:
		cyclus_1s.start()
		t1.start()
		t2.start()

		t1.trigger = t2.out
		if cyclus_1s.out:
			print "t1 : %s  op  %s" % (t1.out, datetime.datetime.now())
		time.sleep(0.01)

if __name__ == '__main__':
	Main()

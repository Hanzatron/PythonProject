#!/usr/bin/python

#####################################################################################
# SINUSDEMPING																		HANS
# V0.0
#
# V0.0		20/03/15		created
# V0.1		20/03/15		Pulstrein bijgevoegd
#####################################################################################
# del(n[0])		n.append(4)
# 
#
#####################################################################################

import time #sleep functie
import datetime
import os
import math


class Pulstrein(object): #code uit timertest.py V0.1
	"""Pulsetimer"""
	def __init__(self,m, s, ms):
		self.ms = ms	#milliseconden
		self.s = s		#seconden
		self.m = m		#minuten
		
		self.vorigepuls = datetime.datetime.now()
		self.out = False	
		self.tijd = datetime.timedelta(0,self.s, 0, self.ms, self.m) # days, seconds, microseconds, milliseconds, minutes, hours, weeks,...
		
	def start(self):	
		if datetime.datetime.now() >= (self.vorigepuls + self.tijd):
			self.out = True
			self.vorigepuls = datetime.datetime.now()
		else:
			self.out = False

class Hoekrotatie(object):
	def __init__(self,rpm):
		self.rpm = rpm	#rotaties per minuut
		
		self.vorigetijd = datetime.datetime.now()
		self.hoek = 0.0
		self.sinus = 0.0
		
	def start(self):
		delta_t = ((datetime.datetime.now()-self.vorigetijd).microseconds)	
		rpms = ((self.rpm /60.0)/1000000.0)* delta_t
		if (self.hoek + (rpms * 360)) < 360:
			self.hoek = self.hoek + (rpms * 360)
		else:
			self.hoek = 0
		self.sinus = math.sin(math.radians(self.hoek))
		self.vorigetijd = datetime.datetime.now()

class Demping(object):
	def __init__(self, duur, sampletijd):
		
		self.duur = duur
		self.sampletijd = int(sampletijd)
		
		self.ingang = 0
		self.samples = []
		self.sample = datetime.timedelta(0,0,0,sampletijd)
		for x in range(int((self.duur * 1000.0)/self.sampletijd)):
			self.samples.append(0)
			
		self.lastsample = datetime.datetime.now()
		self.gedemptewaarde = 0
		
	def start(self):
		if datetime.datetime.now() >= self.lastsample + self.sample:
			self.samples.append(self.ingang)
			self.samples.pop(0)
			self.lastsample = datetime.datetime.now()
		
		tot_samples = 0.0
		for x in range(len(self.samples)):
			tot_samples = tot_samples + self.samples[x]
		self.gedemptewaarde = tot_samples / len(self.samples)
def Main():
	s1 = Hoekrotatie(0.5)
	d1 = Demping(10, 100)
	
	
	while True:	
		s1.start()
		d1.start()
		d1.ingang = s1.hoek
		print "hoek: %s en sinus %s" %(format(s1.hoek, '.1f'), format(s1.sinus, '.1f'))
		print "gedempte waarde hoek: %s" %(d1.gedemptewaarde)
		
		time.sleep(0.01)
		os.system('cls')
if __name__ == '__main__':
	Main()	

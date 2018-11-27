#!/usr/bin/python

#####################################################################################
# PID.py																		HANS
# V0.2
#
# V0.0		05/03/15		created
# V0.1		20/03/15		variatie op bepaalde constanten door class hoekrotatie
# V0.2		20/03/15		demping op debieten en energietoevoer
#####################################################################################
# Process simulatie
#
#
#####################################################################################

import time #sleep functie
from datetime import datetime, timedelta
from threading import Thread
import os
import math


class Regelaar(object):
	"""PID regelaar"""
	def __init__(self):
		self.pv = 0
		self.w = 0
		self.p = 0
		self.i = 0
		self.d = 0

		self.y = 30
		self.p_actie = 0
		self.i_actie = 0
		self.d_actie = 0

		self.bovengrens = 100.0
		self.ondergrens = 0.0

		self.lastcyclus = datetime.now()
		self.lastpv = 0.0

	def start_regeling(self):
		self.p_actie = (self.w - self.pv) * self.p
		if self.p_actie > 100:
			self.p_actie = 100
		delta_t = ((datetime.now()-self.lastcyclus).microseconds)
		self.i_actie = self.i_actie + ((((self.w - self.pv)/self.i)/1000000.0) * delta_t)
		if self.i_actie > 100:
			self.i_actie = 100

		self.d_actie = (((self.lastpv - self.pv)*1000000)/delta_t)*self.d
		if self.d_actie > 100:
			self.d_actie = 100

		if self.p_actie + self.i_actie + self.d_actie < self.ondergrens: #ondergrens regelaar = 0
			self.Y = self.ondergrens
		elif self.p_actie + self.i_actie + self.d_actie > self.bovengrens: #bovengrens regelaar = 100
			self.y = self.bovengrens
		else:
			self.y = self.p_actie + self.i_actie + self.d_actie

		self.lastcyclus = datetime.now()
		self.lastpv = self.pv
class Processsim(object):
	"""PID regelaar"""
	def __init__(self):
		self.tanktemperatuur = 0.0			#Temperatuur tankinhoud
		self.tankvolume = 0.0				#Inhoud tank
		self.tankenergie =  0.0				#E=V*t (energie = volume * temperatuur)
		self.energieverliesfactor = 0.3		#bepaald hoe snel tank afkoeld of opwarmd door omgevingstemperatuur
		self.omgevingstemperatuur = 25.0

		self.toevoer = False
		self.toevoerdebiet = 0.0
		self.toevoertemperatuur = 0.0
		self.toevoerregelklepstand = 100.0

		self.act_toevoerdebiet = 0.0
		self.act_afvoerdebiet = 0.0
		self.act_toevoertemperatuur = 0.0

		self.afvoer = False
		self.afvoerdebiet = 0.0
		self.afvoerregelklepstand = 100.0

		self.stoomklepstand = 0.0
		self.stoom_max_energie = 50.0

		self.hr1 = Hoekrotatie(0.1)
		self.hr2 = Hoekrotatie(0.15)

		self.d1 = Demping(5, 150)
		self.d2 = Demping(4, 150)
		self.d3 = Demping(10, 150)

		self.lastcyclus = datetime.now()

	def start(self):
		self.tankenergie = self.tankvolume * self.tanktemperatuur

		#sinusgenerators starten:
		self.hr1.start()
		self.hr2.start()

		#demping starten
		self.d1.start()
		self.d2.start()
		self.d3.start()

		#sinus op toevoertemperatuur
		self.act_toevoertemperatuur = self.toevoertemperatuur + self.hr1.sinus

		#delta_t is de tijd sinds vorige cyclus dat dit programma doorlopen is
		delta_t = ((datetime.now()-self.lastcyclus).microseconds)

		#tankenergie/volume aanpassen als er wordt toegevoerd of afgevoerd
		#toevoer:
		if self.toevoer == True:
			self.d1.ingang = (self.toevoerdebiet * (self.toevoerregelklepstand/100.0))
			self.act_toevoerdebiet = self.d1.gedemptewaarde

			self.tankvolume = self.tankvolume + ((self.act_toevoerdebiet/1000000.0)* delta_t)
			self.tankenergie = self.tankenergie + (((self.act_toevoerdebiet/1000000.0)* delta_t)* self.act_toevoertemperatuur)
		elif self.toevoer == False and (self.act_toevoerdebiet > 0.05):
			self.act_toevoerdebiet = self.act_toevoerdebiet - 0.05
			self.tankvolume = self.tankvolume + ((self.act_toevoerdebiet/1000000.0)* delta_t)
			self.tankenergie = self.tankenergie + (((self.act_toevoerdebiet/1000000.0)* delta_t)* self.act_toevoertemperatuur)
		elif self.toevoer == False and (self.act_toevoerdebiet <= 0.05):
				self.act_toevoerdebiet = 0

		#afvoer:
		if (self.afvoer == True) and self.tankvolume > 0:
			self.d2.ingang = ((self.afvoerdebiet * (self.afvoerregelklepstand/100.0)) + (self.hr2.sinus * 0.05))
			self.act_afvoerdebiet = self.d2.gedemptewaarde

			self.tankvolume = self.tankvolume - ((self.act_afvoerdebiet/1000000.0)*delta_t)
			self.tankenergie = self.tankenergie - (((self.act_afvoerdebiet/1000000.0)* delta_t)* self.tanktemperatuur)
		elif self.afvoer == False and (self.act_afvoerdebiet > 0.05):
			self.act_afvoerdebiet = self.act_afvoerdebiet - 0.05
			self.tankvolume = self.tankvolume - ((self.act_afvoerdebiet/1000000.0)*delta_t)
			self.tankenergie = self.tankenergie - (((self.act_afvoerdebiet/1000000.0)* delta_t)* self.tanktemperatuur)
		elif self.afvoer == False and (self.act_afvoerdebiet <= 0.05):
				self.act_afvoerdebiet = 0

		if self.tankvolume < 0:
			self.tankvolume = 0

		#afkoeling tank door verschil met omgevingstemperatuur:
		self.tankenergie = self.tankenergie + ((((self.omgevingstemperatuur - self.tanktemperatuur)* self.energieverliesfactor)/1000000.0)* delta_t)

		#stoomtoevoer
		self.d3.ingang = (((self.stoom_max_energie/1000000.0)*delta_t)*(self.stoomklepstand/100.0))

		#~ self.tankenergie = self.tankenergie + (((self.stoom_max_energie/1000000.0)*delta_t)*(self.stoomklepstand/100.0))
		self.tankenergie = self.tankenergie + self.d3.gedemptewaarde

		#tanktemperatuur berekenen adhv tankenergie
		if self.tankvolume > 0: #delen door 0 kan niet...
			self.tanktemperatuur = self.tankenergie/self.tankvolume
		else:
			self.tanktemperatuur = 0

		self.lastcyclus = datetime.now()
	def niveausturing(self):
		if self.tankvolume > 90:
			self.toevoer = False
		if self.tankvolume < 75:
			self.toevoer = True
		if self.tankvolume < 5:
			self.afvoer = False
		if self.tankvolume > 10:
			self.afvoer = True
class Hoekrotatie (object):
	def __init__(self,rpm):
		self.rpm = rpm	#rotaties per minuut

		self.vorigetijd = datetime.now()
		self.hoek = 0.0
		self.sinus = 0.0

	def start(self):
		delta_t = ((datetime.now()-self.vorigetijd).microseconds)
		rpms = ((self.rpm /60.0)/1000000.0)* delta_t
		if (self.hoek + (rpms * 360)) < 360:
			self.hoek = self.hoek + (rpms * 360)
		else:
			self.hoek = 0
		self.sinus = math.sin(math.radians(self.hoek))
		self.vorigetijd = datetime.now()

class Demping(object):
	def __init__(self, duur, sampletijd):

		self.duur = duur
		self.sampletijd = int(sampletijd)

		self.ingang = 0
		self.samples = []
		self.sample = timedelta(0,0,0,sampletijd)
		for x in range(int((self.duur * 1000.0)/self.sampletijd)):
			self.samples.append(0)

		self.lastsample = datetime.now()
		self.gedemptewaarde = 0

	def start(self):
		if datetime.now() >= self.lastsample + self.sample:
			self.samples.append(self.ingang)
			self.samples.pop(0)
			self.lastsample = datetime.now()

		tot_samples = 0.0
		for x in range(len(self.samples)):
			tot_samples = tot_samples + self.samples[x]
		self.gedemptewaarde = tot_samples / len(self.samples)


def disp_PID(naam, p_actie, i_actie, d_actie, tot_actie):
	p = ""
	i = ""
	d = ""
	y = ""
	spatie_p = ""
	spatie_i = ""
	spatie_d = ""
	spatie_y = ""
	offset = 30
	#P-actie
	for x in range(offset - len(str(format(p_actie, '.2f')))):
		spatie_p = spatie_p + " "
	if p_actie > 0:
		for x in range(int(p_actie/4.0)):
			p = p + "*"
	else:
		p = spatie_p

	#I-actie
	for x in range(offset - len(str(format(i_actie, '.2f')))):
		spatie_i = spatie_i + " "

	if i_actie > 0:
		for x in range(int(i_actie/4.0)):
			i = i + "*"
	else:
		i = spatie_i

	#D-actie
	for x in range(offset - len(str(format(d_actie, '.2f')))):
		spatie_d = spatie_d + " "

	if d_actie > 0:
		for x in range(int(d_actie/4.0)):#- len(str(format(d_actie, '.2f')))):
			d = d + "*"
		d = spatie_d + "|" + d
	elif d_actie < 0:
		spatie_d = ""
		for x in range(offset - abs(int(d_actie/4.0))- len(str(format(d_actie, '.2f')))):
			spatie_d = spatie_d + " "
		for x in range(abs(int(d_actie/4.0))):
			d = d + "*"
		d = spatie_d + d + "|"
	else:
		d = spatie_d + "|"

	#Totale actie
	for x in range(offset - len(str(format(tot_actie, '.2f')))):
		spatie_y = spatie_y + " "

	for x in range(int(tot_actie/4.0)):
		y = y + "*"
	print "-------------------------------------------------------------------------------"
	print naam + ": "
	print "-------------------------------------------------------------------------------"
	print "P: " + str(format(p_actie, '.2f')) + "" + spatie_p + "|" + p
	print "I: " + str(format(i_actie, '.2f')) + "" + spatie_i + "|"+ i
	print "D: " + str(format(d_actie, '.2f')) + "" + d
	print "Y: " + str(format(tot_actie, '.2f')) + "" + spatie_y + "|"+ y
	print "-------------------------------------------------------------------------------"


def Main():
	#initiele waarden voor process simulator
	processsim = Processsim() #object aanmaken
	processsim.tankvolume = 50.0
	processsim.tanktemperatuur = 25.0
	processsim.omgevingstemperatuur = 25.0
	processsim.toevoerdebiet = 1.0
	processsim.toevoertemperatuur = 30.0
	processsim.afvoerdebiet = 0.5

	niveauregelaar = Regelaar() #regelaar object aanmaken
	niveauregelaar.p = 4
	niveauregelaar.i = 10.0
	niveauregelaar.d = 50.0

	temperatuurregelaar = Regelaar() #regelaar object aanmaken
	temperatuurregelaar.p = 1.5
	temperatuurregelaar.i = 18.0
	temperatuurregelaar.d = 20.0


	while True:
		os.system('cls')
		processsim.start() #start process simulator
		processsim.niveausturing() #start niveauregeling

		if processsim.toevoer == True:
			print "Toevoer staat	open	debiet: %s  l/s	aan %s graden" % (str(format(processsim.act_toevoerdebiet, '.2f')), str(format(processsim.act_toevoertemperatuur, '.2f')))
		else:
			print "Toevoer staat	dicht	debiet: %s  l/s	aan %s graden" % (str(format(processsim.act_toevoerdebiet, '.2f')), str(format(processsim.act_toevoertemperatuur, '.2f')))

		if processsim.afvoer == True:
			print "Afvoer staat	open	debiet: %s  l/s" % str(format(processsim.act_afvoerdebiet, '.2f'))
		else:
			print "Afvoer staat	dicht"
		print ""
		print "Tankvolume:  " + str(format(processsim.tankvolume, '.2f')) + " l"
		print "Temperatuur: " + str(format(processsim.tanktemperatuur, '.2f'))+ " graden"

		niveauregelaar.pv = processsim.tankvolume
		niveauregelaar.w = 50
		niveauregelaar.start_regeling()
		processsim.toevoerregelklepstand = niveauregelaar.y

		temperatuurregelaar.pv = processsim.tanktemperatuur
		temperatuurregelaar.w = 60
		temperatuurregelaar.start_regeling()
		processsim.stoomklepstand = temperatuurregelaar.y

		print ""
		disp_PID("Niveauregelaar", niveauregelaar.p_actie, niveauregelaar.i_actie, niveauregelaar.d_actie, niveauregelaar.y)
		print ""
		disp_PID("Temperatuurregelaar", temperatuurregelaar.p_actie, temperatuurregelaar.i_actie, temperatuurregelaar.d_actie, temperatuurregelaar.y)

		time.sleep(0.15)


if __name__ == '__main__':
	Main()

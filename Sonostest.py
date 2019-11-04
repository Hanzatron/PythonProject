#!/usr/bin/python

#####################################################################################
# Sonostest.py																	HANS
# V1.0          25/10/2019

#####################################################################################
# pip install soco
#####################################################################################


import soco
ipadr = "192.168.0.219"
sonoszones = []
# zones = soco.discover(interface_addr= ipadr)
#
# print(zones)

class Sonoszone(object):
		def __init__(self):
			self.zone_list = []
			self.name_list = []

		def scan(self):
			self.zone_list = list(soco.discover(interface_addr= "192.168.0.219"))
			if len(self.zone_list) > 0:
				for zone in self.zone_list:
					self.name_list.append(zone.player_name)
					print(str(zone.player_name) + ": " + str(zone.get_current_transport_info()['current_transport_state']) + ": " + str(zone.get_current_track_info()['artist']))

def main():
		sonos = Sonoszone()
		sonos.scan()


if __name__ == '__main__':
	main()



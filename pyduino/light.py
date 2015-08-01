#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Tous droits réservés - 2013
# www.mon-club-elec.fr - Licence GPLv3

from __future__ import absolute_import
from __future__ import unicode_literals

# modules utiles 

### pour PWM - accès kernel + transposition C to Python ### 
#import fcntl # module pour fonction ioctl
#from ctypes import *
#import ctypes # module pour types C en Python 

import re # expression regulieres pour analyse de chaines

# serie 
try:
	import serial
except: 
	print "ATTENTION : Module Serial manquant : installer le paquet python-serial "

### les sous modules Pyduino utilisés par ce module ###
from .core.common import * # variables communes
from .core.base   import *
from .core.system import *
from .core.libs   import *

### declarations ###
# NB : les variables déclarées ici ne sont pas modifiables en dehors du module
# pour modifier la valeur d'une variable de ce module, la seule solution est de la réaffecter dans le programme 
# par exemple noLoop


# constantes Arduino like
INPUT  = "0"
OUTPUT = "1"
PULLUP = "8"

A0, A1, A2, A3, A4, A5  = 0, 1, 2, 3, 4, 5 # identifiant broches analogiques
PWM0, PWM1, PWM2, PWM3, PWM4, PWM5 = 3, 5, 6, 9, 10, 11 # identifiant broches PWM


### diverses classes utiles utilisées par les fonctions Pyduino ###

### Fonctions spécifiques pour une plateforme donnée: version PC desktop avec Arduino ###

### gestion broches E/S numériques ###

# pinMode 
def pinMode(pin, mode):
	print "Fonction non supportée : vous utilisez la version light"
	
# digitalWrite 
def digitalWrite(pin, state):
	print "Fonction non supportée : vous utilisez la version light"
	
# digitalRead
def digitalRead(pin):
	print "Fonction non supportée : vous utilisez la version light"

def toggle(pin): # inverse l'etat de la broche
	print "Fonction non supportée : vous utilisez la version light"

### gestion broches analogique ###

# analogRead - entrées analogiques 
def analogRead(pinAnalog):
	print "Fonction non supportée : vous utilisez la version light"

# analogReadmV - entrées analogiques - renvoie valeur en millivolts
def analogReadmV(pinAnalog):
	print "Fonction non supportée : vous utilisez la version light"

# analogWrite # idem Arduino en 0-255
def analogWrite(pinPWMIn, largeurIn):
	print "Fonction non supportée : vous utilisez la version light"

# analogWritePercent(pinPWMIn, largeurIn)=> rescale 0-100 vers 0-255
def analogWritePercent(pinPWMIn, largeurIn):
	print "Fonction non supportée : vous utilisez la version light"
	
### Fonctions Libs dédiées ###

# classe Uart pour communication série UART 

uartPort = None # objet global 

class Uart():
	# def __init__(self): # constructeur principal

	def begin(self,rateIn, *arg): # fonction pour émulation de begin... Ne fait rien... 
		global uartPort
		
		# configure pin 0 et 1 pour UART (mode = 3)
		#pinMode(RX,UART) - sur le pcduino
		#pinMode(TX,UART)
		
		### initialisation port serie uart ###
		try:
			if len(arg) == 0: # si pas d'arguments
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = 10) # initialisation port serie uart
				#uartPort=serial.Serial('/dev/ttyACM0', rateIn, timeout = 10) # initialisation port serie uart
				uartPort = serial.Serial('/dev/ttyACM0', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 10)
				uartPort.flushInput() # vide la file d'attente série
			if len(arg) == 1 : # si timeout
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
				uartPort = serial.Serial('/dev/ttyACM0', rateIn, timeout = arg[0]) # initialisation port serie uart
				uartPort.flushInput() # vide la file d'attente série
				
			print "Initialisation Port Serie : /dev/ttyACM0 @ " + str(rateIn) + " = OK " # affiche debug
			
		except:
			print  "Erreur lors initialisation port Serie" 
			
	def waitOK(self): # fonction pour attendre reponse OK suite initialisation
		out = None
		while not out : # attend une réponse 
			out = Uart.waitingAll() # lit tous les caracteres
		
		print out
	
	
	def println(self,text, *arg):  # message avec saut de ligne
		# Envoi chaine sur port serie uart 
		# Supporte formatage chaine façon Arduino avec DEC, BIN, OCT, HEX
		
		global uartPort
		
		# attention : arg est reçu sous la forme d'une liste, meme si 1 seul !
		text = str(text) # au cas où
		
		arg = list(arg) # conversion en list... évite problèmes.. 
		
		#print arg - debug
		
		if not len(arg) == 0: # si arg a au moins 1 element (nb : None renvoie True.. car arg existe..)
			if arg[0] == DEC and text.isdigit():
				# print(text)
				out = text
			elif arg[0] == BIN and text.isdigit():
				out = bin(int(text))
				# print(out)
			elif arg[0] == OCT and text.isdigit():
				out = oct(int(text))
				# print(out)
			elif arg[0] == HEX and text.isdigit():
				out = hex(int(text))
				# print(out)
		else: # si pas de formatage de chaine = affiche tel que 
			out = text
			# print(out)
		
		uartPort.write(out + chr(10)) # + saut de ligne 
		#print "Envoi sur le port serie Uart : " + out+chr(10) # debug
		
		# ajouter formatage Hexa, Bin.. cf fonction native bin... 
		# si type est long ou int
	"""
	def print(self,text): # affiche message sans saut de ligne
		
		#text=str(txt)
		
		print(text), # avec virgule pour affichage sans saus de ligne
	"""
	
	def available(self):
		global uartPort
		
		if uartPort.inWaiting() : return True
		else: return False
		
	def flush(self):
		global uartPort
		return uartPort.flush()
	
	def read(self):
		global uartPort
		return uartPort.read()
	
	def write(self, strIn):
		global uartPort
		uartPort.write(strIn)
		
	### lecture d'une ligne jusqu'a caractere de fin indique ###
	def waiting(self, *arg): # lecture d'une chaine en reception sur port serie 
		
		global uartPort
		
		if len(arg) == 0: endLine = "\n" # par defaut, saut de ligne
		elif len(arg) == 1: endLine = arg[0] # sinon utilise caractere voulu
		
		### variables de reception ###
		chaineIn = ""
		charIn = ""
		
		#delay(20) # laisse temps aux caracteres d'arriver
		
		while uartPort.inWaiting(): # tant que au moins un caractere en reception
			charIn = uartPort.read() # on lit le caractere
			#print charIn # debug
			
			if charIn == endLine: # si caractere fin ligne , on sort du while
				#print("caractere fin de ligne recu") # debug
				break # sort du while
			else: #tant que c'est pas le saut de ligne, on l'ajoute a la chaine 
				chaineIn = chaineIn + charIn
				# print chaineIn # debug
			
		### une fois sorti du while : on se retrouve ici - attention indentation ###
		if len(chaineIn) > 0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # affiche la chaine # debug
			return chaineIn  # renvoie la chaine 
		else:
			return False # si pas de chaine
	
	### lecture de tout ce qui arrive en réception ###
	def waitingAll(self): # lecture de tout en reception sur port serie 
		global uartPort
		
		### variables de reception ###
		chaineIn = ""
		charIn = ""
		
		#delay(20) # laisse temps aux caracteres d'arriver
		
		while uartPort.inWaiting(): # tant que au moins un caractere en reception
			charIn = uartPort.read() # on lit le caractere
			#print charIn # debug
			chaineIn = chaineIn + charIn
			# print chaineIn # debug
			
		### une fois sorti du while : on se retrouve ici - attention indentation ### 
		if len(chaineIn) > 0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # affiche la chaine # debug
			return chaineIn  # renvoie la chaine 
		else:
			return False # si pas de chaine


# fin classe Uart


### initialisation ###

Serial   = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal
Ethernet = Ethernet() # declare instance Ethernet implicite pour acces aux fonctions 
Uart     = Uart() # declare instance Uart implicite 

micros0Syst = microsSyst() # mémorise microsSyst au démarrage
millis0Syst = millisSyst() # mémorise millisSyst au démarrage

"""
# initialisation port série dès le début car va communiquer ave Arduino
Uart.begin(115200) # initialise comm' série 
delay(3000) # laisse le temps à la réponse d'arriver
Uart.waitOK() # attend réponse port serie OK 
"""


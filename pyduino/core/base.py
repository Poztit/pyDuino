#!/usr/bin/python
"""Module contenant les fonctions communes Arduino (temps, bits, rescale, random..)"""
### imports ###

### temps ###
import time
import datetime # gestion date

from threading import Timer # importe l'objet Timer du module threading

### math ###
# import math
from math import sin, cos, tan, sqrt, pow, min, max, radians, degrees, abs  # pour acces direct aux fonctions math..
import random as rd # pour fonctions aléatoires - alias pour éviter problème avec fonction arduino random()

### importe les autres modules Pyduino ###
from . import common # variables communes - doit être présente dans TOUS les modules

### Fonctions Pyduino : Core : Base ###

### fonction internes pyduino ###
def set_debug(boolIn):
    """Active les message de debug"""
    common.debug = boolIn # reference à common obligatoire pour affectation...

def debug(msg):
    print(msg)

### temps ###

def delay(ms):
	"""Stoppe le programme pendant la durée (en millisecondes) indiquée en paramètre"""
	int(ms)
	time.sleep(ms / 1000.0) # pause en secondes

def delayMicroseconds(us):
	"""Stoppe le programme pendant la durée (en microsecondes) indiquée en paramètre"""
	time.sleep(us / 1000000.0) # pause en secondes

def millisSyst():
	"""Retourne le nombre de millisecondes courant de l'horloge système"""
	return(int(round(time.time() * 1000))) # millisecondes de l'horloge systeme

def millis():
	"""Retourne le nombre de millisecondes depuis le debut du programme"""
	return millisSyst() - common.millis0Syst # renvoie difference entre milliSyst courant et millisSyst debut code

def microsSyst():
	"""Retourne le nombre de microsecondes courant de l'horloge systeme"""
	return(int(round(time.time() * 1000000))) # microsecondes de l'horloge systeme

def micros():
	"""Retourne le nombre de millisecondes depuis le debut du programme"""
	return microsSyst() - common.micros0Syst # renvoie difference entre microsSyst courant et microsSyst debut code

def timer(delaiIn, fonctionIn):
	"""Lance une fonction avec intervalle en ms"""
	Timer(delaiIn / 1000.0, fonctionIn).start() # relance le timer

def year():
	"""Retourne l'Année (RTC)"""
	return str(datetime.datetime.now().year)

def month():
	"""Returne le mois (RTC)"""
	if datetime.datetime.now().month < 10:
		return "0" + str(datetime.datetime.now().month) # ajoute 0 si < 10
	else:
		return str(datetime.datetime.now().month)

def day():
	"""Returne le jour (RTC)"""
	if datetime.datetime.now().day < 10:
		return "0" + str(datetime.datetime.now().day) # ajoute 0 si < 10
	else:
		return str(datetime.datetime.now().day)

def day_of_week():
	"""Returne le jour de la semaine (lundi = 1... Dim=7)"""
	return str(datetime.datetime.now().weekday() + 1)

def hour():
	"""Returne l'heure (%h)"""
	if datetime.datetime.now().hour < 10:
		return "0" + str(datetime.datetime.now().hour) # ajoute 0 si < 10
	else:
		return str(datetime.datetime.now().hour)

def minute():
	"""Returne la minute (%m)"""
	if datetime.datetime.now().minute < 10:
		return "0" + str(datetime.datetime.now().minute) # ajoute 0 si < 10
	else:
		return str(datetime.datetime.now().minute)

def second():
	"""Retourne la seconde (%s)"""
	if datetime.datetime.now().second < 10:
		return "0" + str(datetime.datetime.now().second) # ajoute 0 si < 10
	else:
		return str(datetime.datetime.now().second)

def unixtime():
	"Retourne l'heure UNIX"
	return str(int(time.time()))

# formes mixees

def now_time(*arg):
	"""Retourne l'heure (%h %m %s)"""
	if len(arg) == 0:
		return hour() + minute() + second()  # sans separateur
	elif len(arg) == 1:
		sep = str(arg[0])
		return hour() + sep + minute() + sep + second() # avec separateur

def today(*arg):
	"""Retourne la date (%d %m %y)"""
	if len(arg) == 0:
		return day() + month() + year() # sans séparateur
	elif len(arg) == 1:
		sep = str(arg[0])
		return day() + sep + month() + sep + year()
	elif len(arg) == 2:
		if arg[1] == -1: # forme inversee
			sep = str(arg[0])
			return year() + sep + month() + sep + day()

#def nowdatetime():
#	return today("/") + " " + nowtime(":")

def now_date_time(*arg):
	"""Retourne la date (%d %m %y) et l'heure (%h %m %s)"""
	if len(arg) == 0:
		return today("/") + " " + nowtime(":")
	elif len(arg) == 1:
		if arg[0] == -1:
			return today("/",-1) + " " + nowtime(":")
		else:
			return today("/") + " " + nowtime(":")


### MATH ###

def constrain(x, valMin, valMax):
	"""Contraint un nombre à rester dans une fourchette précise"""
	if x < valMin :
		return valMin
	elif valMax < x :
		return valMax
	else :
		return x

def rescale(valeur, in_min, in_max, out_min, out_max):
	"""Ré-étalonne un nombre d'une fourchette de valeur vers une autre fourchette"""
	return (valeur - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def sq(x):
	"""Calcule le carré de x"""
	return pow(x,2)

def randomSeed(x):
	"""Initialise le générateur de nombre pseudo-aléatoire"""
	rd.seed(x) # appelle fonction seed du module random

# random(max) et random(min,max) : renvoie valeur aléatoire entière
def random(*arg): # soit forme random(max), soit forme random(min,max)
	"""Retourne une valeur aléatoire entiere"""
	if len(arg) == 1:
		return rd.randint(0,arg[0])
	elif len(arg) == 2:
		return rd.randint(arg[0],arg[1])
	else:
		 return 0 # si argument invalide

### gestion de bits et octets ###
def lowByte(a):
	"""Retourne l'octet de poids faible de la valeur a"""
	out = bin(a) # '0b1011000101100101'
	out = out[2:] # enleve 0b '1011000101100101'
	out = out[-8:] # extrait 8 derniers caracteres - LSB a droite / MSB a gauche
	while len(out) < 8:out = "0" + out # complete jusqu'a 8 O/1
	out = "0b" + out # re-ajoute 0b
	return out

def highByte(a):
	"""Retourne l'octet de poids fort de la valeur a"""
	out = bin(a) # '0b1011000101100101'
	out = out[2:] # enleve 0b '1011000101100101'
	while len(out) > 8:out = out[:-8] # tant que plus de 8 chiffres, enleve 8 par 8 = octets low

	# une fois obtenu le highbyte, on complete les 0 jusqu'a 8 chiffres
	while len(out) < 8:out = "0" + out # complete jusqu'a 8 O/1
	out = "0b" + out # re-ajoute 0b
	return out


def bitRead(a, index):
	"""Lit le bit de rang index de la valeur a"""
	# le bit de poids faible a l'index 0
	out = bin(a) # '0b1011000101100101'
	out = out[2:] # enleve 0b '1011000101100101'
	out = out[len(out) - index - 1] # rang le plus faible = indice 0 = le plus a droite
	# extrait le caractere du bit voulu - LSB a droite / MSB a gauche
	#out="0b"+out # re-ajoute 0b
	return out


def bitWrite(a, index, value):
	"""Met le bit d'index voulu de la valeur a à la valeur indiquee (HIGH ou LOW)"""
	# le bit de poids faible a l'index 0
	out = bin(a) # '0b1011000101100101'
	out = out[2:] # enleve 0b '1011000101100101'
	out = list(out) # bascule en list
	out[len(out) - index - 1] = str(value) # rang le plus faible = indice 0 = le plus a droite
	#out=str(out) # rebascule en str - pb car reste format liste
	out = "".join(out) # rebascule en str - concatenation des caracteres
	# remplace le caractere du bit voulu - LSB a droite / MSB a gauche
	out = "0b" + out # re-ajoute 0b
	return out

def bitSet(a,index):
	"""Met le bit d'index voulu de la valeur a a HIGH"""
	# le bit de poids faible a l'index 0
	return bitWrite(a, index, 1) # met le bit voulu a 1 - Index 0 pour 1er bit poids faible


def bitClear(a,index):
	"""Met le bit d'index voulu de la valeur a a LOW"""
	# le bit de poids faible a l'index 0
	return bitWrite(a, index, 0) # met le bit voulu a 0 - Index 0 pour 1er bit poids faible


def bit(index):
	"""calcule la valeur du bit d'index specifie (le bits LSB a l'index 0)"""
	# le bits de poids faible a l'index 0 - calcule en fait 2 exposant index
	return pow(2, index) # cette fonction renvoie en fait la valeur 2^index

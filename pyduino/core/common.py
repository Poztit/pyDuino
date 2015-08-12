#!/usr/bin/python
"""Module contenant les variables communes
à l'ensemble des modules de la librairie
"""

# import utiles
import os

# déclarations utiles
HIGH = 1
LOW = 0

DEC = 10
BIN = 2
HEX = 16
OCT = 8

# constantes utiles pyDuino
NO_LOOP = False  # pour stopper loop
# DEBUG = False  # pour message debug

READ = "r"
WRITE = "w"
APPEND = "a"

# pour uart
UART = "3"
RX = 0
TX = 1
# Uart = None
# uartPort = None  # objet global

# objets internes utiles
# Serial = None
# Ethernet = None

# ## chemin de reference ##

# constantes de SELECTION
TEXT = "TEXT"
IMAGE = "IMAGE"
AUDIO = "AUDIO"
VIDEO = "VIDEO"

DIRS = {
    'home': os.getenv('HOME') + '/',
    'main': os.getenv('HOME') + '/',
    'data': {
        'text': 'data/text/',
        'audio': 'data/audio/',
        'image': 'data/images/',
        'video': 'data/videos/',
    },
    'src': {
        'text': 'source/text/',
        'audio': 'source/audio/',
        'image': 'source/images/',
        'video': 'source/videos/',
    }
}

# variables globales utiles - non initialisées ici
# important : pour réaffecter la valeur d'une variable partagée
# IL FAUT UTILISER LE NOM DU MODULE DE PARTAGE dans les modules les utilisant
# sinon c'est une variable globale module qui est créée,
# pas une variable partagée...
PLATFORM = None

# fichiers broches E/S
# pathMode = None
# pathState = None

# constantes Arduino like
# INPUT = None
# OUTPUT = None
# PULLUP = None

# identifiants hardware E/S
# A0, A1, A2, A3, A4, A5 = None, None, None, None, None, None
# PWM = None
# PWM0, PWM1, PWM2, PWM3, PWM4, PWM5 = None, None, None, None, None, None

# variables internes utiles
MICROS_SYST_INIT = 0
MILLIS_SYST_INIT = 0

#!/usr/bin/python

# Par F. ILLIEN - Tous droits réservés - 2015
# www.mon-club-elec.fr - Licence GPLv3

# ### Expressions regulieres ###
import re  # Expression regulieres pour analyse de chaines

# Serie Uart
import serial

# ### Pour PWM - accès kernel + transposition C to Python ###
import fcntl  # Module pour fonction ioctl
import ctypes  # Module pour types C en Python

# ### Les sous modules Pyduino utilisés par ce module ###
from .core.base import (delay, delayMicroseconds, millisSyst, microsSyst,
                        millis, micros, timer, year, month, day, day_of_week,
                        hour, minute, second, unixtime, now_time,
                        today, now_date_time,
                        constrain, rescale, sq, randomSeed, random,
                        lowByte, highByte, bitRead, bitWrite,
                        bitSet, bitClear, bit)

from .core.system import (MailServer, EthernetServer, Ethernet, Serial,
                          executeCmd, executeCmdWait, executeCmdOutput,
                          homePath, mainPath, setMainPath, dataPath,
                          setDataPath, sourcesPath, setSourcesPath, exists,
                          isdir, isfile, dirname, currentdir, changedir,
                          rewindDirectory, mkdir, rmdir, listdirs,
                          listfiles, dircontent, remove, size,
                          appendDataLine, httpResponse)

from .core.libs import LiquidCrystal, Servo

# ### declarations ###
# NB : les variables déclarées ici ne sont pas modifiables en dehors du module
# pour modifier la valeur d'une variable de ce module,
# la seule solution est de la réaffecter dans le programme
# par exemple noLoop ou de passer par un fichier commun...

# sur le pcDuino, la plupart des operations passent par des fichiers systeme
# important : pour réaffecter la valeur d'une variable partagée
# IL FAUT UTILISER LE NOM DU MODULE
# sinon variable globale module, pas partagée...

PLATFORM = "RPI"

# Fichiers broches E/S raspberryPi
pathMain = "/sys/class/gpio/"

# Definition des broches E/S - version B
pinList = {
    "17": '17',
    "18": '18',
    "27": '27',
    "22": '22',
    "23": '23',
    "24": '24',
    "25": '25',
    "4": '4'}

# A0, A1, A2, A3, A4, A5 = 0, 1, 2, 3, 4, 5 # Identifiant broches analogiques
# PWM0 = 1 # Identifiant broches PWM


# Constantes Arduino like spécifique de la plateforme utilisée
INPUT = "in"
OUTPUT = "out"
PULLUP = "up"  # Accepter par la commande gpio

# ### Fonctions spécifiques pour une plateforme donnée: Version RaspberryPi ###


# ### Broche logique ###
def export(pin):
    try:
        file = open(pathMain + "export", 'w')  # Ouvre le fichier en ecriture
        file.write(pinList[pin])  # Ecrie le pin a exporter
        file.close()
    except:
        print("ERREUR : Impossible d'ouvrir la broche")
        return -1
    else:
        return 0


def pinMode(pin, mode):
    mode = str(mode)  # Mode de fonctionnement (str)
    pin = str(pin)
    if export(pin) == 0:
        # gpio mode <pin> in/out/pwm/clock/up/down/tri
        if mode == INPUT or mode == OUTPUT:  # Si in ou out
            # En acces direct = plus rapide
            try:
                file = open(pathMain + "gpio/" + pinList[pin] + "/direction",
                            'w')
                # Ouvre le fichier en ecriture
                file.write(mode)  # Ecrie l'etat du pin demande
                file.close()
            except:
                return -1
            else:
                return 0
        elif mode == PULLUP:  # Sinon = si up
            # Fixe le mode de la broche E/S via ligne commande gpio
            cmd = "gpio mode " + pin + " " + mode
            subprocess.Popen(cmd, shell=True)
            return 0
    else:
        return -1


def digitalWrite(pin, state):
    pin = str(pin)
    state = str(state)  # Transforme en chaine

    # gpio mode <pin> in/out/pwm/clock/up/down/tri

    # Met la broche dans etat voulu via ligne de commande gpio
    # cmd="gpio write "+str(pin)+" "+str(state)
    # subprocess.Popen(cmd, shell=True)
    # print cmd # debug

    # En acces direct = plus rapide
    try:
        file = open(pathMain + "gpio/" + pinList[pin] + "/value", 'w')
        # Ouvre le fichier en écriture
        file.write(state)
        file.close()
    except:
        # print "ERREUR : Impossible d'ecrire sur la broche"
        return -1
    else:
        return 0


def digitalRead(pin):
    pin = str(pin)
    try:
        # Lit etat de la broche en acces direct
        file = open(pathMain + "gpio/" + pinList[pin] + "/value", 'r')
        # Ouvre le fichier en lecture
        file.seek(0)  # Se place au debut du fichier
        state = file.read()  # Lit le fichier
        file.close()
    except:
        # print "ERREUR : Impossible de lire la broche"
        return -1
    else:
        return int(state)  # Renvoie valeur entiere


def toggle(pin):  # Inverse l'etat de la broche
    if digitalRead(pin) == HIGH:
        digitalWrite(pin, LOW)
        return LOW
    else:
        digitalWrite(pin, HIGH)
        return HIGH


# ### Broche analogique ###
# analogRead
def analogRead(pin):
    print("ERREUR : analogRead non disponible sur le RaspberryPi")
    return 0  # Renvoie la valeur


# analogWrite = generation pwm
def analogWrite(pin, value):
    pin = str(pin)
    value = int(rescale(value, 0, 255, 0, 1023))
    # Fixe le mode pwm pour la broche E/S via ligne commande gpio
    cmd = "gpio mode " + pin + " " + "pwm"
    subprocess.Popen(cmd, shell=True)
    # gpio pwm <pin> <value> avec value entre 0 et 1023
    # Fixe pwm via ligne commande gpio
    cmd = "gpio pwm " + pin + " " + str(value)
    subprocess.Popen(cmd, shell=True)


def analogWritePercent(pin, value):
    analogWrite(pin, rescale(value, 0, 100, 0, 255))
    # Re-echelonne valeur 0-100% vers 0-255


# ### Fonctions Libs dédiées ###

class Uart():
    # def __init__(self): # constructeur principal
    def begin(self, rateIn, *arg):  # fonction initialisation port serie
        # arg = rien ou timeout ou timeout et port a utiliser
        global uartPort

        # configure pin 0 et 1 pour UART (mode = 3)
        pinMode(RX, UART)
        pinMode(TX, UART)

        # -- initialisation port serie uart
        try:
            if len(arg) == 0:  # si pas d'arguments
                # uartPort=serial.Serial('/dev/ttyS1', rateIn,
                # serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE,
                # timeout = 10) # initialisation port serie uart
                uartPort = serial.Serial('/dev/ttyS1', rateIn, timeout=10)
                # initialisation port serie uart
            elif len(arg) == 1:  # si timeout
                # uartPort=serial.Serial('/dev/ttyS1', rateIn,
                # serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE,
                # timeout = arg[0]) # initialisation port serie uart
                uartPort = serial.Serial('/dev/ttyS1', rateIn, timeout=arg[0])
                # initialisation port serie uart
            elif len(arg) == 2:  # si timeout et port
                # uartPort=serial.Serial('/dev/ttyS1', rateIn,
                # serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE,
                # timeout = arg[0])
                # initialisation port serie uart
                uartPort = serial.Serial(arg[1], rateIn, timeout=arg[0])
                # initialisation port serie uart
        except:
            raise "Erreur lors initialisation port Serie"

    def println(self, text, *arg):  # message avec saut de ligne
        # Envoi chaine sur port serie uart
        # Supporte formatage chaine façon Arduino avec DEC, BIN, OCT, HEX
        global uartPort
        # attention : arg est reçu sous la forme d'une liste, meme si 1 seul !
        text = str(text)  # au cas où
        # print "text =" + text # debug

        arg = list(arg)  # conversion en list... évite problèmes..

        # print arg - debug

        if not len(arg) == 0:
            # si arg a au moins 1 element
            # (nb : None renvoie True.. car arg existe..)
            if arg[0] == DEC and text.isdigit():
                out = text
                # print(out) # debug
            elif arg[0] == BIN and text.isdigit():
                out = bin(int(text))
                # print(out) # debug
            elif arg[0] == OCT and text.isdigit():
                out = oct(int(text))
                # print(out) # debug
            elif arg[0] == HEX and text.isdigit():
                out = hex(int(text))
                # print(out) # debug
        else:  # si pas de formatage de chaine = affiche tel que
            out = text
            # print(out) # debug

        uartPort.write(out + chr(10))  # + saut de ligne
        # print "Envoi sur le port serie Uart : " + out+chr(10) # debug
        uartPort.flush()
        # ajouter formatage Hexa, Bin.. cf fonction native bin...
        # si type est long ou int

    def available(self):
        global uartPort

        if uartPort.inWaiting():
            return True
        else:
            return False

    def flush(self):
        global uartPort
        return uartPort.flush()

    def read(self):
        global uartPort
        return uartPort.read()

    def write(self, strIn):
        global uartPort
        uartPort.write(strIn)

    # --- lecture d'une ligne jusqu'a caractere de fin indique
    def waiting(self, *arg):
        # lecture d'une chaine en reception sur port serie
        global uartPort

        if len(arg) == 0:
            endLine = "\n"  # par defaut, saut de ligne
        elif len(arg) == 1:
            endLine = arg[0]  # sinon utilise caractere voulu

        # -- variables de reception --
        chaineIn = ""
        charIn = ""

        # delay(20) # laisse temps aux caracteres d'arriver

        while uartPort.inWaiting():
            # tant que au moins un caractere en reception
            charIn = uartPort.read()  # on lit le caractere
            # print charIn # debug

            if charIn == endLine:
                # si caractere fin ligne , on sort du while
                # print("caractere fin de ligne recu") # debug
                break  # sort du while
            else:
                # tant que c'est pas le saut de ligne, on l'ajoute a la chaine
                chaineIn = chaineIn + charIn
                # print chaineIn # debug

        # Une fois sorti du while : on se retrouve ici - attention indentation
        if len(chaineIn) > 0:  # ... pour ne pas avoir d'affichage si ""
            # print(chaineIn) # affiche la chaine # debug
            return chaineIn  # renvoie la chaine
        else:
            return False  # si pas de chaine

    # --- lecture de tout ce qui arrive en réception
    def waitingAll(self):  # lecture de tout en reception sur port serie

        global uartPort

        # -- variables de reception --
        chaineIn = ""
        charIn = ""

        # delay(20) # laisse temps aux caracteres d'arriver

        while uartPort.inWaiting():
            # tant que au moins un caractere en reception
            charIn = uartPort.read()  # on lit le caractere
            # print charIn # debug
            chaineIn = chaineIn + charIn
            # print chaineIn # debug

        # Une fois sorti du while : on se retrouve ici - attention indentation
        if len(chaineIn) > 0:  # ... pour ne pas avoir d'affichage si ""
            # print(chaineIn) # affiche la chaine # debug
            return chaineIn  # renvoie la chaine
        else:
            return False  # si pas de chaine

# ajouter write / read   / flush


# ### Initialisation###

Serial = Serial()
# Declare une instance Serial pour acces aux fonctions depuis code principal
Ethernet = Ethernet()
# Declare instance Ethernet implicite pour acces aux fonctions
Uart = Uart()
# Declare instance Uart implicite

micros0Syst = microsSyst()  # Mémorise microsSyst au démarrage
millis0Syst = millisSyst()  # Mémorise millisSyst au démarrage

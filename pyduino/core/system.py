#!/usr/bin/python
"""fichier contenant les fonctions dites «système»
À savoir Ethernet, Mail, Serial, Fichiers
et répertoires (équiv. SD) et ligne de commande
"""

# ### imports ###

# ### système ###
import subprocess
# import getpass # pour connaitre utilisateur systeme
import os  # gestion des chemins

# reseau
import socket
import smtplib  # serveur mail
import netifaces  # pour acces interf reseaux - dépendance : python-netifaces

# ### importe les autres modules Pyduino ###
from .common import (TEXT, IMAGE, AUDIO, VIDEO, DEC, BIN, OCT, HEX, main_dir,
                     data_dir_text, data_dir_image,
                     data_dir_audio, data_dir_video,
                     src_dir_text, src_dir_image,
                     src_dir_audio, src_dir_video)


# ### Fonctions Système ####
# ## Console ###
# ### Système : ligne de commande ###
def executeCmd(cmd):
    """Execute la ligne de commande systeme passee en parametre
    sans attendre la fin de l'execution
    """

    # p=subprocess.Popen(cmd, shell=True) # exécute la commande et continue
    p = subprocess.Popen("exec " + cmd, shell=True)
    # exécute la commande et continue
    # exec pour processus renvoyé sinon c'est le shell...
    # la sortie standard et la sortie erreur ne sont pas interceptées
    # donc s'affieront dans le Terminal mais non accessible depuis le code..
    return p


def executeCmdWait(cmd):
    """Execute la ligne de commande systeme passee en parametre
    et attend la fin de l'execution
    """
    # subprocess.Popen(cmd, shell=False).wait
    # subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait
    # attention - wait attend pas si SHell=True !

    # en cas de commande : cmd -params "chaine"
    subcmd = cmd.split("\"")
    subsubcmd = subcmd[0].split(" ")
    # pour avoir format liste [ arge, arg, arg] attendu par check_call
    # pose probleme si chaine en param
    try:
        subsubcmd.remove('')  # enleve '' car bloque commande si present...
    except:
        pass

    if len(subcmd) == 1:  # si pas de chaine
        subprocess.check_call(subsubcmd)
    elif len(subcmd) > 1:
        subsubcmd.append("\"" + str(subcmd[1]) + "\"")
        # ajoute la chaine en + encadree par " "
        subprocess.check_call(subsubcmd)


def executeCmdOutput(cmd):
    """Execute la ligne de commande systeme passee en parametre
    capture la sortie console et attend la fin de l'execution
    """

    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    # execute la commande

    out = pipe.read()  # lit la sortie console
    pipe.close()  # ferme la sortie console

    return out


# ### fichiers et data texte ####

# ### les fonctions fichiers de la lib' Pyduino.. ###
def homePath():
    """Retourne le chemin vers le Home"""
    return os.getenv("HOME") + "/"


def mainPath():
    return main_dir


def setMainPath(pathIn):
    global main_dir
    main_dir = pathIn


# ### (get) data Path ###
def dataPath(typeIn):
    """Retourne le chemin vers le type de données spécifié en argument"""
    if typeIn == TEXT:
        return data_dir_text
    elif typeIn == IMAGE:
        return data_dir_image
    elif typeIn == AUDIO:
        return data_dir_audio
    elif typeIn == VIDEO:
        return data_dir_video
    else:
        print("Erreur : choisir parmi TEXT, IMAGE, AUDIO, VIDEO")


# ### set data Path ###
def setDataPath(typeIn, dirIn):
    """Permet de spécifier le chemin
    vers le type de données spécifié en argument
    """
    if typeIn == TEXT:
        global data_dir_text
        data_dir_text = dirIn
    elif typeIn == IMAGE:
        global data_dir_image
        data_dir_image = dirIn
    elif typeIn == AUDIO:
        global data_dir_audio
        data_dir_audio = dirIn
    elif typeIn == VIDEO:
        global data_dir_video
        data_dir_video = dirIn
    else:
        print("Erreur : choisir parmi TEXT, IMAGE, AUDIO, VIDEO")


# ### (get) source Path ###
def sourcesPath(typeIn):
    if typeIn == TEXT:
        return src_dir_text
    elif typeIn == IMAGE:
        return src_dir_image
    elif typeIn == AUDIO:
        return src_dir_audio
    elif typeIn == VIDEO:
        return src_dir_video
    else:
        print("Erreur : choisir parmi TEXT, IMAGE, AUDIO, VIDEO")


# ### set sources Path ###
def setSourcesPath(typeIn, dirIn):
    if typeIn == TEXT:
        global src_dir_text
        src_dir_text = dirIn
    elif typeIn == IMAGE:
        global src_dir_image
        src_dir_image = dirIn
    elif typeIn == AUDIO:
        global src_dir_audio
        src_dir_audio = dirIn
    elif typeIn == VIDEO:
        global src_dir_video
        src_dir_video = dirIn
    else:
        print("Erreur : choisir parmi TEXT, IMAGE, AUDIO, VIDEO")


# ### fonction gestion répertoires / fichiers ###

def exists(filepathIn):
    """Teste si le chemin ou fichier existe"""
    # try:
    #     with open(filepathIn): return True
    # except IOError:
    #     print "Le fichier n'existe pas" # debug
    #     return False
    if os.path.isfile(filepathIn) or os.path.isdir(filepathIn):
        return True
    else:
        return False


def isdir(pathIn):
    """Verifie si l'argument est un repertoire ou non"""
    return os.path.isdir(pathIn)


def isfile(filepathIn):
    """Verifie si l'argument est un fichier ou non"""
    return os.path.isfile(filepathIn)


def dirname(pathIn):
    """Retourne le nom du repertoire"""
    return os.path.dirname(pathIn) + "/"


def currentdir():
    """Retourne le nom du repertoire courant"""
    return os.getcwd() + "/"


def changedir(pathIn):
    """Changer de repertoire courant"""
    os.chdir(pathIn)


def rewindDirectory():
    os.chdir("..")  # remonte d'un niveau


def mkdir(pathIn):
    """Crée le répertoire si il n'existe pas"""
    # os.mkdir(pathIn) ne créée pas les rep intermediaires
    try:
        os.makedirs(pathIn)  # cree les rep intermediaires
        return True
    except OSError:
        print("Probleme creation")
        return False


def rmdir(pathIn):
    """Efface le répertoire"""
    try:
        os.rmdir(pathIn)  # efface repertoire
        return True
    except OSError:
        print("Effacement impossible")
        return False


def listdirs(pathIn):
    """Liste les repertoires"""
    if exists(pathIn):
        onlydirs = [f for f in os.listdir(pathIn)
                    if os.path.isdir(os.path.join(pathIn, f))]
        return sorted(onlydirs)
    else:
        return False


def listfiles(pathIn):
    """Liste les fichiers"""
    if exists(pathIn):
        onlyfiles = [f for f in os.listdir(pathIn)
                     if os.path.isfile(os.path.join(pathIn, f))]
        return sorted(onlyfiles)
    else:
        return False


def dircontent(pathIn):
    """Liste le contenu du répertoire (les repertoires suivi des fichiers)"""
    if exists(pathIn):
        out = ""
        for dirnames in listdirs(pathIn):  # les rép
            out = out + dirnames + "/\n"

        for filenames in listfiles(pathIn):  # les fichiers
            out = out + filenames + "\n"

        return out
    else:
        return False


# open(path, mode) avec mode parmi r, w ou a
# fonction native Python --> renvoie un objet file

def remove(filepathIn):
    """Efface le fichier indiqué"""
    try:
        os.remove(filepathIn)  # efface fichier
        return True
    except OSError:
        print("Effacement impossible")
        return False


# ### fonctions objet file ###
# voir http://docs.python.org/2/library/stdtypes.html#bltin-file-objects

# close () -- Python --V
# http://docs.python.org/2/library/stdtypes.html#file.close

# flush () -- Python --V
# http://docs.python.org/2/library/stdtypes.html#file.flush

# name() -- Python --V
# http://docs.python.org/2/library/stdtypes.html#file.name

# tell () -- Python --V
# http://docs.python.org/2/library/stdtypes.html#file.tell

# seek () -- Python --V
# http://docs.python.org/2/library/stdtypes.html#file.seek

# size () -- Python -->
def size(filepathIn):
    """Retourne la taille de la cible"""
    return os.path.getsize(filepathIn)

# read () -- Python --V
# http://docs.python.org/2/library/stdtypes.html#file.read

# write () -- Python --V
# http://docs.python.org/2/library/stdtypes.html#file.write

# readLine() -- Python --V
# http://docs.python.org/2/library/stdtypes.html#file.readline

# readLines() -- Python --V
# http://docs.python.org/2/library/stdtypes.html#file.readlines


# ### fonctions Pyduino utiles files ###
def appendDataLine(filepathIn, dataIn):
    if exists(filepathIn):
        dataFile = open(filepathIn, 'a')  # ouvre pour ajout donnees
        dataFile.write(str(dataIn) + "\n")
        dataFile.close()
    elif not exists(filepathIn):
        dataFile = open(filepathIn, 'w')  # cree fichier pour ajout donnees
        dataFile.write(str(dataIn) + "\n")
        dataFile.close()


# ## création des chemins si existent pas - mis après déclaration fonctions ##
if not exists(homePath() + data_dir_text):
    mkdir(homePath() + data_dir_text)  # creation si existe pas
if not exists(homePath() + data_dir_audio):
    mkdir(homePath() + data_dir_audio)  # creation si existe pas
if not exists(homePath() + data_dir_image):
    mkdir(homePath() + data_dir_image)  # creation si existe pas
if not exists(homePath() + data_dir_video):
    mkdir(homePath() + data_dir_video)  # creation si existe pas

if not exists(homePath() + src_dir_text):
    mkdir(homePath() + src_dir_text)  # creation si existe pas
if not exists(homePath() + src_dir_audio):
    mkdir(homePath() + src_dir_audio)  # creation si existe pas
if not exists(homePath() + src_dir_image):
    mkdir(homePath() + src_dir_image)  # creation si existe pas
if not exists(homePath() + src_dir_video):
    mkdir(homePath() + src_dir_video)  # creation si existe pas


# #### Reseau ####
def httpResponse():  # reponse HTTP par defaut
    """Retourne la reponse HTTP par defaut"""
    return "HTTP/1.0 200 OK\nContent-Type: text/html\nConnnection: close"
    # ligne vide finale obligatoire ++


class Serial():
    """Émule l'affichage des message en console"""
    # def __init__(self): # constructeur principal

    def println(self, text, *arg):  # message avec saut de ligne
        # Emulation Serial.println dans console systeme
        # Supporte formatage chaine façon Arduino avec DEC, BIN, OCT, HEX

        # attention : arg est reçu sous la forme d'une liste, meme si 1 seul !
        text = str(text)  # au cas où
        arg = list(arg)  # conversion en list... évite problèmes..

        if not len(arg) == 0:
            if arg[0] == DEC and text.isdigit():
                print(text)
            elif arg[0] == BIN and text.isdigit():
                print(bin(int(text)))
            elif arg[0] == OCT and text.isdigit():
                print(oct(int(text)))
            elif arg[0] == HEX and text.isdigit():
                print(hex(int(text)))
            else:  # si pas de formatage de chaine = affiche tel que
                print(text)

        # ajouter formatage Hexa, Bin.. cf fonction native bin...
        # si type est long ou int

    # def print(self,text): # affiche message sans saut de ligne

        # text=str(txt)

        # print(text), # avec virgule pour affichage sans saus de ligne
    def begin(self, rate):
        """Émulation de begin... Ne fait rien..."""
        pass


class Ethernet():
    """Émule l'accès au materiel réseau"""
    # def __init__(self): # constructeur principal

    def localIP(self):
        """Retourne l'IP locale"""
        # return socket.gethostbyname(socket.gethostname()) ne fonctionne pas
        # print socket.gethostbyname(socket.getfqdn())
        # obtenir IP système active - ne marche pas...

        # ce code dépend de la distro et tout changement le rend caduque
        # sortieConsole=executeCmdOutput("ifconfig")
        # execute commande et attend 5s

        # print sortieConsole - debug

        # result=(re.findall(r'^.*inet  adr:(.*\..*\..*\..*) .*$',
        #            sortieConsole, re.M))
        # extrait *.*.*.* de la chaine
        # au format inet adr: *.*.*.* si la chaine est au format valide
        # + tolerant fin chaine

        # result=(re.findall(r'^.*inet ad.*r:(.*\..*\..*\..*)  B.*$',
        #            sortieConsole, re.M))
        # ad.*r car selon syst c'est addr ou adr .. !
        # print result
        # if len(result)>0 :return result[0]
        # else: return

        addr = netifaces.ifaddresses('eth0')
        return addr[netifaces.AF_INET][0]['addr']
        # récupère l'élément voulu des adresses
        # puis accès élément 0 (un dico) puis accès addr du dico


class EthernetServer(socket.socket):
    """Classe de serveur HTTP"""
    # attention recoit classe du module, pas le module !

    def __init__(self, ipIn, portIn):  # constructeur principal
        # self=socket.socket( socket.AF_INET,socket.SOCK_STREAM)
        # self est un objet serveur

        # self.bind((ipIn,portIn))
        # lie l'adresse et port au serveur # '' pour interface disponible

        (super(EthernetServer, self)
            .__init__(socket.AF_INET, socket.SOCK_STREAM))
        # initialise Ethernet class en tant que socket...

        # a present self dispose de toutes les fonctions socket !
        # print type(self) # debug
        # print dir(self) # debug

        # self.socket(socket.AF_INET,socket.SOCK_STREAM)
        # self.socket( AF_INET,SOCK_STREAM)
        # socket.socket( AF_INET,SOCK_STREAM)
        # socket.socket([family[, type[, proto]]])

        self.bind((ipIn, portIn))
        # lie l'adresse et port au serveur # '' pour interface disponible

    def begin(self, *arg):
        """"""
        if len(arg) == 0:  # si pas de nombre client precise
            self.listen(5)  # fixe a 5
        elif len(arg) == 1:  # si nombre client
            self.listen(arg[0])  # fixe au nombre voulu

    def clientAvailable(self):
        """Attend un client entrant"""
        client, adresseDistante = self.accept()  # attend client entrant
        return client, adresseDistante[0]
        # l'adresse recue est un tuple - ip est le 1er element

    def readDataFrom(self, clientDistantIn, *arg):
        # arg = rien ou maxIn
        if len(arg) == 0:
            maxIn = 1024
        elif len(arg) == 1:
            maxIn = arg[0]

        chaineRecue = clientDistantIn.recv(maxIn)  # .strip()
        chaineRecue.decode('utf-8')
        return chaineRecue

    def writeDataTo(self, clientDistantIn, reponseIn):
        clientDistantIn.send(reponseIn)  # préférer sendAll ?

    def sendResponse(self, clientDistantIn, responseIn):
        # fonction d'envoi reponse Http + chaine + saut de ligne

        responseOut = httpResponse() + responseIn + "\n"
        # entete http OK 200 automatique fournie par la librairie Pyduino

        # self.writeDataTo(clientDistantIn, responseOut)
        # envoie donnees vers client d'un coup - pour test - hors try

        try:
            self.writeDataTo(clientDistantIn, responseOut)
            # envoie donnees vers client d'un coup
            return True
        except:
            return False

    # fin sendResponse

# class EthernetClient(socket.socket) :
#    attention recoit classe du module, pas le module !
#    def read():
#        #--- requete client ---
#        rec=self.recv(1024).strip()
#        rec.decode('utf-8')
#        print rec

# close() -- module socket -- classe socket -- Python ---------------\
# http://docs.python.org/2/library/socket.html#socket.socket.close <-|


class MailServer():
    """Classe de serveur mail"""
    def __init__(self):
        self.name = ""
        self.port = 0
        self.fromMail = ""
        self.fromPassword = ""
        self.toMail = ""
        self.subject = ""
        self.msg = ""
        self.imageToJoin = ""

    def setName(self, nameIn):
        """Attribut le nom du serveur au quel envoyer le mail"""
        self.name = nameIn

    def setPort(self, portIn):
        """Attribut le port du serveur au quel envoyer"""
        self.port = portIn

    def setFromMail(self, fromMailIn):
        self.fromMail = fromMailIn

    def setFromPassword(self, fromPasswordIn):
        self.fromPassword = fromPasswordIn

    def setToMail(self, toMailIn):
        self.toMail = toMailIn

    def setSubject(self, subjectIn):
        """Attribut le sujet du message à envoyer"""
        self.subject = subjectIn

    def setMsg(self, msgIn):
        """Attribut le message à envoyer"""
        self.msg = msgIn

    def setImageToJoin(self, pathIn):
        self.imageToJoin = pathIn

    def getHeader(self):
        # header
        header = 'To:' + self.toMail + '\n'
        header = header + 'From:' + self.fromMail + '\n'
        header = header + 'Subject:' + self.subject + '\n'
        return header

    def sendMail(self):
        """Envoi le mail"""
        from email.mime.text import MIMEText
        # connexion serveur smtp
        smtpserver = smtplib.SMTP(self.name, self.port)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        print(smtpserver.login(self.fromMail, self.fromPassword))

        # preparation du mail
        # mail=self.getHeader()+self.msg+"\n\n"
        # print mail # debug

        # preparation du mail - utilise module email
        mail = MIMEText(self.msg)
        mail['Subject'] = self.subject
        mail['From'] = self.fromMail
        mail['To'] = self.toMail

        # envoi du mail
        smtpserver.sendmail(self.fromMail, [self.toMail], mail.as_string())

        # fermeture serveur smtp
        # smtpserver.close()
        print(smtpserver.quit())

    def sendMailImage(self):

        from email.mime.text import MIMEText
        from email.mime.image import MIMEImage
        from email.mime.multipart import MIMEMultipart

        # connexion serveur smtp
        smtpserver = smtplib.SMTP(self.name, self.port)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(self.fromMail, self.fromPassword)

        # preparation du mail
        # mail=self.getHeader()+self.msg+"\n\n"
        # print mail # debug

        # preparation du mail - utilise module email
        # mail = MIMEText(self.msg)
        mail = MIMEMultipart()
        mail['Subject'] = self.subject
        mail['From'] = self.fromMail
        mail['To'] = self.toMail
        mail.preamble = self.subject

        msg = MIMEText(self.msg)  # le texte
        mail.attach(msg)  # attache le texte au mail

        fp = open(self.imageToJoin, 'rb')  # ouvre l'image en lecture binaire
        img = MIMEImage(fp.read())  # lit l'image et récupere l'objet obtenu
        fp.close()  # ferme le fichier

        mail.attach(img)  # attache l'image au mail

        # envoi du mail
        smtpserver.sendmail(self.fromMail, [self.toMail], mail.as_string())

        # fermeture serveur smtp
        # smtpserver.close()
        smtpserver.quit()
# ### fin serveur mail ###

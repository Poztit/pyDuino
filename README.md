# La librairie pyDuino

La librairie Pyduino apporte une couche d'abstraction au langage Python afin de pouvoir utiliser les broches E/S de mini-PC tels que RaspberryPi ou le pcDuino avec des instructions identiques au langage Arduino.

## Versions disponibles

La librairie existe en plusieurs versions :

* en version standard qui implémente :
	* les fonctions Arduino standards
	* les fonctions système (console, ligne de commande)
	* les fonctions de gestion des fichiers et données texte (équivalent librairie SD)
	* les fonctions de gestion du réseau (équivalent de la librairie Ethernet)
	* les fonctions UART
	* les fonctions gestion de servomoteurs (équivalent librairie Servo)
	* les fonctions de gestion d'un afficheur LCD (équivalent librairie LiquiCrystal)
	* à venir : les fonctions SPI, I2C
	* à venir : les motorisations : moteurs CC, pas à pas

* en version multimédia qui implémente en plus :
	* la capture d'image, l'inscrustation de texte dans image
	* la lecture de fichier sons (bruitages, etc...) à partir de fichiers aux formats standards
	* la capture audio
	* la synthèse vocale
	* la reconnaissance vocale en mode connecté
	* à venir : reconnaissance de lettres dans image, détection objet coloré dans image..

## Installation

Pour installer pyDuino il suffit d'executer :
```bash
python setup.py install
```
dans un terminal (shell).

## Exemples

Les codes d'exemple sont rassemblés [ici](https://github.com/sensor56/pyduino-exemples)

## Structure de pyDuino

    * core
        * common.py : les variables communes à l'ensemble des fichiers de la librairie.
        * base.py : les fonctions communes Arduino (temps, bits, rescale, random..).
        * libs.py : les fonctions des «librairies» Arduino (LCD, Servo, à venir I2C, SPI, Stepper, etc...).
        * system.py : les fonctions dites «système», à savoir Ethernet, Mail, Serial, Fichiers et répertoires * (équiv. SD) et ligne de commande.
    * multimedia

    * pcduino.py : version adaptée à la plateforme pcDuino.
    * rpi.py : version adaptée à la plateforme RaspberryPi B.
    * light.py : version sans le support «hardware» pouvant être utilisé sur n'importe quel système Gnu/Linux.
    * arduino_pc.py : version permetant de controler une carte Arduino avec Python via la liaison serie d'un PC. Il faut préalablement flasher le programme arduino_live.ino (qui est un interpréteur de commande) sur l'Arduino.

Happy coding !!!

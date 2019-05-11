# Téléinfo compteur Linky

Ce script python permet de récupérer les informations de votre compteur linky via la liaison série du port usb.
Ce script a été réalisé pour un raspbery zero mais est facillement adaptable à pour un autre équipement.

> **A noter**
> Ce script a été testé sur un compteur Linky monophasé en mode consomateur. Il se base sur ce [documentation de spécifications](linky-tic-specs.pdf)

## Montage

Utiliser un cable USB et connecter sur le RPI 
- La masse (fil noir) sur le PIN 6 (GND)
- Data+ (fil blanc) sur le PIN 10 (Rx)

## Communication 

Les caractéristiques de la liaison série sont les suivantes : 
- 1 bit de start (0 logique)
- 7 bits
- 1 bit de parité pair
- 1 bit de stop (1 logique)

**Tester la liaison**
Si la communicaion fonctionne correctement vous devriez voir une information par ligne.
*Utilisez Ctrl+A - K pour quiter screen.*
```bash
$ screen /dev/ttyS0 9600,cs7,parenb,-parodd,-cstopb
```

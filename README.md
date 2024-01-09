# Tembo-PickupAutomatisation

Deze codes worden gebruikt voor proof of concept voor het bedrijf Tembo. Het systeem was ontworpen om erachter te komen of het geheel geautomatiseerd kon worden. hierbij wordt er gebruikt gemaakt van een Gantry en een AMR. Deze twee moeten worden geprogrameerd voor de AMR is er gebruikt gemaakt van python. en voor de plc door middel van structered text. 

Het is de bedoeling dat het systeem de waspods van de lopendeband in een tray gelegd wordt. Hierna moet doormiddel van de AMR de trays naar de kwaliteitscontrole vervoerd worden. 
De python code is voor de werking van de AMR. Deze staat in directe communicatie met de PLC. Doormiddel van het internet kan de plc communiceren. In het document is er duidelijk te zien wat er gebeurt bij elke functie. 

Hardware:
- Omron LD-60;
- Beckhoff PLC CX5100;
- Laptop windows11.

Software:
- Python version 3.12.0 64-bit
- TwinCat XAE Shell version 3;

Imports FinalScript.py:
- Threading;
- Pyads version 3.3.9;
- Telnetlib version 3;
- time;

Imports "plc programma naam":


Architectuur: 
- De PLC heeft een connectie met het internet nodig voor de communicatie met de AMR. Hiervoor is er gebruikt gemaakt van een TP-Link wireless USB adapter (AC660). Verder is er in de PLC een task opgesteld dat wanneer de PLC wordt opgestart, dat dan het python script automatisch wordt aangeroepen zodat er een connectie tussen de AMR en PLC opgezet is;
- De PLC kent zijn eigen code die is geupload vanaf de laptop met het programma TwinCat XAE Shell.

Usage:
- Voor het gebruik van het systeem is het van belang dat eerst de AMR wordt gestart en wanneer deze volledig is opgestart dan pas de PLC aan te zetten. Dit zorgt ervoor dat er een juiste communicatie tussen de PLC en AMR bevind.

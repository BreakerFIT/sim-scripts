# sim-scripts
Sim-related scripts for use by ECorp/FSociety.

----
usage: pull-ec-fs.py [-h]

Pull ECorp and FSociety decks from the spreadsheets and merge into
customdecks.txt. After this, you will want to add personal custom decks to
customdecks_extras.txt instead.

optional arguments:
  -h, --help  show this help message and exit

----
usage: mission.py [-h] [-f] [-e BGE] MEMBER MISSION

Simulate a mission battle.

positional arguments:
  MEMBER      member to sim for
  MISSION     mission to sim

optional arguments:
  -h, --help  show this help message and exit
  -f          use unlimited SP (default: use no SP)
  -e BGE      Use BGE as battleground effect (default: none)

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
	usage: pvp-ecg.py [-h] [-f] [-e BGE] MEMBER

	Make optimized PVP surge decks (requires ECG gauntlets).

	positional arguments:
	  MEMBER      member to sim for

	optional arguments:  
	  -h, --help  show this help message and exit  
	  -f          use unlimited SP (default: use no SP)  
	  -e BGE      Use BGE as battleground effect (default: none)

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

----
	usage: guild-quest.py [-h] [-f] [-e BGE] MEMBER MISSION GUILD_FORTS ENEMY_FORTS

	Make optimized deck for a guild quest.

	positional arguments:
	  MEMBER       member to sim for
	  MISSION      mission to sim
	  GUILD_FORTS  the guild's current forts
	  ENEMY_FORTS  the enemy's current forts

	optional arguments:  
	  -h, --help   show this help message and exit  
	  -f           use unlimited SP (default: use no SP)  
	  -e BGE       Use BGE as battleground effect (default: none)

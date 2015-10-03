# Digital Display Script
Checks an e-mail inbox for messages containing a specific subject line, and opens specified program or file in fullscreen.  The purpose of this application and intended workflow is to use IFTTT and DO Button android apps, and the gmail channel on IFTTT, to easily send an e-mail with a specific subject line that triggers our Python script and opens a file or program in fullscreen.  The Do button is the only way to trigger events yourself using IFTTT, and there are limited channels to choose from.  The original use case was to help automate starting presentations or videos on a PC connected to a large or multi-screen display in an office.  

Yes, there are dedicated digital display and signage applications that do this better, but this was also largely a python learning project.   

License
------------

You can fork this repository on GitHub as long as it links back to this original repository. Do not sell this script.

Prerequisites
------------

  * Windows - Python 2.7

Installation
------------
Use virtualenv, please.

Clone or download this repository.

From the command line:

	pip install -r requirements.txt
	
Then run:

	python main.py

Configuration
------------
Rename 'config.example' to 'config'.

Open up `config` and make the values correspond to your POP compatible e-mail server, username, and password.  Gmail is recommended.

The message fields should contain the commands you wish to put in your e-mail subject line to trigger the respective on, off, and fullscreen actions.


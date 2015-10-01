# Digital Display Script
Checks an e-mail inbox for messages containing a specific subject line, and opens specified program or file in fullscreen.

[![Build Status](https://travis-ci.org/ModusVivendi/dur-displays.svg?branch=master)](https://travis-ci.org/ModusVivendi/twitter-contest)

License
------------

You can fork this repository on GitHub as long as it links back to this original repository. Do not sell this script as I would like the code to remain free.

Prerequisites
------------

  * Windows - Python 2.7
  * Linux - Python 2.7 or Python 3
  
Configuration
------------

Open up `config` and make the values correspond to your POP compatible e-mail server, username, and password.

Installation
------------
From the command line:

	"pip install requests && pip install ctypes && pip install configobj && pip install pywinauto && pip install apscheduler"
	
Then run:

	python main.py
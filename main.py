import os
import ctypes
import time
import requests
from configobj import ConfigObj
#from scapy.all import *
from subprocess import Popen, PIPE
import sys
import win32gui #http://sourceforge.net/projects/pywinauto/
from apscheduler.schedulers.blocking import BlockingScheduler

# apt-get install xautomation required for linux

# Use scapy to listen for specific mac address connections
#def arp_display(pkt):
#	if pkt.haslayer(ARP):
#		if pkt[ARP].op == 1: #who-has (request)
#			if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
#				if pkt[ARP].hwsrc == 'a0:1d:48:75:2b:8c': # Button 1
#					print('Pushed Button 1')
#					OpenFile('test.txt')
#				elif pkt[ARP].hwsrc == '10:ae:60:00:4d:f3': # Button 2
#					print('Pushed Button 2')
#					OpenFile(file2)
#				else:
#					print('ARP Probe from unknown device: ' + pkt[ARP].hwsrc)

import poplib
from email import parser

def CheckEmail():
	pop_conn = poplib.POP3_SSL(pop_server)
	pop_conn.user(pop_user)
	pop_conn.pass_(pop_password)
	#Get messages from server:
	messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
	# Concat message pieces:
	messages = [b"\n".join(mssg[1]) for mssg in messages]
	#Parse message intom an email object:
	messages = [parser.Parser().parsestr(mssg.decode('utf-8')) for mssg in messages]
	for message in messages:
		print(message['subject'])
		if message['subject'] == message_subject:
			OpenFile(open_file)
		elif message['subject'] == message_subject_off:
			CloseFile()
	pop_conn.quit()

# Opens program on windows and go fullscreen
def OpenFile(file):
	if sys.platform == 'linux2':
		subprocess.call(["xdg-open", file])
	else:
		os.startfile(file)
		time.sleep(5)
		toplist = []
		winlist = []
		def enum_callback(hwnd, results):
			winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
		win32gui.EnumWindows(enum_callback, toplist)
		app = [(hwnd, title) for hwnd, title in winlist if str(app_title_bar) in title.lower()]
		# just grab the first window that matches
		app = app[0]
		# use the window handle to set focus
		win32gui.SetForegroundWindow(app[0])

	#Key press to go fullscreen
	if sys.platform == 'linux2':
		keypress(AltEnterLinux)
	else:
		AltEnter()

# Actual Functions

def PressKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Windows key codes available at: http://msdn.microsoft.com/en-us/library/windows/desktop/dd375731%28v=vs.85%29.aspx

# Combo presses

def AltEnter():
    '''
    Press Alt+Enter and hold Alt key for 2 seconds
    '''

    PressKey(0x012) #Alt
    PressKey(0x0D) #Enter
    ReleaseKey(0x0D) #~Enter

    time.sleep(1)       
    ReleaseKey(0x012) #~Alt

# ====Begin building debian-based xautomation keypresses

def AltEnterLinux():
	'''keydown Alt_L
	key Enter
	keyup Alt_L
	'''

def keypress(sequence):
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence)

if __name__ =="__main__":
	#print(sniff(prn=arp_display, filter='arp', store=0, count=0))

	#Load config
	config = ConfigObj('config')
	pop_server = config['pop_server']
	pop_user = config['pop_user']
	pop_password = config['pop_password']

	message_subject = raw_input('What e-mail message subject will trigger this script?: ')
	open_file = raw_input('What is the path of the file you would like to open?: ')
	app_title_bar = raw_input('What is the name of the default program that opens your file?: ').lower()

	# ====Windows begin building ctypes functions====
	if not sys.platform == 'linux2':

		SendInput = ctypes.windll.user32.SendInput

		# C struct redefinitions 
		PUL = ctypes.POINTER(ctypes.c_ulong)
		class KeyBdInput(ctypes.Structure):
		    _fields_ = [("wVk", ctypes.c_ushort),
		                ("wScan", ctypes.c_ushort),
		                ("dwFlags", ctypes.c_ulong),
		                ("time", ctypes.c_ulong),
		                ("dwExtraInfo", PUL)]

		class HardwareInput(ctypes.Structure):
		    _fields_ = [("uMsg", ctypes.c_ulong),
		                ("wParamL", ctypes.c_short),
		                ("wParamH", ctypes.c_ushort)]

		class MouseInput(ctypes.Structure):
		    _fields_ = [("dx", ctypes.c_long),
		                ("dy", ctypes.c_long),
		                ("mouseData", ctypes.c_ulong),
		                ("dwFlags", ctypes.c_ulong),
		                ("time",ctypes.c_ulong),
		                ("dwExtraInfo", PUL)]

		class Input_I(ctypes.Union):
		    _fields_ = [("ki", KeyBdInput),
		                 ("mi", MouseInput),
		                 ("hi", HardwareInput)]

		class Input(ctypes.Structure):
		    _fields_ = [("type", ctypes.c_ulong),
		                ("ii", Input_I)]


	#Initialize scheduler
	scheduler = BlockingScheduler()

	scheduler.add_job(CheckEmail, 'interval', seconds=15)

	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		pass

import os
import ctypes
import time
import requests
from configobj import ConfigObj
#from scapy.all import *
from subprocess import Popen, PIPE
import sys
import win32gui #http://sourceforge.net/projects/pywinauto/ via easy_install
import win32con
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
import poplib
from email import parser

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
		if message['subject'] == message_subject_on:
			OpenFile(open_file)
		elif message['subject'] == message_subject_off:
			CloseFile(open_file)
			os.startfile('turnoff.exe')
		elif message['subject'] == message_subject_fullscreen:
			AltEnter()
	pop_conn.quit()


# Opens program on windows and go fullscreen

def OpenFile(file):
	toplist = []
	winlist = []
	def enum_callback(hwnd, results):
		winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
	win32gui.EnumWindows(enum_callback, toplist)
	app = [(hwnd, title) for hwnd, title in winlist if str(app_title_bar) in title.lower()]
	if len(app) == 0:
		os.startfile(os.path.normpath(file))
		time.sleep(5)
		win32gui.EnumWindows(enum_callback, toplist)
		app = [(hwnd, title) for hwnd, title in winlist if str(app_title_bar) in title.lower()]
		# just grab the first window that matches
		app = app[0]
		# use the window handle to set focus
		win32gui.SetForegroundWindow(app[0])

		#Key press to go fullscreen
		AltEnter()
	else:
		# just grab the first window that matches
		app = app[0]
		# use the window handle to set focus
		win32gui.SetForegroundWindow(app[0])
		AltEnter()



def CloseFile(file):
	toplist = []
	winlist = []
	def enum_callback(hwnd, results):
		winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
	win32gui.EnumWindows(enum_callback, toplist)
	app = [(hwnd, title) for hwnd, title in winlist if str(app_title_bar) in title.lower()]
	# just grab the first window that matches
	if len(app) > 0:
		app = app[0]
		# use the window handle to set focus
		win32gui.PostMessage(app[0], win32con.WM_CLOSE,0,0)

# Actual key press functions

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


if __name__ =="__main__":
	#print(sniff(prn=arp_display, filter='arp', store=0, count=0))

	#Load config
	config = ConfigObj('config')
	pop_server = config['pop_server']
	pop_user = config['pop_user']
	pop_password = config['pop_password']

	message_subject_on = config['message_subject_on']
	message_subject_off = config['message_subject_off']
	message_subject_fullscreen = config['message_subject_fullscreen']
	open_file = config['open_file']
	app_title_bar = config['app_title_bar'].lower() # Name of application that will be running your file

	# ====Windows begin building ctypes functions====

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
	logging.basicConfig()
	scheduler = BlockingScheduler()

	scheduler.add_job(CheckEmail, 'interval', seconds=15)

	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		pass

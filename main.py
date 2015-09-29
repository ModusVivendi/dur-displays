import os
import ctypes
import time
import requests
from scapy.all import *
from subprocess import Popen, PIPE

# apt-get install xautomation required for linux

# Use scapy to listen for specific mac address connections
def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      if pkt[ARP].hwsrc == 'a0:1d:48:75:2b:8c': # Button 1
        print('Pushed Button 1')
        OpenFile('test.txt')
      elif pkt[ARP].hwsrc == '10:ae:60:00:4d:f3': # Button 2
        print('Pushed Button 2')
        OpenFile(file2)
      else:
        print('ARP Probe from unknown device: ' + pkt[ARP].hwsrc)

# Opens program on windows and go fullscreen
def OpenFile(file):
	if sys.platform == 'linux2':
		subprocess.call(["xdg-open", file])
	else:
		os.startfile(file)

	#Key press to go fullscreen
	if sys.platform == 'linux2':
		keypress(AltEnterLinux)
	else:
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

    time.sleep(2)       
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
	print(sniff(prn=arp_display, filter='arp', store=0, count=0))



	
#Steven Pitts
import sys
from vGUI import VGUI
from setupGUI import SetupGUI
import Tkinter
from Tkinter import *

def main(argv=None):
	if argv is None: argv = sys.argv
	infoDict = dict()
	print "infoDict before: ",infoDict
	setup_gui = SetupGUI(Tk(),infoDict)
	print "infoDictAfter: ",infoDict
	my_gui = VGUI(Tk())
	return 0

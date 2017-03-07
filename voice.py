import sys
import Tkinter
from Tkinter import *
from makuUtil import Sound
from makuUtil import AudioRecorder
import sys
import socket
from setupGUI import UserSetupGUI
#from vGUI import VGUI
class VGUI:
	def __init__(self):
		
		
		infoDict = {}
		user_setup_gui = UserSetupGUI(Tk(),infoDict)
		self.sock = socket.socket()
		self.host = socket.gethostname()
		self.port = 12345
		self.firstName = infoDict["firstName"]
		self.lastName = infoDict["lastName"]
		self.sock.connect((self.host,self.port))
		
		infoDict["host"] = self.host
		infoDict["port"] = self.port
		infoDictString = str(infoDict)
		self.sock.send(infoDictString)
		
		self.master = Tk()
		self.audioRecorder = AudioRecorder(self)
		
		self.master.title("Intercom")
		
		Label(self.master, text = "Send your message to others on the network!\n\n").pack()
		self.record_button = Button(self.master, text="Record Message",command=self.recordPress)
		self.record_button.pack()
		mainloop()
		
	
	def recordPress(self):
		wasRecording = (self.record_button["text"] == "Stop Recording") #There must be a better way of doing this
		if wasRecording:
			data = self.audioRecorder.recordAudio()
			self.sendData(data)
			self.record_button["text"] = "Record Message"
		else:
			self.record_button["text"] = "Stop Recording"
	def sendData(self, data):
		newSound = Sound(data,self.getName())
		newSound.sendData(self)
	def getName (self):
		return self.firstName+" "+self.lastName
if __name__ == '__main__':
	vGUI = VGUI()
	mainloop()
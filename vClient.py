import sys
import Tkinter
from Tkinter import *
#from makuUtil import Sound
#from makuUtil import AudioRecorder
import sys
import socket
from config import *
import pyaudio
import wave
import config
import time
from config import *
from shutil import copyfile

class SetupGUI:
	def __init__(self, master, infoDict, inputDict, labelTextDict):
		self.master = master
		master.title("Setup")
		
		self.infoDict = infoDict
		
		defaultScreenSize = "500x500"
		master.geometry(defaultScreenSize)
		
		labelText = "Please fill out the information.\n\n"
		self.mainLabel = Label(master, text=labelText)
		self.mainLabel.pack()
		self.inputDict = inputDict
		self.labelTextDict = labelTextDict
		for key in self.inputDict:
			Label(master,text=self.labelTextDict[key]).pack()
			self.inputDict[key].pack()
		self.submitButton = Button(master,text="Submit",command=self.pressSubmit)
		self.submitButton.pack()
		
		self.populateButton = Button(master, text="Autopopulate (for debugging)",command=self.populate)
		self.populateButton.pack()
		
		mainloop()
		
	def pressSubmit(self):
		for key in self.inputDict:
			entryVal = self.inputDict[key].get()
			if (entryVal == ""):
				self.mainLabel["text"] = "One or more spaces are blank. Please fill out the form."
				return
			self.infoDict[key] = entryVal
		self.master.destroy()
	def populate(self):
		for key in self.inputDict:
			self.inputDict[key].insert(0,key+"Default")
class UserSetupGUI:
	def __init__(self, master, infoDict):
		self.master = master
		self.infoDict = infoDict
		
		self.inputDict = {"username": Entry(master),
			"firstName":Entry(master),
			"lastName":Entry(master)
			}
		self.labelTextDict = {"username":"Please enter your username here",
			"firstName":"Please enter your first name here",
			"lastName":"Please enter your last name here"
			}
		user_setup_gui = SetupGUI(self.master,self.infoDict,self.inputDict,self.labelTextDict)
		
		
class VGUI:
	def __init__(self):
		
		
		infoDict = {}
		user_setup_gui = UserSetupGUI(Tk(),infoDict)
		self.sock = socket.socket()
		hostname,aliaslist,ipaddress = socket.gethostbyaddr(makuServerIP) #Should be host IP
		self.host = hostname
		self.port = makuPort
		self.firstName = infoDict["firstName"]
		self.lastName = infoDict["lastName"]
		self.sock.connect((self.host,self.port))
		infoDict["host"] = self.host
		infoDict["port"] = self.port
		infoDictString = str(infoDict)
		self.sock.send(infoDictString)
		self.master = Tk()
		#self.audioRecorder = AudioRecorder(self)
		
		self.p = pyaudio.PyAudio()
		
		self.master.title("Intercom")
		Label(self.master, text = "Send your message to others on the network!\n\n").pack()
		self.record_button = Button(self.master, text="Record Message",command=self.recordPress)
		self.record_button.pack()
		mainloop()
		
	
	def recordPress(self):
		wasRecording = (self.record_button["text"] == "Stop Recording") #There must be a better way of doing this
		if wasRecording:
			#data = self.audioRecorder.recordAudio() #This gets the file
			data = self.recordAudio()
			self.sock.sendall(data.read())
			self.sendData(data)
			self.record_button["text"] = "Record Message"
		else:
			self.record_button["text"] = "Stop Recording"
	def sendData(self, data):
		print "1"
		self.sock.send(data.read())
		print "2"
		#newSound = Sound(data,self.getName())
		#newSound.sendData(self)
	def getName (self):
		return self.firstName+" "+self.lastName
	def recordAudio(self):
		#somehow record audio here
		stream = self.p.open(format=makuFormat,channels=makuChannels,rate=makuRate,input=True,frames_per_buffer=makuChunk)
		print "recording"
		frames = []
		for i in range(0,int((makuRate/makuChunk)*makuRecordSeconds)):
			soundData = stream.read(makuChunk)
			frames.append(soundData)
		print "done recording"
		stream.stop_stream()
		stream.close()
		wf=wave.open(makuOutputFilename,'wb')
		wf.setnchannels(makuChannels)
		wf.setsampwidth(self.p.get_sample_size(makuFormat))
		wf.setframerate(makuRate)
		wf.writeframes(b''.join(frames))
		wf.close()
		#time.sleep(2)
		openFile = open(makuOutputFilename,'rb')
		#time.sleep(2)
		return openFile
		
if __name__ == '__main__':
	vGUI = VGUI()
	mainloop()
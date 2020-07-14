#!/bin/python
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

import tkinter as tk
from tkinter.font import Font
from wordBook import *


buttonWordSize = 50
buttonWidth = 15
buttonHeight = 3

wordSize = 60
wordDisplayWidth = 30
wordDisplayHeight = 6
fontFam = "Cambria"
appColor='#f7eac2'

root = tk.Tk()
root.configure(bg=appColor)
displayFrame = tk.Frame(root, bg=appColor)
wordDisplay = tk.Label(displayFrame, width=wordDisplayWidth, height=wordDisplayHeight, bg=appColor)


TestMode = False
TestEnded = False

readWords("wordList.txt")
record = evaluater(len(wordList))

gen = wordGenerator(wordList)
if wordGenerator.savingExists():
	gen.readProgress()
	TestEnded = gen.testFinished()
	wordDisplay["text"] = gen.getCurrentWord() if not TestEnded else "Finished. Keep going or not? "
else:
	gen.setTestAmount(5)
	wordDisplay["text"] = gen.getRandomWord()


def handleResponse(response):

	global TestEnded, TestMode
	if not TestEnded:
		if response:	# Get corrected
			if TestMode:
				record.markCorrect()
			gen.passWord()
		else:			# Get wrong
			if TestMode:
				record.markWrong()
				gen.passWord()
				print("Word No." + str(gen.getCurrentWordID()))
			else:
				gen.recordWrong()
	else:
		if response:
			gen.reset()
			record.reset()
			TestEnded = False
			#word = gen.getRandomWord()
		else:
			gen.saveProgress()
			root.destroy()
			return

	wordCountDisplay["text"] = "%d / %d"%(gen.getTestCount(), gen.getTestAmount())


	if gen.testFinished():
		# Display whether to continue
		wordDisplay['text'] = "Finished. Keep going or not? "
		TestEnded = True
		return

	word = gen.getRandomWord()
	wordDisplay['text'] = word


def on_closing():
	gen.saveProgress()
	root.destroy()


if __name__ == "__main__":

	#cornerFrame = tk.Frame(root, bg=appColor)
	wordCountDisplay = tk.Label(root, font=Font(size=20), width=10, height=2, bg=appColor)
	wordCountDisplay["text"] = "%d / %d"%(gen.getTestCount(), gen.getTestAmount())
	wordCountDisplay.pack(anchor="ne", padx=10)
	#cornerFrame.pack(anchor="ne")

	wordFont = Font(family=fontFam, size=wordSize)
	wordDisplay.configure(font=wordFont)
	wordDisplay.pack(side="left")
	
	displayFrame.pack(pady=20)

	bottonFrame = tk.Frame(root, bg=appColor)

	yesButton = tk.Button(bottonFrame, text='Yes', width=buttonWidth, height=buttonHeight, fg='green', command=lambda: handleResponse(True))
	yesButton.pack(side = "left", padx=50) 
	noButton = tk.Button(bottonFrame, text='No', width=buttonWidth, height=buttonHeight, fg='red', command=lambda: handleResponse(False))
	noButton.pack(side = "left", padx=50)
	buttonFont = Font(family=fontFam, size=buttonWordSize)
	yesButton.configure(font=buttonFont)
	noButton.configure(font=buttonFont)
	bottonFrame.pack(anchor="center", pady=30)	

	root.protocol("WM_DELETE_WINDOW", on_closing)

	root.mainloop() 
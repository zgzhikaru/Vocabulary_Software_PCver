import tkinter as tk
from tkinter.font import Font

import wordBook

buttonWordSize = 50
buttonWidth = 15
buttonHeight = 3

wordSize = 60
wordDisplayWidth = 30
wordDisplayHeight = 6
fontFam = "Cambria"

appColor='#f7eac2'

if __name__ == "__main__":

	root = tk.Tk()
	root.configure(bg=appColor)

	displayFrame = tk.Frame(root, bg=appColor)
	wordDisplay = tk.Label(displayFrame, text='Word', width=wordDisplayWidth, height=wordDisplayHeight, bg=appColor)
	wordFont = Font(family=fontFam, size=wordSize)
	wordDisplay.configure(font=wordFont)
	wordDisplay.pack(side="top")
	displayFrame.pack(pady=20)

	bottonFrame = tk.Frame(root, bg=appColor)

	yesButton = tk.Button(bottonFrame, text='Yes', width=buttonWidth, height=buttonHeight, fg='green')
	yesButton.pack(side = "left", padx=50) 
	noButton = tk.Button(bottonFrame, text='No', width=buttonWidth, height=buttonHeight, fg='red')
	noButton.pack(side = "left", padx=50)
	buttonFont = Font(family=fontFam, size=buttonWordSize)
	yesButton.configure(font=buttonFont)
	noButton.configure(font=buttonFont)
	bottonFrame.pack(anchor="center", pady=30)	

	readWords("wordBook.txt")

	root.mainloop() 
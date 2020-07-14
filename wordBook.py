#!/bin/python

import sys, os
import random
from collections import defaultdict 
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

wordList = []
wordStat = defaultdict(lambda: 0) 
wordIDs = defaultdict(lambda: []) 
repeatRate = []

def readWords(filename):
	try:
		file = open(filename)
	except:
		print("File " + filename + " can't be opened")
		exit(-1)

	id = 0
	for word in file:
		word = word.rstrip("\n")
		if not all(ch.isalpha() or ch.isspace() or "-" or "'" in ch for ch in word):
			print("File contains non-valid word: " + word)
			exit(-1)

		wordList.append(word)
		wordStat[word] += 1
		id+=1
		wordIDs[word].append(id)
		repeatRate.append((1-len(wordStat)/id)*100)

	file.close()

	if not wordList:
		print("Word file is empty")
		exit(-1)

	print("Unique words: %d" % len(wordStat))
	print("Repeat rate: %.2f%%" % ((1-len(wordStat)/id)*100))

	return wordList


def showStat(words, freqs):
	#words = list(wordStat.keys())
	#freqs = list(wordStat.values())
	maxfreq = max(freqs)

	fig, ax = plt.subplots()
	ax.bar(words, freqs)

	plt.xticks(words, rotation='vertical')
	fig.tight_layout()
	#fig.subplots_adjust(bottom=0.25)
	plt.ylim(0, maxfreq + 1)
	ax.yaxis.set_major_locator(MaxNLocator(integer=True))

	plt.show()

def repeatRateChange():
	#words = list(wordStat.keys())
	#freqs = list(wordStat.values())
	#maxfreq = max(freqs)

	#fig, ax = plt.subplots()
	#ax.bar(words, freqs)

	#plt.xticks(words, rotation='vertical')
	#fig.tight_layout()
	#fig.subplots_adjust(bottom=0.25)
	#plt.ylim(0, 100)
	#ax.yaxis.set_major_locator(MaxNLocator(integer=True))
	plt.plot(repeatRate)

	plt.show()


def editDistance(str1, str2):
	m = len(str1)
	n = len(str2)

	dist = [[j for j in range(n + 1)] if not i else [i] for i in range(m + 1)]
	"""
	dist = [[j for j in range(n + 1)] if not i else 
			[i if not j 
				else (str1[i-1] != str2[j-1]) + min(dist[i-1][j-1], dist[i-1][j], dist[i][j-1]) 
				for j in range(n + 1)] 
			for i in range(m + 1)]
	"""
	for i in range(1, m+1):
		for j in range(1, n+1):
			distIJ = (str1[i-1] != str2[j-1]) + min(dist[i-1][j-1], dist[i-1][j], dist[i][j-1])
			dist[i].append(distIJ)

	return dist[m][n]


def findSimilarWords(word):
	maxED = 4
	wordsByED = defaultdict(lambda: [])
	#i = 0
	for entryWord in wordStat:
		ED = editDistance(word, entryWord)
		wordsByED[ED].append(entryWord)
		"""
		if i > 10:
			print(wordsByED)
			return wordsByED
		i+=1
		"""
	similarWords = [[] for ED in range(maxED)]
	for ED in wordsByED:
		if ED < maxED:
			similarWords[ED] = wordsByED[ED]
	#print(similarWords)
	return [word for words in similarWords for word in words]



class wordGenerator:
	def digitData(self, dataType, dataContent):
		#print("In digitData")
		#print(dataType)
		try:
			dataContent = int(dataContent)
			#print(dataContent + 1)
			if dataContent:
				exec("self.%s = %d" % (dataType, dataContent))
			else:
				print("Error: Cannot Read Savings(Null digit data)")
				exit(-1)
		except:
			print("Error: Cannot Read Savings(Digit data error)")
			exit(-1)

	def strListData(self, dataType, dataContent):
		#print("In strListData")
		#print(dataType)
		try:
			exec("self.%s = []" % (dataType))
			if dataContent:
				dataContent = dataContent.split(", ")
				for strdata in dataContent:
					try:
						exec("self.%s.append(%s)" % (dataType, strdata))
					except:
						print("Error: Cannot Read Savings(String data error)")
						#print("%s.append(%s)" % (dataType, strdata))
						exit(-1)
			# Else the string list is supposed to be empty
		except:
			print("Error: Cannot Read Savings(String data error)")
			exit(-1)

	#global digitData, strListData
	#global handleSavedData
	

	def __init__(self, wordList):
		if not wordList:
			print("To Administrator: Word List must be non-empty")
			exit(-1)
		self.wordList = wordList
		self.wordAmount = len(self.wordList)	# Total number of all available words
		self.indexSet = set(range(len(self.wordList)))	# Representation of each word as index
		self.currIndex = -1
		self.testHistory = []
		self.wrongWords = set()	
		self.testCount = 0
		self.testAmount = self.wordAmount

		self.handleSavedData = {"wordAmount": self.digitData, "currIndex": self.digitData, 
			"testHistory": self.strListData, "wrongWords": self.strListData, 
			"testAmount": self.digitData}
		

	def getTestCount(self):
		return self.testCount

	def getTestAmount(self):
		return self.testAmount

	def setTestAmount(self, testAmount):
		if testAmount > self.testCount:
			self.testAmount = testAmount
			return True
		else:
			return False

	def testFinished(self):
		return not (self.testCount < self.testAmount)

	def getCurrentWord(self):
		return self.wordList[self.currIndex]

	def getRandomWord(self):
		if self.testFinished():
			return ""

		remainAmt = self.testAmount - self.testCount
		wrongAmt = len(self.wrongWords)
		if not remainAmt >= wrongAmt:
			print("remainAmt: " + str(remainAmt))
			print("wrongAmt: " + str(wrongAmt))
		assert(remainAmt > 0)
		assert(remainAmt >= wrongAmt)


		choiceIndex = random.randint(0, remainAmt-1)
		#print("choiceIndex: " + str(choiceIndex))
		if choiceIndex < wrongAmt:
			index = random.choice(tuple(self.wrongWords))
		else:
			index = random.choice(tuple(self.indexSet))

		self.currIndex = index
		return self.wordList[index]

	def passWord(self):
		self.indexSet.remove(self.currIndex)
		self.testHistory.append(self.currIndex)
		if self.currIndex in self.wrongWords:
			self.wrongWords.remove(self.currIndex)
		self.testCount += 1

	def recordWrong(self):
		self.wrongWords.add(self.currIndex)

	def getCurrentWordID(self):
		return self.currIndex + 1

	def saveProgress(self):
		try:
			savingFile = open("saving.txt", mode="w")
		except:
			print("Error: Cannot Save")
			exit(-1)

		savingFile.write("wordAmount:%d\n" % self.wordAmount)
		savingFile.write("currIndex:%d\n" % self.currIndex)

		savingFile.write("testHistory:")
		if self.testHistory:
			savingFile.write(str(self.testHistory[0]))
			for index in self.testHistory[1:]:
				savingFile.write(", %d" % index)
		savingFile.write("\n")

		savingFile.write("wrongWords:")
		if self.wrongWords:
			wrongWordList = list(self.wrongWords)
			savingFile.write(str(wrongWordList[0]))
			for index in wrongWordList[1:]:
				savingFile.write(", %d" % index)
		savingFile.write("\n")

		savingFile.write("testAmount:%d\n" % self.testAmount)
		"""
		self.wordList = wordList
		self.wordAmount = len(self.wordList)	# Total number of available words
		self.indexSet = set(range(len(self.wordList)))	# Representation of each word as index
		self.currIndex = -1
		self.testHistory = []
		self.wrongWords = set()
		self.testCount = 0
		self.testAmount = self.wordAmount
		"""

	def readProgress(self):
		try:
			savingFile = open("saving.txt")
		except:
			print("Error: Cannot Read Savings(Saving file missing or damaged)")
			exit(-1)

		for line in savingFile:
			line = line.rstrip("\n")

			content = line.split(":")
			if len(content) > 2:
				print("Error: Cannot Read Savings(Saving format disrupted)")
				exit(-1)
			else:
				dataType = content[0]
				dataContent = content[1] if len(content) == 2 else None

				#global handleSavedData
				self.handleSavedData[dataType](dataType, dataContent)

		if len(wordList) != self.wordAmount:
			print("Error: Cannot Read Savings(Word source different)")
			exit(-1)
		self.wrongWords = set(self.wrongWords)
		self.indexSet = self.indexSet - set(self.testHistory)
		self.testCount = len(self.testHistory)

		print("wordAmount: %d"%self.wordAmount)
		print("currIndex: %d"%self.currIndex)
		print("testHistory: ", end="")
		print(self.testHistory)
		print("wrongWords: ", end="")
		print(self.wrongWords)
		print("testAmount: %d"%self.testAmount)


	def savingExists():
		return os.path.exists("saving.txt")

	def reset(self):
		self.indexSet = set(range(len(self.wordList)))
		self.currIndex = -1
		self.testHistory = []
		self.wrongWords.clear()
		self.testCount = 0


class evaluater:
	def __init__(self, wordNum):
		self.total = wordNum
		self.wrong = 0
		self.correct = 0

	def markWrong(self):
		self.wrong += 1

	def markCorrect(self):
		self.correct += 1

	def report(self):
		testedNum = self.correct + self.wrong
		percentage = self.correct / testedNum * 100
		print("Corrected: %d out of %d (%.2f%%)" % (self.correct, testedNum, percentage))

	def reset(self):
		self.wrong = 0
		self.correct = 0


if __name__ == "__main__":

	TestMode = False
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		print("In Practice Mode\n")
	elif len(sys.argv) == 3:
		filename = sys.argv[1]
		if sys.argv[2] == '-t':
			TestMode = True
			print("In Test Mode\n")
		else:
			print("In Practice Mode\n")
	else:
		print("Usage: python wordBook.py filename.txt -t/-p")
		exit(-1)

	readWords(sys.argv[1])

	#showStat()
	gen = wordGenerator(wordList)
	gen.setTestAmount(5)
	word = gen.getRandomWord()

	record = evaluater(len(wordList))
	keepGoing = True
	while keepGoing:
		# Generates random word one at a time
		while not gen.testFinished():
			print("[%d] "% (gen.getTestCount()+1), end="")
			print(word)
			respond = input("[y or n]: ")
			if respond == 'n':	# Get wrong
				if TestMode:
					record.markWrong()
					gen.passWord()
				print("Word No." + str(gen.getCurrentWordID()))
			else:	# Get corrected
				if TestMode:
					record.markCorrect()
				gen.passWord()

			print()
			word = gen.getRandomWord()

		if TestMode:
			record.report()

		# Ask user whether to retry or end the session
		ContinueCommand = ''
		while not ContinueCommand in ['y','n']:
			ContinueCommand = input("Finished. Keep going or not: [y or n]")
			if ContinueCommand == 'n':
				keepGoing = False
			elif ContinueCommand == 'y':
				gen.reset()
				record.reset()
				word = gen.getRandomWord()


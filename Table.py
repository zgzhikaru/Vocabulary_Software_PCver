#!/bin/python
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

from tkinter import *
from tkinter import ttk 
from wordBook import *
from collections import defaultdict 

noResultDisplay = None

class Table: 
      
   def __init__(self,root): 
          
        # code for creating table 
        for i in range(total_rows): 
            for j in range(total_columns): 
                  
                self.e = Label(root, text=lst[i][j], width=20, 
                               font=('Arial',16)) 
                  
                self.e.grid(row=i, column=j) 
                #self.e.insert(END, lst[i][j]) 

def handleSearch():
	global noResultDisplay
	if noResultDisplay:
		noResultDisplay.pack_forget()
		noResultDisplay = None

	word = E1.get()

	"""
	wordsByED = defaultdict(lambda: [])
	for entry in treev.get_children():
		#treev.delete(entry)
		entryWord = treev.item(entry, "values")[1]
		ED = editDistance(word, entryWord)
		wordsByED[ED].append(entryWord)
		if i > 10:
			print(wordsByED)
			return
		i+=1
	"""
	if not word:	return
	 
	for entry in treev.get_children():
		treev.delete(entry)

	if word in wordStat:
		treev.insert("", 'end', text ="L1", values = (wordIDs[word], word, wordStat[word]))
	else:
		noResultDisplay = Label(headFrame, text="  No result found. Do you mean: ",  
                               font=('Arial',16)) 
		noResultDisplay.pack()

		similarWords = findSimilarWords(word)
		for word in similarWords:
			treev.insert("", 'end', text ="L1", values = (wordIDs[word], word, wordStat[word]))
		#print(similarWords)

def handleClear():
	global noResultDisplay
	if noResultDisplay:
		noResultDisplay.pack_forget()
		noResultDisplay = None

	for entry in treev.get_children():
		treev.delete(entry)
	for entry in lst: 
		treev.insert("", 'end', text ="L1", values = entry) 
	#treev.set_children(treev.get_children(), allEntries)


if __name__ == "__main__":
	# take the data 
	readWords("wordList.txt")

	lst = []
	#i = 0
	for word, freq in wordStat.items():
		#i += 1
		id_str = ""#str(wordIDs[word][0])
		for id in wordIDs[word]:
			id_str += str(id) + ", "
		id_str = id_str[:-2]
		lst.append((id_str, word, freq))

	lst.sort(key=lambda e: e[2], reverse=True)

	words = []
	freqs = []
	for id_str, word, freq in lst:
		words.append(word)
		freqs.append(freq)

	#showStat(words, freqs)
	#repeatRateChange()
		
	# find total number of rows and 
	# columns in list 
	total_rows = len(lst)
	total_columns = len(lst[0]) 
	   
	root = Tk()

	headFrame = Frame(root)
	searchBarFrame = Frame(headFrame)
	#L1 = Label(searchBarFrame, text="Search")
	#L1.pack(side ='left')
	E1 = Entry(searchBarFrame, bd =5)
	E1.pack(side ='left')
	B1 = Button(searchBarFrame, text='Search', width=8, height=1, command=handleSearch)
	B1.configure(font=('Arial',20))
	B1.pack(side ='left')
	B2 = Button(searchBarFrame, text='Clear', width=8, height=1, command=handleClear)
	B2.configure(font=('Arial',20))
	B2.pack(side ='left')
	searchBarFrame.pack()
	headFrame.pack()

	treev = ttk.Treeview(root, height=40)
	treev.pack(side ='left')

	verscrlbar = ttk.Scrollbar(root, orient ="vertical", command = treev.yview) 
	verscrlbar.pack(side ='right', fill ='x') 
	treev.configure(xscrollcommand = verscrlbar.set) 

	treev["columns"] = ("1", "2", "3") 
	treev['show'] = 'headings'

	treev.column("1", width = 200, anchor ='c') 
	treev.column("2", width = 200, anchor ='se') 
	treev.column("3", width = 200, anchor ='se')

	treev.heading("1", text ="ID") 
	treev.heading("2", text ="Word") 
	treev.heading("3", text ="Frequency")

	for i in range(total_rows): 
		#print(lst[i])
		treev.insert("", 'end', text ="L1", values = lst[i]) 

	#allEntries = treev.get_children()

	"""
	scroll_bar = Scrollbar(root) 
	scroll_bar.pack( side = RIGHT, fill = Y ) 
	mylist = Listbox(root, yscrollcommand = scroll_bar.set) 
	   
	#for line in range(1, 26): 
	 #   mylist.insert(END, "Geeks " + str(line)) 
	for i in range(total_rows): 
        for j in range(total_columns):           
        	self.e = Label(root, text=lst[i][j], width=20, 
                               font=('Arial',16)) 
                  
            #self.e.grid(row=i, column=j) 
            mylist.insert(END, lst[i][j]) 
	  
	mylist.pack( side = LEFT, fill = BOTH ) 
	  
	scroll_bar.config( command = mylist.yview ) 
	""" 
	root.mainloop() 

	# create root window 
	#root = Tk() 
	#t = Table(root) 
	#root.mainloop() 

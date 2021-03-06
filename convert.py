from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename
import csv
import os

#***********************************************************************************************************************
# Funktionen
#***********************************************************************************************************************

def manuellFile(*event):
    """
    The user must say which files he wants to convert. Calls the function manuellFileWriter as long as the return is true.
    :param event: (Is only there so that the short cut works.)
    :return: nothing
    """
    filename = str(askopenfilename()) #get the filename
    if os.path.exists(filename):
        writer = outputFile(filename) #make the outputfile and get the object writer to can write the file
        manuellerInput = manuellFileWriter(filename,writer) #writes the file into the outputfile and returns true or false
        while manuellerInput:
            filename = str(askopenfilename()) #get the filename
            if os.path.exists(filename):
                manuellerInput = manuellFileWriter(filename,writer)

def manuellFileWriter(filename,writer):
    """
    Writes the file and ask if another should be done. Return then true or false, so the while loop in manuellFile keeps looping.
    :param filename: filename of the file which should be converted.
    :param writer: the prepared output file
    :return: True or False, depend on which answer the user gives
    """
    #writes the inputfile into the outputfile
    writeFile(filename, writer)
    #asks if the user wants to convert another file
    if tkMessageBox.askyesno("Question", "Convert another File?"):
        return True
    else:
        return False

def statusBar(message):
    """
    Writes the filename in the statusbar. The latest filename appears always at the top of the list.
    :param message: the filename of the file which have been converted.
    :return: nothing
    """
    global TextField
    TextField.insert('1.0', message)
    convertWindow.update()

def outputFile(filename):
    """
    First creates a new filename out of the file, which have been chosen. Opens then the output file and writes the headline.
    :param filename: the chosen filename
    :return: the output file
    """
    #Outputfilename
    newInputFilenameList = filename.split('_')
    del newInputFilenameList[-1]
    OutputFilename = "_".join(newInputFilenameList)
    OutputFilename = OutputFilename +"_all.csv"
    #Open output file
    outputFile = open(OutputFilename, "wb")
    writer = csv.writer(outputFile, delimiter=',')
    #write headline
    headline = ["Time","RelativeTimeMilliseconds","Clock","Pulse","inSEV","inO2"]
    writer.writerow(headline)
    return writer

def autoFile(*event):
    """
    Reads every file in directory. The first file must be choose, then the function replaces the number and reads so the next file until all have been converted.
    :param event: (Is only there so that the short cut works.)
    :return: nothing
    """
    filename = str(askopenfilename())
    if os.path.exists(filename):
        #Opens the outputfile
        writer = outputFile(filename)
        #check if the first file exists
        fileExsits = True
        #fileindex
        index = 1
        while fileExsits:
            #open the file
            writeFile(filename, writer)
            #create new filename
            newFilenameList = filename.split('_')
            del newFilenameList[-1]
            newFilename = "_".join(newFilenameList)
            index += 1
            #if the index is smaller than 10 there is a zero before the number.
            if index < 10:
                endung = "0"+str(index)+".csv"
            else:
                endung = str(index)+".csv"

            #add the ending to the filename
            filename = newFilename+"_"+endung
            fileExsits = os.path.exists(filename)

def writeFile(inputFilename, writer):
    """
    Reads every line in the chosen file and writes every 50th line into the output file. Only the wanted rows are writen into the output file.
    If other rows should also be written in the output file the row must be specified in the if condition and the headlines also must be adopt.
    :param inputFilename: the chosen filename
    :param writer: output file
    :return: nothing
    """
    #go throw every row
    with open(inputFilename) as csvfile:
        file = csv.reader(csvfile)
        for i, row in enumerate(file):
            parameter = []
            if i % 50 == 1: #beginning with the second entry every 5th entry is written
                parameter.append(row[0])  #time
                parameter.append(row[1])  #Relative time in mS
                parameter.append(row[2])  #Clock
                parameter.append(row[5])  #Pulse
#               parameter.append(row[19]) #etDES
#               parameter.append(row[20]) #inDES
#               parameter.append(row[21]) #etISO
#               parameter.append(row[22]) #inISO
#               parameter.append(row[23]) #etSEV
                parameter.append(row[24]) #inSEV
#               parameter.append(row[25]) #etN2O
                parameter.append(row[29]) #inO2
                writer.writerow(parameter)
    messege = inputFilename+" done\n"
    statusBar(messege)

#***********************************************************************************************************************
# Programm Start
#***********************************************************************************************************************
convertWindow = Tk()
convertWindow.title('Vital Signs Data Explorer Converter')

#keyboard events
convertWindow.bind("<Control-a>",autoFile)
convertWindow.bind("<Control-m>",manuellFile)
convertWindow.update()

#Label
Label(convertWindow,text="Einzeln(manuell) oder alle(automatisch) convertieren?").pack()

#the two buttons at the top
topframe = Frame(convertWindow)
topframe.pack(side=TOP)
Button(topframe, text="Manuell", command=manuellFile).pack(side=LEFT, pady=5, padx=50)
Button(topframe, text="Automatisch", command=autoFile).pack(side=LEFT, pady=5, padx=50)

#Statusbar at the bottom
bottomframe = Frame(convertWindow)
bottomframe.pack(side=BOTTOM, fill=BOTH, expand=1)
ScrollBar = Scrollbar(bottomframe)
TextField = Text(bottomframe, bg="#EEEEEE")
ScrollBar.pack(side=RIGHT, fill=Y)
TextField.pack(side=LEFT, fill=BOTH, expand=1)
ScrollBar.config(command=TextField.yview)
TextField.config(yscrollcommand=ScrollBar.set)

convertWindow.mainloop()
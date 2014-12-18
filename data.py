from tkFileDialog import askopenfilename
import csv
import os

class Data():
    def __init__(self):
        """
        Defines the value headline
        :return: nothing
        """
        self.headline = ""

    def getFilename(self):
        """
        Gets the file and if the file exists returns true.
        :return: True or False
        """
        self.temp = str(askopenfilename())
        if os.path.exists(self.temp):
            self.filename = self.temp
            return True
        else:
            return False

    def readHeadline(self):
        """
        Reads the headline from the csv file
        :return: titles from the headline
        """
        with open(self.filename) as file:
            self.headline = file.readline()
        self.headline = self.headline.split(',')
        self.headline[-1] = self.headline[-1].strip()
        return self.headline

    def readValues(self, rowNumber):
        """
        Reads the row.
        :param rowNumber:
        :return: row
        """
        self.valuesTemp = []
        with open(self.filename) as self.file:
            self.csvfile = csv.reader(self.file)
            next(self.csvfile)
            for row in self.csvfile:
                self.valuesTemp.append(row[rowNumber])
        return self.valuesTemp

    def readAllValues(self):
        """
        Reads every row from the file
        :return: 2-dimensional list with every value
        """
        self.valueAll = []
        for rowNumber in range(len(self.headline)):
            self.values = self.readValues(rowNumber)
            self.valueAll.append(self.values)
        return self.valueAll

    def getInfo(self):
        """
        Get starttime, endtime and calculates length.
        :return: starttime, endtime, length
        """
        self.durationRow = 1
        self.clockRow = 2

        self.durations = self.readAllValues()
        self.durationStart = int(self.durations[self.durationRow][0])
        self.durationEnd = int(self.durations[self.durationRow][-1])

        self.durationH = int((self.durationEnd - self.durationStart)/3600000)
        self.durationMin = int((self.durationEnd - self.durationStart - (self.durationH *3600000))/60000)
        self.durationSec = int((self.durationEnd - self.durationStart - (self.durationH *3600000) - (self.durationMin * 60000))/1000)

        self.duration = str(self.durationH) + "h " + str(self.durationMin) + "Min " + str(self.durationSec) + "Sec"

        self.clocks = self.readAllValues()
        self.clockStart = self.clocks[self.clockRow][0]
        self.clockEnd = self.clocks[self.clockRow][-1]

        self.infos = [self.duration, self.clockStart, self.clockEnd]
        return self.infos


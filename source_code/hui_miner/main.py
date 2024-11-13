import time
import csv
import psutil
from collections import defaultdict
import bisect

class Element:
    def __init__(self, tid, iutils, rutils):
        self.tid = tid
        self.iutils = iutils
        self.rutils = rutils

class UtilityList:
    def __init__(self, item):
        self.item = item
        self.sumIutils = 0
        self.sumRutils = 0
        self.elements = []

    def addElement(self, element):
        self.sumIutils += element.iutils
        self.sumRutils += element.rutils
        self.elements.append(element)

class HUIMiner:
    def __init__(self):
        self.startTimestamp = 0
        self.endTimestamp = 0
        self.huiCount = 0
        self.mapItemToTWU = {}
        self.joinCount = 0
        self.BUFFERS_SIZE = 200
        self.itemsetBuffer = [0] * self.BUFFERS_SIZE

    def runAlgorithm(self, inputPath, outputPath, minUtility):
        self.startTimestamp = time.time()
        self.startMemory = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory in MB
        self.itemsetBuffer = [0] * self.BUFFERS_SIZE

        with open(outputPath, 'w') as writer:
            self.writer = writer

            self.mapItemToTWU = defaultdict(int)

            transactions = self.readTransactions(inputPath)
            self.calculateTWU(transactions, minUtility)
            listOfUtilityLists, mapItemToUtilityList = self.createUtilityLists(minUtility)
            self.buildUtilityLists(transactions, mapItemToUtilityList, minUtility)
            self.huiMiner([], 0, None, listOfUtilityLists, minUtility)

            self.endTimestamp = time.time()
            self.endMemory = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory in MB

    def readTransactions(self, inputPath):
        transactions = []
        with open(inputPath, 'r') as file:
            reader = csv.reader(file, delimiter=':')
            for row in reader:
                items = list(map(int, row[0].split()))
                transactionUtility = int(row[1])
                utilities = list(map(int, row[2].split()))
                transactions.append((items, transactionUtility, utilities))
        return transactions

    def calculateTWU(self, transactions, minUtility):
        for items, transactionUtility, _ in transactions:
            for item in items:
                self.mapItemToTWU[item] += transactionUtility

    def createUtilityLists(self, minUtility):
        listOfUtilityLists = []
        mapItemToUtilityList = {}

        for item, twu in self.mapItemToTWU.items():
            if twu >= minUtility:
                uList = UtilityList(item)
                mapItemToUtilityList[item] = uList
                listOfUtilityLists.append(uList)

        listOfUtilityLists.sort(key=lambda x: self.mapItemToTWU[x.item])
        return listOfUtilityLists, mapItemToUtilityList

    def buildUtilityLists(self, transactions, mapItemToUtilityList, minUtility):
        for tid, (items, transactionUtility, utilities) in enumerate(transactions):
            revisedTransaction = []
            remainingUtility = 0

            for item, utility in zip(items, utilities):
                if self.mapItemToTWU[item] >= minUtility:
                    revisedTransaction.append((item, utility))
                    remainingUtility += utility

            revisedTransaction.sort(key=lambda x: self.mapItemToTWU[x[0]])

            for item, utility in revisedTransaction:
                remainingUtility -= utility
                element = Element(tid, utility, remainingUtility)
                mapItemToUtilityList[item].addElement(element)

    def huiMiner(self, prefix, prefixLength, pUL, ULs, minUtility):
        for i in range(len(ULs)):
            X = ULs[i]

            if X.sumIutils >= minUtility:
                self.writeOut(prefix, prefixLength, X.item, X.sumIutils)

            if X.sumIutils + X.sumRutils >= minUtility:
                exULs = []
                for j in range(i + 1, len(ULs)):
                    Y = ULs[j]
                    exULs.append(self.construct(pUL, X, Y))
                    self.joinCount += 1

                self.itemsetBuffer[prefixLength] = X.item
                self.huiMiner(self.itemsetBuffer, prefixLength + 1, X, exULs, minUtility)

    def construct(self, P, px, py):
        pxyUL = UtilityList(py.item)

        for ex in px.elements:
            ey = self.findElementWithTID(py, ex.tid)
            if ey is None:
                continue
            if P is None:
                eXY = Element(ex.tid, ex.iutils + ey.iutils, ey.rutils)
                pxyUL.addElement(eXY)
            else:
                e = self.findElementWithTID(P, ex.tid)
                if e is not None:
                    eXY = Element(ex.tid, ex.iutils + ey.iutils - e.iutils, ey.rutils)
                    pxyUL.addElement(eXY)
        return pxyUL

    def findElementWithTID(self, ulist, tid):
        elements = [e.tid for e in ulist.elements]
        index = bisect.bisect_left(elements, tid)
        if index < len(ulist.elements) and ulist.elements[index].tid == tid:
            return ulist.elements[index]
        return None

    def writeOut(self, prefix, prefixLength, item, utility):
        self.huiCount += 1
        output = ' '.join(map(str, prefix[:prefixLength])) + ' ' + str(item) + ' #UTIL: ' + str(utility)
        self.writer.write(output + '\n')
        
    def printStats(self):
        elapsed_time = self.endTimestamp - self.startTimestamp
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = elapsed_time % 60

        print("=============  HUI-MINER ALGORITHM - STATS =============")
        print(f" Total time ~ {hours} giờ {minutes} phút {seconds:.2f} giây")
        print(" Memory ~", self.endMemory - self.startMemory, "MB")
        print(" High-utility itemsets count :", self.huiCount)
        print(" Join count :", self.joinCount)
        print("===================================================")

if __name__ == "__main__":
    minUtility = 40
    inputPath = "db_utility.txt"
    outputPath = "outputMiner.txt"
    hui_miner = HUIMiner()
    hui_miner.runAlgorithm(inputPath, outputPath, minUtility)
    hui_miner.printStats()

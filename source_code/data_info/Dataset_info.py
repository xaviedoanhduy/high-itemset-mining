from Transaction import Transaction
class Dataset:
    def __init__(self, datasetPath):
        self.transactions = []
        self.totalUtility = 0
        self.maxItem = 0
        with open(datasetPath) as f:
            for line in f:
                if line=="" or line[0] == '#' or line[0] == '%' or line[0] == '@':
                    continue
                t = self.createTransaction(line)
                self.totalUtility += t.getUtility()
                self.transactions.append(t)

    def createTransaction(self, line):
        split = line.split(":")
        transactionUtility = int(split[1])
        itemsString = split[0].split(' ')
        itemsUtilitiesString = split[2].split(' ')
        items = []
        utilities = []
        for i in range(len(itemsString)):
            items.append(int(itemsString[i]))
            utilities.append(int(itemsUtilitiesString[i]))
            if items[i] > self.maxItem:
                self.maxItem = items[i]
        t = Transaction(items, utilities, transactionUtility)
        #t.Print(); #input()
        return t

    def getTransactions(self):
        return self.transactions

    def getMaxItem(self):
        return self.maxItem

    def getTotalUtility(self):
        return self.totalUtility


if __name__ == '__main__':
    dataset = "contextHUIM.txt";
    db = Dataset(dataset);
    print('Done..!')







    

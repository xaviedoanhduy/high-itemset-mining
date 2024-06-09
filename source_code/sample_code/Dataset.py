from Transaction import Transaction
class Dataset:
    def __init__(self, datasetPath):
        self.transactions = []
        self.maxItem = 0
        self.maxNum = 0
        with open(datasetPath) as f:
            for line in f:
                if line=="" or line[0] == '#' or line[0] == '%' or line[0] == '@':
                    continue
                t = self.createTransaction(line)
                if len(t)>self.maxItem: self.maxItem = len(t)
                self.transactions.append(t)

    def createTransaction(self, line):
        itemsString = line.split(' ')
        #print(itemsString)
        items = []
        for i in range(len(itemsString)):
            if itemsString[i]!='\n':
                tmp = itemsString[i].splitlines()
                #print(tmp)
                if len(tmp)==0: continue
                n = int(tmp[0])
                if n>self.maxNum: self.maxNum=n
                items.append(n)
                
        return items

    def getTransactions(self):
        return self.transactions
    def getMaxItem(self):
        return self.maxItem
    def getMaxNum(self):
        return self.maxNum
    

if __name__ == '__main__':
    dataset = "mushroom.txt"
    db = Dataset(dataset);
    #for i in db.getTransactions():
    #    print(i)
    print(db.getTransactions())
    print('Done..!')







    

class Transaction:
    temItems = []
    tempUtilities = []

    
    
    def __init__(self, items, utilities, transactionUtility):
        self.items = items
        self.utilities = utilities
        self.transactionUtility = transactionUtility
        self.offset = 0
        self.prefixUtility = 0

    def getItems(self):
        return self.items

    def getUtilities(self):
        return self.utilities

    def getUtility(self):
        return self.transactionUtility
    def Print(self):
        print(self.items,":",self.transactionUtility,":",self.utilities)

if __name__ == '__main__':
    t = Transaction(0,0,0)

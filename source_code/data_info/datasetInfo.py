from Dataset_info import Dataset

def datasetInfo():
    print("  ___  ___    ___ _  _ ___ ___ ")
    print(" |   \\| _ )__|_ _| \\| | __/ _ \\")
    print(" | |) | _ \\___| || .` | _| (_) |")
    print(" |___/|___/  |___|_|\\_|_| \\___/")
    print()
    print("Loading dataset...")
    dataset = "chainstore.txt"
    try:			
        db = Dataset(dataset)
        print("done.")

        _len =0.0; density=0.0; avgLen=0.0; maxLen=0.0;
        densityThreshold = 1.0E-2
        
        for transaction in db.getTransactions():
            _len = len( transaction.getItems())
            avgLen += _len
            if maxLen < _len:
                maxLen = _len
        avgLen /= len(db.getTransactions())
        density = avgLen / db.getMaxItem()
        			
        print("===============[ "+dataset+" ]===============")
        print(". Total transactions: %d"%len(db.getTransactions()))
        print(". Total items       : %d" % db.getMaxItem())
        print(". Total utility     : %d" % db.getTotalUtility())
        print(". Avg. trans. len.  : %f" % avgLen)
        print(". Max. trans. len.  : %d" % maxLen)
        print(". Density           : %f" % density)
        print(". Type              : Dense" if density > densityThreshold else ". Type              : Sparse");
    except:
        print("failed.")
	

if __name__ == '__main__':
    datasetInfo()

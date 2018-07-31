# 1 Import Python standard Library modules
import hashlib
import json
from collections import OrderedDict,deque

# 2 Define class for the Transaction module
class Transactions():
    
    # 2.1 Defining and setting class attributes (variables)
    transactionID = 0
    pendingTxList = deque([])
    completedTxList = []
    lastID = 0
    txInBlock = 0

        
    # 2.2 Class constructor to set the state of transaction ID's and queue.
    def __init__(self):
        self.transactionID = Transactions.transactionID
        self.pastTransaction = OrderedDict()

        
    # 2.3 Class method to create the merkel tree and merkel root. 
    def createTree(self):
        listOfTransaction = Transactions.completedTxList
        
        pastTransaction = self.pastTransaction
        tempTransaction = []
        #2.3.1 For every element in the transaction list, skipping 1 at a time
        for index in range(0,len(listOfTransaction),2):
            current = listOfTransaction[index]

            # 2.3.2 If element to the right of the current index is NOT end of list
            if index+1 != len(listOfTransaction):
                
                #2.3.3 Set currentRight to index right of current index 
                currentRight = listOfTransaction[index+1]
            else:
                currentRight = ''

            # 2.3.4 Hashes the element set to variable current
            currentHash = hashlib.sha256((str(current)).encode())
            
            # 2.3.5 If current right is not empty, hash that too
            if currentRight != '':
                currentRightHash = hashlib.sha256((str(currentRight)).encode())
                
            # 2.3.6 Overwrite current value with hash of itself.
            pastTransaction[listOfTransaction[index]] = currentHash.hexdigest()
            
            # 2.3.7 If current right is not empty, replace itself with hash too.
            if currentRight != '':
                pastTransaction[listOfTransaction[index+1]] = currentRightHash.hexdigest()

            # 2.3.8 If currentRight is not empty, create a temporary variable
            #       and concatenate both hashes together.
            if currentRight != '':
                tempTransaction.append(currentHash.hexdigest() + currentRightHash.hexdigest())

            # 2.3.9 if current hash is by itself, add to temp variable
            else:
                tempTransaction.append(currentHash.hexdigest())
                
        # 2.4 base case for recursive createTree() function
        if len(listOfTransaction) != 1:
            
            # 2.4.1 Append the temp trasactions to complted tx list.
            Transactions.completedTxList = tempTransaction
            self.pastTransaction = pastTransaction
            
            # 2.4.2 Call fuction recursively untill length of transaction
            #       list is 1
            self.createTree()


    # 3 Class method to return full dictionary of past transactions.
    def getPastTransaction(self):
        return self.pastTransaction


    # 4 Class method to sort through dictionary of past transaction and return
    #   simply the plain text transactions.
    def printTx(self):
        
        transactions = []
        
        # 4.1 Gather list of all hashes and plaintext info from previous txn.
        txKeys = list(self.pastTransaction.keys())
        for element in txKeys:
            
            # 4.1 If the key is a tuple, append the unhashed tuple to list
            if type(element)== tuple:
                transactions.append(element)
                
        # 4.2 If the length of the transaction list is not 0 return it
        if len(transactions) != 0:
            self.pastTransaction.clear()
            return transactions
        else:
            return False

    
    # 5  Class method to return merkel root of merkel tree.
    def getRootLeaf(self):
        lastKey = list(self.pastTransaction.keys())[-1]
        return self.pastTransaction[lastKey]


    # 6 Class method to add tuple of a new transaction to pending tx list.
    def newTransaction(self, sender, reciever, amount):
        self.transactionID += 1
        transaction = (self.transactionID, sender, reciever, amount)
        Transactions.pendingTxList.append(transaction)
        return True

    
    # 7 Class method to process all transactions in the pending tx list.
    def processTx(self):
        
        # 7.1 For every transaction in the queue
        for element in list(Transactions.pendingTxList):
            currentTx = element
            
            # 7.1.1 If the current Transaction is a test transaction
            if currentTx[1].startswith("MBC") == False:
                        Transactions.pendingTxList.popleft()
                        Transactions.completedTxList.append(currentTx)
            

            # 7.1.2 If transaction is not a test transaction,
            #  Obtainin wallet IDs and checking addresses are in the system
            else:
                with open('MiniBlockChainWallets.json', 'r') as userWalletsJSON:
                    try:
                        walletData = json.load(userWalletsJSON)
                    # 7.1.3 If the wallet JSON file is empty, do nothing.
                    except json.decoder.JSONDecodeError:
                        pass
                    
                i = 0
                # 7.1.4 Searches JSON file for wallet information
                for key in walletData:
                    
                    # 7.1.5 If a match is found for both sender and recipient
                    #       Add and Take away where applicable and increment
                    #       Transactions send/recv by 1
                    if currentTx[1] == key[str(i)]['address']:
                        senderID = str(i)
                        key[senderID]['moneyValue'] -= int(currentTx[3])
                        key[senderID]['txSent'] += 1
                        
                    if currentTx[2] == key[str(i)]['address']:
                        recipientID = str(i)
                        key[recipientID]['moneyValue'] += int(currentTx[3])
                        key[recipientID]['txRecieved'] += 1
                           
                    i += 1
                # 7.2 After movement of MBC is performed, save wallets to JSON
                with open ('MiniBlockChainWallets.json', 'w') as userWalletsJSON:
                        json.dump(walletData, userWalletsJSON, sort_keys=True, indent=4)    
                    
                # 7.3 Pop transaction from list and loop untill all are processed.
                Transactions.pendingTxList.popleft()
                Transactions.completedTxList.append(currentTx)
                print("Transactions processed and added to block.")


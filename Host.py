# 1.1 Import Standard Library modules
import json
import sys

# 1.2 To see if flask is present and installed on user's system.
try:
    from flask import Flask, request, jsonify
except ImportError:
    print("ImportError: flask was not found on your Computer.")
    print("Make sure pip is installed and working, then run the following command in a shell: \n")
    print(" "*20,"pip install flask\n")
    print("-"*50)
    input("Press Enter to quit.\n")
    sys.exit()

# 1.3 Import serverside programs
import MiniBlockChainV3
import Wallet
import TransactionsV3
import Miner


# 2.1 Set Variables TX and MBC to appear in Global Scope.
global TX
global MBC

# 2.2 Creates instance of Transaction class.
TX = TransactionsV3.Transactions()

# 2.3 Creates instance of MiniBlockChain class.
MBC = MiniBlockChainV3.MiniBlockChain()

# NOTE: Instances of both the Blockchain and Transactions are called at
#       the global level because of the way the classes are designed.
#       I.E: a different blockchain will be created for each new instance
#       of the class.


# 3.1 Creates instance of Flask class.
app=Flask(__name__)

# 4. Route to return blockchain
@app.route("/BlockChain/", methods = ['POST'])
def returnBlockData():
    try:
        blockNum = dict(request.get_json())
        print(blockNum)
        # 4.1 Returns output of returnBlockChain function (returns whole blockchain to client)
        return jsonify(MBC.returnBlock(blockNum['num']))
    except TypeError:
        return jsonify(MBC.returnBlockChain())


# 5. Route to return a user's wallet on login
@app.route("/WalletLogin/", methods = ['POST'])
def returnUserWallet():
    # 5.1 Requests user's login information from client
    data = dict(request.get_json())
    
    # 5.2 Attempts to log the user in
    walletData = Wallet.loadWallet(data['uHash'])

    # 5.3 Returns output of loadWallet function, either the wallet data or bool False.
    return (jsonify(walletData))

        
# 6. Route to add a new wallet
@app.route("/WalletNew/", methods = ['POST'])
def returnNewWallet():
    # 6.1 Requests new wallet info from client
    data = dict(request.get_json())
    pKey = Wallet.newWallet(data['uHash'])
    
    # 6.2 Returns output of the new wallet being created (Returns private key of new wallet)
    return jsonify({'pKey':pKey})


# 7. Route to accept an incoming transaction request and add to queue
@app.route("/sendTX/", methods = ['POST'])
def sendTx():
    # 7.1 requests transaction info from client
    txData = dict(request.get_json())
    
    # 7.2 Attempts to add the new transaction to queue
    txStatus = TX.newTransaction(txData['sender'],
                                 txData['recipient'],
                                 txData['moneyVal'])
    
  
    # 7.3 Return True if transaction was addes successfully, else return False.
    if txStatus == True:
        return jsonify({'status':True})
    else:
        return jsonify({'status':False})
    

# 8. Route to check a user input address is on server.
@app.route('/AddressCheck/', methods = ['POST'])
def checkAddr():
    # 8.1 Requests addresses to be checked from client program
    addresses = dict(request.get_json())

    # 8.2 Opens JSON file and decodes JSON Objects to Dictionaries
    with open ('MiniBlockChainWallets.json' ,'r') as walletJSON:
        wallets = json.load(walletJSON)
        
        #8.2.1 If sender address isnt the same as recipient 
    if addresses['sender'] != addresses['recipient']:
        i = 0
        
            # 8.2. Loop through every walletID in the JSON file
        for key in wallets:
            #print (key)
            # 8.2.3 If address in JSON is same as address of recipient
            if key[str(i)]['address'] == addresses['recipient']:
                return jsonify({'status':True})
            else:
                i += 1
            
        # 8.3 If no wallet matches found, return False.    
    return jsonify({'status' : False})

            
# 9. Route to execute mining of a block. 
@app.route('/mineBlock/', methods=['GET'])
def mineBlock():
    # 9.1 Adds transaction to queue to ensure merkel root is always computed.
    TX.newTransaction("Harry", "Bob", 10)

    # 9.2 Processes all pending transactions and creates Merkel Tree for block.
    TX.processTx()

    #9.3 Mines block and sets Block status to value of the mineBlock function
    blockStatus = Miner.mineBlock(MBC,TX)

    # 9.4 If block mines successfully, return True, otherwise return False.
    if blockStatus == True:
        return jsonify({'status':True})
    else:
        return jsonify({'status':False})

#10. Route to return list of transactions from a block.
@app.route('/returnTx/', methods=['GET'])
def getTx():
    data = {'txList':TX.printTx()}
    return jsonify(data)

# Test.
@app.route("/POSTTEST/", methods = ['POST'])
def test():
    req_data = request.get_json()
    return (jsonify(req_data))

if __name__ =='__main__':
    app.run()

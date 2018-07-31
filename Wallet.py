# 1. Import Standard Library Modules
import hashlib
import csv
import json
from secrets import token_hex

# 2. Declares walletID as global Variable and sets it to 0.
global walletID
walletID = 0


''' 3. Method for loading wallets into program

        Takes login Data and finds the wallet hash associated with it.
'''
def loadWallet(uHash):
    # 3.1 opens JSON file and loads wallet data into pythonic dictionaries
    with open ('MiniBlockChainWallets.json','r') as userWalletsJSON:
        walletData = json.load(userWalletsJSON)
    i=0
    # 3.2 loop through every walletID in JSON file
    for key in walletData:
        
        # 3.2.1 If a wallet's user hash is identical to one sent by client
            if key[str(i)]['uHash'] == uHash:
                
                #3.2.2 return the user's wallet
                userWallet = key[str(i)]
                return userWallet
            
            # 3.2.3 If no match, go to next walletID
            else:
                i += 1
            
''' Function to make a wallet Address.
        Creates a wallet hash (address) by generating a random 64 byte string
        and converting it into a 32 hex digit string that is hashed 256 times.
        MBC appended to the front of the wallet address
        returns the Address
'''

def newWalletAddr(walletAddr=None):
    # 4.1 Loop 256 times
    for i in range (0,255):
        
        # 4.2 Create a new hexadecimal string 32 bytes long and add it to hash
        walletPreHash = str(walletAddr)+str(token_hex(32))
        
        #4.2.1 Hashes hex string + previous hash
        walletAddr = hashlib.md5((str(walletPreHash)).encode()).hexdigest()
        
        #4.3 Adds MBC to front of hash value and returns address.
    walletAddr = "MBC" + walletAddr
    return walletAddr


# 5 New wallet
def newWallet(uHash):
    # 5.1 Opens JSON file
    with open('MiniBlockChainWallets.json','r') as userIDNum:
        
        # 5.2 Sets the walletID of new wallet to the length of all other walletID's + 1
        try:
            IDNum = json.load(userIDNum)
            walletID = len(IDNum)
            print(walletID)
            print(len(IDNum))
            
        #5.2.1 If JSON load returns with error, set WalletID to 0
        except Exception:
            walletID = 0
            pass
    # 5.3 Generate new Private key for wallet
    privKey = token_hex(32)
    
    # 5.4 Creates hash of username, password and private key.
    walletHash = hashlib.sha256((str(uHash)+str(privKey)).encode()).hexdigest()
    
    # 5.5 Creates Dictionary containing the new wallet's data
    uWallet = {'uHash' : walletHash,
               'address' : newWalletAddr(),
               'moneyName' : "MBC",
               'moneyValue' : 10,
               'txSent' : 0,
               'txRecieved' :0}
    
    # 5.6 Creates nested Dictionary with walletID as the key and new Wallet data as value.
    uWalletID = {walletID:uWallet}
    
    # 5.7 Loads JSON data once again
    try:
        with open('MiniBlockChainWallets.json','r') as userWalletsJSON:
            
            # 5.7.1 Due to JSON x is a list with all wallet Dictionaries inside it.
            x = json.load(userWalletsJSON)
            
    # 5.7.2 If JSON file is empty, set x as empty list
    except json.decoder.JSONDecodeError:
        x=[]
        pass
    
    # 5.8 Appends new wallet to the end of wallet list and overwrites JSON data.
    with open ('MiniBlockChainWallets.json', 'w') as userWalletsJSON:
        x.append(uWalletID)
        json.dump(x, userWalletsJSON, sort_keys=True, indent=4)
        print("New wallet created")
        
    # 5.9 Returns user's private key
    return privKey


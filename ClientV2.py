# 1.1 Import standard Library modules
import json
import os,sys,platform
from time import sleep
import threading
import hashlib

# 1.2 Try to import requests, if not present inform user to install it.
try:
    import requests
except ImportError:
    print("ImportError: requests not found. Please install it to continue")
    print("Please ensure you have pip installed and enter the following command \n")
    print("NOTE: if you have installed Python for Windows 3.xx you will have pip installed.\n")
    print(" "*20,"pip install requests\n")
    print("-"*50)
    input("Enter to quit")
    sys.exit()


# 2.1 Set IP address the client will POST and GET data to and from. 
IP_ADDRESS = ("127.0.0.1:5000") # Change this to the IP address the Host File is serving

# 3.1 Discovers type of Operating System to ensure correct clear command is used. 
osType = platform.system()

if osType == "Linux" or osType == "Darwin": # Darwin = MacOS
    clearTerminal = 'clear'
elif osType == "Windows":
    clearTerminal = 'cls'

# 4 Defines Client Class
class Client():
    # 4.1 Class Attribute that gets set to user's current wallet.
    currentWallet = ""


    def serverRequest(self,route,data,method):
        if method == "GET":
            r = requests.get('http://'+IP_ADDRESS+route)
        elif method == "POST":
            r = requests.post(('http://'+IP_ADDRESS+route),
                                 json = data)
        return (r.json())
            
    def printFullBlockchain(self):
        blockChain = self.serverRequest('/BlockChain/',None,'POST')
        os.system(clearTerminal)
        for key in blockChain:
            print ("Block: {}".format(blockChain[key]['blockId']))
            print ("Was created on: {}".format(blockChain[key]['timeStamp']))
            print ("Has the hash: {}".format(blockChain[key]['currHash']))
            print ("The hash of the previous block is: {}".format(blockChain[key]['prevHash']))
            print ("It has {} confirmations".format(blockChain[key]['confirms']))
            print ("Finally, it's merkel root is: {}".format(blockChain[key]['merkelRoot']))
            print("-"*50+"\n"*2)
                
    def printBlockInfo(self, blockNum):
        if blockNum == "":
            return "InputError: Please input a block number!"
        else:
            os.system(clearTerminal)
            block = self.serverRequest('/BlockChain/',{'num':blockNum},'POST')
            
            print(" "*25,"Block {}".format(blockNum))
            print("Has the hash: {0}\nIt was created on: {1} ".format(block['currHash'],
                                                               block['timeStamp']))
            print("Finally, it has {} confirmations".format(block['confirms']))
            
            userChoice = input("Would you like to see the transactions? Y/N")
            if userChoice.lower() == "y":
                print("Transactions for block {} are as follows:".format(blockNum))
                for tx in block['transactions']:
                    print("{t[1]} sent {t[3]} MBC to {t[2]}.".format(t=tx))
            elif userChoice.lower() == "n":
                pass
            else:
                print("Error")

    def walletLogin(self):
        os.system(clearTerminal)
        a = True
        while a == True:
            userChoice = str(input("Welcome, do you have a wallet?\n"
                               + "1.Yes\n"
                               + "2. No\n"
                               + "Enter. Back to Main Menu\n"))
            if userChoice in ['Yes','yes','y','Y','1']:
                print("Please Login to your wallet\n")
                walletInfo = self.walletRefresh()
                self.walletMenu(walletInfo)
                a = False
                
            elif userChoice in ['No','no','n','N','2']:
                print("Create a New Wallet")
                uName = input("Please enter a username:\n")
                pWord = input("please enter a password:\n")
                userHash = hashlib.sha256((str(uName)
                                           +str(pWord)).encode()).hexdigest()

                data = {'uHash':userHash}

                
                privKey = self.serverRequest('/WalletNew/',data,'POST')
                
                print("Your private key is:{}".format(privKey['pKey']))
                print("WARNING: DO NOT LOSE YOUR KEY, IF YOU DO, YOU LOSE YOUR WALLET")
                print("Now, please login to your wallet!")
                userChoice = "y"
            elif userChoice == "":
                a = False
            else:
                print('InputError: Please input only "Y" or "N".')
                sleep(1)
                
    def walletRefresh(self):
        os.system(clearTerminal)
        uName = input("What is your Username?\n")
        pWord = input("What is your Password?\n")
        privKey = input("What is your Private Key?\n")
        
        # Hashes user information client side to prevent plain text being transmitted.
        walletHash = hashlib.sha256((str(uName)
                                    +str(pWord)).encode()).hexdigest()
        
        walletHash = hashlib.sha256((str(walletHash)
                                     + str(privKey)).encode()).hexdigest()

        data = {'uHash':walletHash}
        
        walletData = self.serverRequest('/WalletLogin/',data,'POST')
        return walletData

    def walletMenu(self,walletInfo):
        os.system(clearTerminal)
        Client.currentWallet = walletInfo
        try:
            print("Welcome Login Successful!\nYour Wallet address is: ",str(walletInfo['address']))
            print("You currently have:",str(walletInfo['moneyValue']),"MBC in your wallet.")
            print("-"*50)
        except TypeError:
            print("LoginError: Incorrect login information.\n"
                  +"Please enter the correct details or make a wallet if you dont have one")
            return None
        try:
            while True:
                userChoice = int(input("What would you like to do?\n"
                                       + "1. Send Transaction\n"
                                       + "2. Generate new address\n"
                                       + "3. Logout\n"))
                if userChoice == 1:
                    self.txMenu(walletInfo)
                elif userChoice == 2:
                    print("Feature coming soon")
                elif userChoice == 3:
                    Client.currentWallet = ""
                    break
        except ValueError:
            print ("InputError: Please enter a number that corresponds to a menu item")

            
    def txMenu(self,walletInfo):
        os.system(clearTerminal)
        a = True
        while a == True:
            try:
                recipient = input("Enter the address you wish to send MBC to:\n")
                if self.checkAddress(walletInfo['address'],recipient) == True:
    
                    b = True
                    while b == True:
                        print("How much MBC do you wish to send? Max: ",walletInfo['moneyValue'],"MBC.")
                        moneyVal = input()
                        try:
                            if int(moneyVal) <= int(walletInfo['moneyValue']) and int(moneyVal) > 0:
                                b = False
                                print("Are you sure you wish to send", str(moneyVal), "to",str(recipient),"? Y/N")
                                confirm = input()
                                if confirm.lower() == "y":
                                    a = False
                                    txData = {'sender':walletInfo['address'],
                                              'recipient':recipient,
                                              'moneyVal':moneyVal}
                                    txRequest = self.serverRequest('/sendTX/',txData,'POST')
                                    if txRequest['status'] == True:
                                        print("-"*50)
                                        print("Success, your transaction has been added to the queue.")
                                        print("Mine a block to have your transaction added to the Blockchain.")
                                        #print("NOTE: You will need to logout of your wallet to see your MBC value change.")
                                    else: print("Trasaction Failed.\n")
                                    
                                else:
                                    print("Transaction cancelled.\n")
                                    a = False
                                
                                
                            else: raise ValueError    
                        except ValueError:
                            print("ValueError: Please input a whole number greater than or equal to 0 and less than or equal to your amount of MBC.\n")

            except ValueError:
                print("InputError: Please input a valid address.\n")

                
    def checkAddress(self, sender, recipient):
        data = {'sender':sender,
                     'recipient' : recipient}
        check = self.serverRequest('/AddressCheck/',data,'POST')
        
        if check['status'] == True:
            return True
        else:
            return False

    def mineBlockMenu(self):
        os.system(clearTerminal)
        print("NOTE: There will always be 1 transaction in each block, even if you haven't added one.\n")
        print("This is to prevent any errors with the creation of a merkel tree.")
        print("Mining Block, please wait...")
        sleep(2) # To let user read information

        mineRequest = self.serverRequest('/mineBlock/',None,'GET')
        if mineRequest['status'] == True:
            print("\n","-"*50)
            print("Block Mined Successfully!")
            print("\n","-"*50)
        else:
            print ("ForgingError: Block data not sent by server.")


            
    def mainMenu(self):
        print(" "*10,"Welcome to the MiniBlockchain.")
        print(" "*20,"Harry Smith")
        print(" "*14,"harry.ej.smith@gmail.com\n")
        print("-"*50,"\n")
        while True:
            print("-"*20+"Main Menu"+"-"*20)
            print("What do you want to do?")
            userChoice = int(input("1. What is this?\n"
                                  + "2. Mine a Block\n"
                                  + "3. View a single Block\n"
                                  + "4. View whole Blockchain\n"
                                  + "5. Wallets and Transactions\n"))
            
            if userChoice == 1:
                print("The Mini Blockchain Project is a simple implementation of a blockchain.\n"
               + "Powered completely by Python and written by a University Undergraduate, "
               + "it's aim is to explain the world of Blockchains in a simple manner, "
               + "enabling more people to understand the intricate behaviour of a Blockchain. ")
                print("-"*50,"\n")
                input("Press Enter to return to main menu\n")
            elif userChoice == 2:
                self.mineBlockMenu()
            elif userChoice == 3:
                blockNum = input("What block number would you like to view?\n")
                self.printBlockInfo(int(blockNum))
                print("-"*50)
            elif userChoice == 4:
                self.printFullBlockchain()
            elif userChoice == 5:
                self.walletLogin()
            elif userChoice > 5:
                raise ValueError
                
if __name__=='__main__':
    client = Client()
    
    client.mainMenu()

        

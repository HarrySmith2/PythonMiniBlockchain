# 1.1 Importing standard libary modules
import threading
import hashlib
from datetime import datetime

# 2.1 Defining the class for the Mini Blockchain
class MiniBlockChain():
    blockID = 0
    blocks = {}
    #2.2 Constructor that sets variables that act as the genesis block's data.
    def __init__(self):
        self.blockIDNum = MiniBlockChain.blockID
        self.timeStamp = datetime.now()
        self.hashCash = "1:abcdefghi"
        self.prevHash = "GenesisGenesisGenesisGenesisGenesisGenesisGenesis"
        self.txRootHash = "Send Lots of monies"
        self.blockData = {}
        self.currHash = self.genesisBlock()
        

    # 2.3 Class method to generate and return hash for a genesis block.
    def genesisBlock(self):
        genesisHash = hashlib.sha256((("Fidget is a very fast midget"
                                       + str(self.timeStamp)
                                       + self.txRootHash
                                       + self.prevHash)).encode()).hexdigest()

        self.blockData = {'blockId' : MiniBlockChain.blockID,
                         'hashcash': self.hashCash,
                         'timeStamp': self.timeStamp,
                         'prevHash': self.prevHash,
                         'merkelRoot': "N/A",
                         'currHash': genesisHash,
                         'confirms': 0,
                         'transactions':None}
        MiniBlockChain.blocks[self.blockIDNum] = self.blockData
        return genesisHash

    # 2.4 Class method to generate a new block after mining has been finalised.
    def newBlock(self,hashCash, merkelRoot,txData):
        MiniBlockChain.blockID += 1
        self.hashCash = hashCash
        self.blockIDNum = MiniBlockChain.blockID
        self.timeStamp = datetime.now()
        self.prevHash = self.currHash
        self.txRootHash = merkelRoot
        self.currHash = hashlib.sha256(((self.prevHash
                                         + str(self.timeStamp)
                                         + self.txRootHash)).encode()).hexdigest()
        self.blockData = {'blockId' : self.blockIDNum,
                         'hashcash': self.hashCash,
                         'timeStamp': self.timeStamp,
                         'prevHash': self.prevHash,
                         'merkelRoot': self.txRootHash,
                         'currHash': self.currHash,
                         'confirms': 0,
                         'transactions':txData}
        MiniBlockChain.blocks[self.blockIDNum] = self.blockData
        
    # 2.5 Class Method to return current state of the whole blockchain
    def returnBlockChain(self):
        return MiniBlockChain.blocks
    # 2.6 Class Method to return current state of a selected block.
    def returnBlock(self, blockNum):
        return (MiniBlockChain.blocks[blockNum])



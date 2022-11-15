# import torch
# x = torch.rand(5, 3)
# print(x)
from bigchaindb_driver import BigchainDB


bdb_root = 'http://localhost:9984'
bdb = BigchainDB(bdb_root)
tokens = {}


print(bdb)

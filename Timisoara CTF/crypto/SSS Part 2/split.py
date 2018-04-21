from sss import SSS
from random import sample
import random

flag = "***"
splitter = SSS(16,13) # 16 shares; at least 13 needed for reconstruction

shares = {}
#split the secret into chunks and split every chunk using sss
for i in range(0, len(flag), 10):
    shares["chunk_" + str(i/10)] = splitter.split_secret(flag[i:i+10])


# delete random splits
for chunk_num, chunk_shares in shares.iteritems():
    shares[chunk_num] = sample(chunk_shares, 10)

print shares

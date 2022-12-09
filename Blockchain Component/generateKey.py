import random
import string

"""A file to generate the identity key to be make transaction with client. 
"""
key = []
file1 = open("key.txt", "w")
for i in range(105):
    num = ''.join(random.choices(string.ascii_letters, k= 105))
    key.append(num)
    file1.write(num)
    file1.write("\n")
print(key)
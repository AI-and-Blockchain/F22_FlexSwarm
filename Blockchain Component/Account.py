class Account:
    """A class to save the issuers address and private key. Hide the private key from the public.
    """
    def __init__(self, address, private_key):
        self.public_key = address
        self.private_key = private_key
        self.token = 100
    

    # A function to add token
    def addToken(self, number):
        self.token += number

    # A functino to minus token
    def minToken(self, number):
        self.token -= number

    # A function to return a token
    def getToken(self):
        return self.token

    # A function to check the token
    def ableToPurchase(self, amount):
        return self.token >= amount

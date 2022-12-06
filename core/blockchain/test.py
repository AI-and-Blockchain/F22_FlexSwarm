import json
from dotenv import dotenv_values
from algosdk.v2client import algod
from algosdk import account, mnemonic
import algosdk.future.transaction as afTxn

# create client
def client_init( mnemonics: str ):
  account = {}
  account['pk'] = mnemonic.to_public_key(mnemonics)
  account['sk'] = mnemonic.to_private_key(mnemonics) 

  algod_base_server = "https://testnet-algorand.api.purestake.io/ps2"

  
  config = dotenv_values('.env')
  algod_token = config['PURESTAKE_TOKEN']
  headers = {
    "X-API-Key": algod_token,
  }
  algod_client = algod.AlgodClient(algod_token, algod_base_server, headers)



if __name__ == "__main__":
  client_init("")
  # pass
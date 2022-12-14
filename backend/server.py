from flask import Flask, request, jsonify
from flask_cors import CORS

import sys
sys.path.append("..")
# Change path to access sibling directory module
from core.blockchain.smart import generate_algorand_keypair

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
app.config['DEBUG'] = True


# Testing endpoint
@app.route('/', methods=['Get'])
def index():

  res = jsonify({'data': "SLFL Simulation"})
  res.headers.add('Access-Control-Allow-Origin', '*')
  return res


@app.route('/account', methods=['Get'])
def account():
  res = jsonify({'account': 1})
  res.headers.add('Access-Control-Allow-Origin', '*')
  return res



@app.route('/generateAcnt', methods=['Post'])
def generateAcnt():
  """
  Send response as a json object with genereated algorand keypair
  {
    'address': address,
    'private_key': private_key,
    'passphrase': passphrase,
  }
  """

  data = request.json
  userName = data['params']['name']
  address, private_key, passphrase = generate_algorand_keypair(userName)

  ret = {
    'address': address,
    'private_key': private_key,
    'passphrase': passphrase,
  }
  print(ret)
  return jsonify(ret)


# @app.route('/modelUpload', methods=['POST'])
# def modelUpload():




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8888)
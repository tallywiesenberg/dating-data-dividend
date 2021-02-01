import json

from decouple import config
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from web3 import Web3

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'
sess = Session()

#web3: connect to smart contract
w3 = Web3(Web3.HTTPProvider(config('MAINNET_URL')))
w3.eth.defaultAccount = w3.eth.accounts[0]

lillith = w3.eth.contract(
    address=Web3.toChecksumAddress(config('CONTRACT_ADDRESS')),
    abi=json.load(open('Lillith.json', 'r'))['abi']
)

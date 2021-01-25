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
lillith = w3.eth.contract(
    address=Web3.toChecksumAddress('0xe4bfde59d11001a6e0b8784635871b8d69d2b97a'),
    abi=json.load(open('Lillith.json', 'r'))['abi']
)

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

Restapp = Flask(__name__)
Restapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
Restapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Restapp.secret_key = 'debayan'
api = Api(Restapp)

@Restapp.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(Restapp, authenticate, identity)  #=> Would create a new Endpoint - /auth. Would send username & password

api.add_resource(Item, '/item/<string:name>')  ##http://127.0.0.1:5000/item/<item-name>
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':                  
    db.init_app(Restapp)
    Restapp.run(port=5000, debug=True)             ##debug=True - this will give an html page of error details in case of any error

# When directly run this app, python assigns __main__ to __name__. 
# If it is imported from another app, then it doesn't assign. So, this statement will ensure
# that is this app is imported from another app, then this app would not be run.
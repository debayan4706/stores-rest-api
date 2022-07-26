from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList   

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'debayan'
api = Api(app)

jwt = JWT(app, authenticate, identity)  #=> Would create a new Endpoint - /auth. Would send username & password

api.add_resource(Item, '/item/<string:name>')  ##http://127.0.0.1:5000/item/<item-name>
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':                  
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)             ##debug=True - this will give an html page of error details in case of any error

# When directly run this app, python assigns __main__ to __name__. 
# If it is imported from another app, then it doesn't assign. So, this statement will ensure
# that is this app is imported from another app, then this app would not be run.
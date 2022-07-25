from winreg import QueryInfoKey
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, required=True, 
        help = "This field cannot be left blank!"
    )
    parser.add_argument('store_id', 
        type=int, required=True, 
        help = "Every item requires a Store id!"
    )

    @jwt_required()           # This will ensure that authentication is necessary for get/items end point everytime   
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return{"message": "An item with name '{}' already exists.".format(name)}, 400  #400 http code for Bad Request
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500  #500 - http code for server error

        return item.json(), 201                  #201 - http code for Success

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        else:
            return {'message': 'item doesnot exist'}, 400

        return {'message': 'item deleted.'}

    def put(self, name):
        #data = request.get_json()
        data = Item.parser.parse_args()  ## This ensures that only the above declared fields would be parsed from the JSON. Rest will be ignored
        
        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['price'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

## Filter function - Takes in values from a collection (like list) and operates on a function
## Ideally the function should be like a filtering criteria. So the values that matches 
## would be stored in a filter object. The filter object can be captured using a list function 
## which would return a list object.
## The Next method captures the first value returned by the Filter function. If no value returned
## then it returns the Default value declared with a comma. If no default value then it throws error
##  

class ItemList(Resource):
    def get(self):

        return {'item': [x.json() for x in ItemModel.query.all()]}
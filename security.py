from models.user import UserModel
import hmac

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user

## GET method is used to retrieve a value within a dictionary. We can also declare a default value
## in case there is no key matching the entered value

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)


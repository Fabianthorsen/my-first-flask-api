from code.resources.register import UserModel

# Function to authenticate our user
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


# Identity function
def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)

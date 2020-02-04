import pickle

class UserClass:
    """
	Holds the fields needed for required API features and the login feature
    Note that saving the salt in plaintext is not needed here because
    it's taken care of by bcrypt
    """

    def __init__(self, name='', username='', pswdHash='', salt='', favorites=set()):
        self.name = name
        self.username = username
        self.pswdHash = pswdHash
        # self.salt = salt
        self.favorites = favorites

    def addToFavs(self, name):
    	self.favorites.add(name)


# Created the user dict, added Jennifer user to it
users = {}

jenobj = UserClass(name='Jennifer', username='jen')
users[jenobj.username] = jenobj

# Serialize the users so can access when server starts
pickle.dump(users, open( "users.p", "wb" ) )

# Example deserialization with pickle
# usersFromFile = pickle.load( open( "users.p", "rb" ) )
# print(usersFromFile['jen'].name)
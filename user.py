import pickle

class UserClass:
    """
	Holds the fields that I might want for a user in the future
    """

    def __init__(self, name='', username='', pswdHash='', salt='', favorites=set()):
        self.name = name
        self.username = username
        self.pswdHash = pswdHash
        self.salt = salt
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
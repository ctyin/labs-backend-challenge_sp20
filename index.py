from flask import Flask, request
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
from user import UserClass
import json, pickle, os
import bcrypt
app = Flask(__name__)


"""
On startup, check if the files exist to load from in the directory
If they don't, instantiate an empty data struct
"""
if os.path.isfile('clubs.json'):
	with open('clubs.json') as clubfile:
		clubs_arr = json.load(clubfile)
else:
	clubs_arr = club_obj_list(get_clubs(soupify(get_clubs_html())))

if os.path.isfile('users.p'):
	with open('users.p', 'rb') as userfile:
		users_dict = pickle.load(userfile)
else:
	users_dict = {}


"""
Current user object that changes when logging in/out
"""
curr_user = None

@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/api/clubs', methods=['GET', 'POST'])
def clubs():
	if request.method == 'GET':

		# send the JSON list
		return get_club_json_list(clubs_arr)
	else:
		if not curr_user:
			return "Log in to add your club"

		temp = ClubClass()

		# TODO: Add a scan to check for duplicate club names before adding


		# Assuming that the subsequent AJAX calls will just throw the tags in
		# under the same key. Could easily change to form data I think
		temp.writeName(request.args.get('name'))
		temp.addTagStrings(request.args.getlist('tags'))
		temp.writeDesc(request.args.get('desc'))

		clubs_arr.append(temp)

		return "Successfully submitted club {}".format(temp.name) 

@app.route('/api/user/<username>')
def getUser(username):
	if username in users_dict:
		user_obj = users_dict[username]
		
		# Only return the non-sensitive data on the user object
		tempJSON = {}
		tempJSON['name'] = user_obj.name
		tempJSON['username'] = user_obj.username
		tempJSON['favorites'] = list(user_obj.favorites)

		return json.dumps(tempJSON)
	else:
		return "Username not found!"

@app.route('/api/favorite', methods=['POST'])
def addToFavorites():
	"""
	Adds a club name to the user's favorited set. Increments a club's fav count by 1
	Makes use of set data structure to impl 1 addition per user
	"""

	if not curr_user:
		return "Log in to favorite this club"

	user = request.args.get('user')
	fav = request.args.get('club')

	if user in users_dict:
		if fav not in users_dict[user].favorites:
			users_dict[user].favorites.add(fav)

			# Prob should have made this a dict as well
			for club in clubs_arr:
				if club.name == fav:
					print('Added to club\'s count')
					club.favcount += 1
	else:
		return "Not a valid username"

	return "Success"

@app.route('/api/signup', methods=['POST'])
def addNewUser():
	"""
	Checks if a user exists in the table already. If it's 
	a valid new username, we instantiate it and log the user in.
	Passwords are encoded then handled by bcrypt
	"""

	req_name     = request.args.get('name')
	req_username = request.args.get('username')
	req_password = request.args.get('password')
	
	if req_username in users_dict:
		return 'Username already exists'

	# if the username is unique, continue
	tempUser = UserClass()
	tempUser.name = req_name
	tempUser.username = req_username

	salt = bcrypt.gensalt()
	tempUser.pswdHash = bcrypt.hashpw(req_password.encode('utf-8'), salt)

	# log the user in
	global curr_user
	curr_user = tempUser

	users_dict[req_username] = tempUser

	return "Completed signup. Welcome, {}!".format(req_name)

@app.route('/api/login')
def loginUser():
	global curr_user
	if not curr_user:
		# current user is still None
		req_username = request.args.get('username')
		req_password = request.args.get('password').encode('utf-8')

		if req_username in users_dict:
			saved_user = users_dict[req_username]
			if bcrypt.checkpw(req_password, saved_user.pswdHash):
				curr_user = saved_user
				return "Success! Welcome, {}!".format(saved_user.name)
		
		return 'Username or password incorrect'
	else:
		return 'Please log out first'

@app.route('/api/logout')
def logoutUser():
	global curr_user
	if curr_user:
		curr_user = None
		return 'Logged out'
	else:
		return 'No user is signed in'

# code adapted from https://www.youtube.com/watch?v=7pOXnc5kS54
@app.route('/shutdown', methods=['POST'])
def shutdown_server():
	"""
	Handle writing data to file. Starting to realize my way of storing data
	is kind of dumb but I'm struggling to think of a better way to store it locally
	without introducing a real DB
	"""

	if not curr_user:
		return "You need to be logged in to shut down my server D:<"

	print('Shutdown context hit with post')
	shutdown = request.environ.get('werkzeug.server.shutdown')
	if shutdown is None:
		raise RuntimeError('Function is unavailable')
	else:
		club_arr_to_file(clubs_arr)
		pickle.dump(users_dict, open('users.p', 'wb'))

		shutdown()
		return 'Server is shutting down'

if __name__ == '__main__':
    app.run()

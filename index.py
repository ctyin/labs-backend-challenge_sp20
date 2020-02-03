from flask import Flask, request
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
from user import UserClass
import json, pickle, os
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
		temp = ClubClass()

		print(request.args.getlist('tags'))

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

# code adapted from https://www.youtube.com/watch?v=7pOXnc5kS54
@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown_server():
	"""
	Handle writing data to file. Starting to realize my way of storing data
	is kind of dumb but I can't think of a better way to store it locally
	without introducing a real DB
	"""

	print('Shutdown context hit with post')
	shutdown = request.environ.get('werkzeug.server.shutdown')
	if shutdown is None:
		raise RuntimeError('Function is unavailable')
	else:
		club_arr_to_file(clubs_arr)
		pickle.dump(users_dict, open('users.p', 'wb'))

		shutdown()

if __name__ == '__main__':
    app.run()

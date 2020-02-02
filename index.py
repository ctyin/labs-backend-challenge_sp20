from flask import Flask, request
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
app = Flask(__name__)


@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/api/clubs', methods=['GET', 'POST'])
def clubs():
	if request.method == 'GET':
		club_list = get_clubs(soupify(get_clubs_html()))

		# send the JSON list
		return get_club_obj_list(club_list)
	else:


if __name__ == '__main__':
    app.run()

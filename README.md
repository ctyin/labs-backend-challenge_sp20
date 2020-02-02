# Penn Labs Server Challenge

## Documentation
In order to store the clubs, I save them to a JSON file. I chose the JSON file route for the following reasons:
   * Persistence: to prevent having to rescrape the website, I didn't want to store the clubs in-memory. The only other option I was seriously considering was pickling. However, JSON is a more widely used standard and is not Python-specific. Looking ahead, this will also be helpful in my `GET /api/clubs` route.
   * Ease of use: the JSON module in Python is pretty clean. The Python object fields I needed easily become JSON objects; Python arrays become JSON arrays without much thought.

In order to store the users, I am creating a dictionary that maps usernames to user objects. Because my objects are more complex and are using the Python `Set` datatype, I will be using pickle to intermittently serialize the data to a file. I will have it initially serialized to a file and then deserialized into an in-memory dict when the app starts. The downside is that pickle files are hackable/non-readable so deploying this scheme remotely is probably a bad idea if it's being transferred over a network. You can find this code in `user.py`


## Installation
1. Click the green "use this template" button to make your own copy of this repository, and clone it. 
2. Change directory into the cloned repository.
3. Install `pipenv`
   * `brew install pipenv` if you're on a Mac with [`homebrew`](https://brew.sh/) installed.
   * `pip install --user --upgrade pipenv` for most other machines.
4. Install packages using `pipenv install`.

## Developing
1. ~Use `pipenv run index.py` to run the project.~
1. I was having trouble using pipenv run. Instead the commands `export FLASK_APP=index.py` followed by `flask run` was how I got it working.
2. Follow the instructions [here](https://www.notion.so/pennlabs/Server-Challenge-Spring-20-5a14bc18fb2f44ba90a61ba86b6fc426).
3. Document your work in this `README.md` file.

## Submitting
Follow the instructions at on the Technical Challenge page for submission.

## Installing Additional Packages
Use any tools you think are relevant to the challenge! To install additional packages 
run `pipenv install <package_name>` within the directory. Make sure to document your additions.

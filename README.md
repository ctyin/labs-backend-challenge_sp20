# Penn Labs Server Challenge

## Documentation
In order to store the clubs, I save them to a JSON file. I chose the JSON file route for the following reasons:
   * Persistence: to prevent having to rescrape the website, I didn't want to store the clubs in-memory. The only other option I was seriously considering was pickling. However, JSON is a more widely used standard and is not Python-specific. Looking ahead, this will also be helpful in my `GET /api/clubs` route.
   * Ease of use: the JSON module in Python is pretty clean. The Python object fields I needed easily become JSON objects; Python arrays become JSON arrays without much thought.

Unfortunately, I lacked the foresight to ensure that I could convert from JSON back to Python objects. Therefore the majority of my actual API stuff is written as if I had access to the objects themselves and most of my methods fail when I load the data from file instead of scraping the website directly. If I were to do it again, I'd probably just pickle my objects because that seems to work for the users. Also storing the data in different ways for clubs and users doesn't make much sense in hindsight.

I attempted to write the clubs to file when the `shutdown` route receives a request. It successfully will write to file the first time, but it is one of the many features which fails when data is loaded from file.

In order to store the users, I am creating a dictionary that maps usernames to user objects. Because my objects are more complex and are using the Python `Set` datatype, I will be using pickle to intermittently serialize the data to a file. I will have it initially serialized to a file and then deserialized into an in-memory dict when the app starts. The downside is that pickle files are hackable/non-readable so deploying this scheme remotely is probably a bad idea if it's being transferred over a network. You can find this code in `user.py`

With my schema of saving club objects as an array, modifying them is pretty straight-forward. Perform a linear search and update the field. I do this in the `/api/favorite` route for example.

## My own additions
It didn't make sense for me to put the user class definition in either of the provided python files so I made a new one called user.py where I also hardcode the Jennifer object.

In order to implement the signup/login/logout features, I needed to add the following modifications:
   * Creating a global "current user." I wasn't sure how to handle logging in multiple users at once or if that even made sense for my server. All this does it keep track of the current user object and the server queries against that object in subsequent requests. Note that Python has some relatively wonky behavior with global variables so remember to use the `global` keyword before trying to change or modify the object (spend like 20 min debugging that ://)
   * Added the hashed-password field to my user object. Bcrypt makes salted hashing pretty simple because I was originally anticipating having to save the random nonce separately in the user object (bcrypt stores the nonce concatenated with the password, so we only save one password field).
   * Added the `/api/login`, `/api/logout`, and `/api/signup` endpoints. There seems to be an existing distinction between the `/ ` endpoint and the `/api/` endpoint so I tried to maintain it for this feature.

## Packages introduced
I included in the Pipfile the `requests` package because I needed to get the HTML from a website in the web scraper. I also added bcrypt as suggested to implement the sign up/login/logout behavior. These should be installed automatically when `pipenv install` is run

## Installation
1. Click the green "use this template" button to make your own copy of this repository, and clone it. 
2. Change directory into the cloned repository.
3. Install `pipenv`
   * `brew install pipenv` if you're on a Mac with [`homebrew`](https://brew.sh/) installed.
   * `pip install --user --upgrade pipenv` for most other machines.
4. Install packages using `pipenv install`.

## Developing
1. ~Use `pipenv run index.py` to run the project.~
I was having trouble using pipenv run. Instead the commands `export FLASK_APP=index.py` followed by `flask run` was how I got it working.
2. Follow the instructions [here](https://www.notion.so/pennlabs/Server-Challenge-Spring-20-5a14bc18fb2f44ba90a61ba86b6fc426).
3. Document your work in this `README.md` file.

## Submitting
Follow the instructions at on the Technical Challenge page for submission.

## Installing Additional Packages
Use any tools you think are relevant to the challenge! To install additional packages 
run `pipenv install <package_name>` within the directory. Make sure to document your additions.

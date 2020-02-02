# Penn Labs Server Challenge

## Documentation
In order to store the clubs, I chose the JSON file route for the following reasons:
   * Persistence: to prevent having to rescrape the website, I didn't want to store the clubs in-memory. The only other option I was seriously considering was pickling. However, JSON is a more widely used standard and is not Python-specific. In the future, I would probably want to store this information in a database like MongoDB which uses JSON as well.
   * Ease of use: the JSON module in Python is pretty clean. Python object fields become dictionaries become JSON objects, and it easily transforms arrays to JSON arrays without much thought. 

## Installation
1. Click the green "use this template" button to make your own copy of this repository, and clone it. 
2. Change directory into the cloned repository.
3. Install `pipenv`
   * `brew install pipenv` if you're on a Mac with [`homebrew`](https://brew.sh/) installed.
   * `pip install --user --upgrade pipenv` for most other machines.
4. Install packages using `pipenv install`.

## Developing
1. Use `pipenv run index.py` to run the project.
2. Follow the instructions [here](https://www.notion.so/pennlabs/Server-Challenge-Spring-20-5a14bc18fb2f44ba90a61ba86b6fc426).
3. Document your work in this `README.md` file.

## Submitting
Follow the instructions at on the Technical Challenge page for submission.

## Installing Additional Packages
Use any tools you think are relevant to the challenge! To install additional packages 
run `pipenv install <package_name>` within the directory. Make sure to document your additions.

from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import json

"""
References https://towardsdatascience.com/how-to-web-scrape-with-python-in-4-minutes-bc49186a8460
"""

class ClubClass:
    """
    Stores the information for a single club
    Fields:
        - Name
        - Tags
        - Description
    """

    def __init__(self):
        self.name = ''
        self.tags = []
        self.desc = ''
        self.favcount = 0

    def toJson(self):
        return json.dumps(self.__dict__)

    def writeName(self, name):
        self.name = name

    def addTagSoup(self, tags):
        for t in tags:
            self.tags.append(t.text)

    def addTagStrings(self, tags):
        for t in tags:
            self.tags.append(t)

    def clearTags(self):
        self.tags = []

    def writeDesc(self, desc):
        self.desc = desc

def get_html(url):
    """
    Retrieve the HTML from the website at `url`.
    """

    # Adapted from provided medium article
    response_html = requests.get(url).text

    return response_html

def get_clubs_html():
    """
    Get the HTML of online clubs with Penn.
    """
    url = 'https://ocwp.apps.pennlabs.org'
    return get_html(url)

def soupify(html):
    """
    Load HTML into BeautifulSoup so we can extract data more easily

    Note that for the rest of these functions, whenever we refer to a "soup", we're refering
    to an HTML document or snippet which has been parsed and loaded into BeautifulSoup so that
    we can query what's inside of it with BeautifulSoup.
    """
    return BeautifulSoup(html, "html.parser") 


def get_elements_with_class(soup, elt, cls):
    """
    Returns a list of elements of type "elt" with the class attribute "cls" in the
    HTML contained in the soup argument.

    For example, get_elements_with_class(soup, 'a', 'navbar') will return all links
    with the class "navbar". 

    Important to know that each element in the list is itself a soup which can be
    queried with the BeautifulSoup API. It's turtles all the way down!
    """ 
    return soup.findAll(elt, {'class': cls})

def get_clubs(soup):
    """
    This function should return a list of soups which each correspond to the html
    for a single club.
    """
    
    club_list = get_elements_with_class(soup, 'div', 'box')

    return club_list

def get_club_name(club):
    """
    Returns the string of the name of a club, when given a soup containing the data for a single club.

    We've implemented this method for you to demonstrate how to use the functions provided.
    """
    elts = get_elements_with_class(club, 'strong', 'club-name')
    if len(elts) < 1:
        return ''
    return elts[0].text

def get_club_description(club):
    """
    Extract club description from a soup of 
    """
    elts = get_elements_with_class(club, 'em', '')
    if len(elts) < 1:
        return ''
    return elts[0].text

def get_club_tags(club):
    """
    Get the tag labels for all tags associated with a single club.
    """
    tag_list = get_elements_with_class(club, 'span', 'tag is-info is-rounded')

    return tag_list

def get_club_object(club):
    """
    Creates the club object from the club soup
    Returns the object with modified fields (object definition at top)
    """

    tempObj = ClubClass()
    tempObj.writeName(get_club_name(club))
    tempObj.addTagSoup(get_club_tags(club))
    tempObj.writeDesc(get_club_description(club))

    return tempObj

def club_obj_list(club_arr):
    """
    Takes an array of club soups and turns it into
    native objects
    """

    obj_arr = []
    for club in club_arr:
        obj_arr.append(get_club_object(club))

    return obj_arr

def club_arr_to_file(club_arr):
    """
    Take the list of club objects and throw em into a big ol JSON array
    Writes aforementioned JSON array to ./clubs.json
    """

    json_arr = []
    for club in club_arr:
        json_arr.append(club.toJson())

    with open('clubs.json', 'w') as outfile:
        json.dump(json_arr, outfile)

def get_club_json_list(club_arr):
    """
    Take a list of club objs and returns a json list
    """

    json_arr = []
    for club in club_arr:
        json_arr.append(club.toJson())

    return json.dumps(json_arr)
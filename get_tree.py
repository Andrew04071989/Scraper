"""
This module is responsible for retrieving the element tree (DOM)
"""
import time
import requests
from lxml import html


class Tree(object):
    """
    This class opens a GET and POST request sessions
    and returns and returns the element trees (DOM).
    """
    def __init__(self):
        self.session = requests.Session()

    def tree_method_get(self, url):
        """
        This method opens a GET request session
        and returns an element tree (DOM).
        """
        get = self.session.get(url).text
        time.sleep(2)
        return html.fromstring(get)

    def tree_method_post(self, url, data):
        """
        This method opens a POST request session
        and returns an element tree (DOM).
        """
        post = self.session.post(url, data).text
        time.sleep(2)
        return html.fromstring(post)

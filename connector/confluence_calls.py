# Methods for searching Confluence

import requests
import base64
from docutils.parsers.rst.roles import role

from connector.htmltableparser import HTMLTableParser
from bs4 import BeautifulSoup


class ConfluenceSearch:
    payload = {}
    headers = {
        'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
    }

    def __init__(self):
        self.parser = HTMLTableParser()

    def get_role(self, role):
        """
        Get people with matching role from the table
        :param role: the role to search for
        :return: data info with matching person information to the role
        """
        array = []
        data = []
        payload = {}
        headers = {
            'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
        }
        url = "https://ccwi.atlassian.net/wiki/rest/api/content/47939585?expand=body.storage"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        html = json_response['body']['storage']['value']
        parser = HTMLTableParser()
        parser.feed(html)
        data.append(parser.tables[0][0])
        for i in parser.tables[0]:
            if i[0].lower() == role.lower():
                data.append(i)
        return data

    def get_roles(self):
        """
        Method used to return the available roles for the search
        :return: array with available roles
        """
        array = []
        payload = {}
        headers = {
            'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
        }
        url = "https://ccwi.atlassian.net/wiki/rest/api/content/47939585?expand=body.storage"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        html = json_response['body']['storage']['value']
        parser = HTMLTableParser()
        parser.feed(html)
        for i in parser.tables[0]:
            if i[0] != "Rolle":
                array.append(i[0].lower())
            # Remove duplicates
            array = list(dict.fromkeys(array))
        return array

    def confluence_search(self, search_term):
        """
        Search with search search_term in the confuence search
        :param search_term:
        :return: results: list with search results
        """
        results = []
        url = "https://ccwi.atlassian.net/wiki/rest/api/content/search?cql=text~" + search_term
        payload = {}
        headers = {
            'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        for i in json_response['results']:
            results.append(i)
        return results

    def get_confluence_site_content(self, site_id):
        """
        Returns the content of given Confluence Site
        :param site_id: the id of the confluence site
        :return: type of found content and content itself
        """
        payload = {}
        headers = {
            'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
        }
        url = "https://ccwi.atlassian.net/wiki/rest/api/content/" + site_id + "?expand=body.storage"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        html = json_response['body']['storage']['value']
        if "table" in html:
            print("Tabelle gefunden")
            rows = []
            tableparser = HTMLTableParser()
            tableparser.feed(html)
            for i in tableparser.tables:
                rows.append(i)
            return "table", rows
        elif "image" in html:
            # TODO: Decide what to do with pictures
            print("image gefunden")
            return "picture", "picture data"
        else:
            parsed_html = BeautifulSoup(html)
            # TODO: Text schöner formatieren also absätze beachten
            return "text", parsed_html.get_text()

    def generic_search(self, search_term):
        """
        Use the search function in Confluence and search for the search_term
        :param search_term:
        :return: typ of found content and content itself
        """
        # TODO: Suche Stefan und filter unbrauchbare info raus
        try:
            results = self.confluence_search(search_term)
            typ, content = self.get_confluence_site_content(results[0]['id'])
            return typ, content
        except Exception as error:
            print("Search term is None " + repr(error))

    def get_person(self, name):
        """
            Return Information for Person
        """
        payload = {}
        headers = {
            'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
        }
        url = "https://ccwi.atlassian.net/wiki/rest/api/group/confluence-users/member"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        for x in json_response["results"]:
            if x["publicName"].lower() == name:
                return x
        return None

    def get_profile_picture(self, path):
        """
            Return Profile picture for Person
        """
        payload = {}
        headers = {
            'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
        }
        url = "https://ccwi.atlassian.net" + path
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response)
        encodepic = base64.b64encode(response.content)
        print(encodepic)
        return encodepic

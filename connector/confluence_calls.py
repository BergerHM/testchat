# Methods for searching Confluence

import requests
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

    def get_sites(self):
        url = "https://ccwi.atlassian.net/wiki/rest/api/content"
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        json_response = response.json()
        chat_response = ""
        for item in json_response["results"]:
            chat_response += item["title"] + "\n"
        print(chat_response)
        return chat_response

    def get_azubis_from_labs(self):
        url = "https://ccwi.atlassian.net/wiki/rest/api/content/47972513?expand=body.storage"
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        print(response.text.encode('utf8'))

    def get_role(self, role):
        """
        Get people with matching role from the table
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
            if i[0] == role:
                data.append(i)
        return data

    def get_roles(self):
        """
            Method used to return the available roles for the search
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
                array.append(i[0])
            # Remove duplicates
            array = list(dict.fromkeys(array))
        return array

    def confluence_search(self, search_term):
        """
        Search with search begriff in the confuence search

        :return results: list with search results
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

    def get_confluence_site_content(self,site_id):
        """
            Returns the content of given Confluence Site
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
            return "picture"
        else:
            parsed_html = BeautifulSoup(html)
            # TODO: Text schöner formatieren also absätze beachten
            return "text", parsed_html.get_text()

    def generic_search(self, search_term):
        results = self.confluence_search(search_term)
        typ, content = self.get_confluence_site_content(results[0]['id'])
        return typ, content


    def get_person(self, name):
        return None

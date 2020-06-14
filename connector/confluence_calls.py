# Methods for searching Confluence

import requests

from connector.htmltableparser import HTMLTableParser


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

    def get_rolle(self, role):

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
        self.parser.reset()
        self.parser.feed(html)
        for i in self.parser.tables[0]:
            if i[0] == role:
                data.append(i)
        return data

    def get_rolles(self):

        array = []
        payload = {}
        headers = {
            'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
        }
        url = "https://ccwi.atlassian.net/wiki/rest/api/content/47939585?expand=body.storage"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        html = json_response['body']['storage']['value']
        self.parser.reset()
        self.parser.feed(html)
        for i in self.parser.tables[0]:
            if i[0] != "Rolle":
                array.append(i[0])
            # Remove duplicates
            array = list(dict.fromkeys(array))
        return array

    def text_search(self, search):
        results = []
        url = "https://ccwi.atlassian.net/wiki/rest/api/content/search?cql=text~Coach"
        payload = {}
        headers = {
            'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        for i in json_response['results']:
            results.append(i)
        return results

search = ConfluenceSearch()
search.text_search("Coach")

# Methods for searching Confluence
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree


class confluence_search:
    payload = {}
    headers = {
        'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
    }

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

    def get_rolle(self, rolle):
        payload = {}
        headers = {
            'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
        }
        url = "https://ccwi.atlassian.net/wiki/rest/api/content/47939585?expand=body.storage"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        html = json_response['body']['storage']['value']
        parsed_html = BeautifulSoup(html, 'html.parser')
        print(parsed_html.find("table"))
        return "test"

    def test(self):
        s = """<table>
          <tr><th>Event</th><th>Start Date</th><th>End Date</th></tr>
          <tr><td>a</td><td>b</td><td>c</td></tr>
          <tr><td>d</td><td>e</td><td>f</td></tr>
          <tr><td>g</td><td>h</td><td>i</td></tr>
        </table>
        """
        table = etree.HTML(s).find("body/table")
        rows = iter(table)
        headers = [col.text for col in next(rows)]
        for row in rows:
            values = [col.text for col in row]
            print(dict(zip(headers, values)))


search = confluence_search()
search.get_rolle("rolle")

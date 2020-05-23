# Methods for searching Confluence
import json
import requests

class confluence_search:
    payload = {}
    headers = {
        'Authorization': 'Basic bHVrYXMuYWx0ZW5zdHJhc3NlckBobS5lZHU6YjBWbGpSc3pxRUFQWE1qQnlmMEdCMEQ4'
    }

    def get_sites(self):
        url = "https://ccwi.atlassian.net/wiki/rest/api/content"
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        chat_response = ""
        for item in json_response["results"]:
            chat_response += item["title"] + "\n"
        print(chat_response)
        return chat_response


    def get_azubis_from_labs(self):
        url = "https://ccwi.atlassian.net/wiki/rest/api/content/47972513?expand=body.storage"
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text.encode('utf8'))


    def get_rolle(rolle):
        return "test"

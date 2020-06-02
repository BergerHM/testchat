# Methods for searching Confluence
from html.parser import HTMLParser
import requests


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

    def get_rolle(self, role):

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

        for i in range(0, 7):
            if (parser.tables[0][i][0] == role):
                for j in range(0, 3):
                    array.append(parser.tables[0][i][j])
        return array


class HTMLTableParser(HTMLParser):
    """ This class serves as a html table parser. It is able to parse multiple
    tables which you feed in. You can access the result per .tables field.
    """

    def __init__(
            self,
            decode_html_entities=False,
            data_separator=' ',
    ):

        HTMLParser.__init__(self)

        self._parse_html_entities = decode_html_entities
        self._data_separator = data_separator

        self._in_td = False
        self._in_th = False
        self._current_table = []
        self._current_row = []
        self._current_cell = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        """ We need to remember the opening point for the content of interest.
        The other tags (<table>, <tr>) are only handled at the closing point.
        """
        if tag == 'td':
            self._in_td = True
        if tag == 'th':
            self._in_th = True

    def handle_data(self, data):
        """ This is where we save content to a cell """
        if self._in_td or self._in_th:
            self._current_cell.append(data.strip())

    def handle_charref(self, name):
        """ Handle HTML encoded characters """

        if self._parse_html_entities:
            self.handle_data(self.unescape('&#{};'.format(name)))

    def handle_endtag(self, tag):
        """ Here we exit the tags. If the closing tag is </tr>, we know that we
        can save our currently parsed cells to the current table as a row and
        prepare for a new row. If the closing tag is </table>, we save the
        current table and prepare for a new one.
        """
        if tag == 'td':
            self._in_td = False
        elif tag == 'th':
            self._in_th = False

        if tag in ['td', 'th']:
            final_cell = self._data_separator.join(self._current_cell).strip()
            self._current_row.append(final_cell)
            self._current_cell = []
        elif tag == 'tr':
            self._current_table.append(self._current_row)
            self._current_row = []
        elif tag == 'table':
            self.tables.append(self._current_table)
            self._current_table = []

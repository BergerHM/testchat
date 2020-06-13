import json


class CardBuilder():
    def build_adaptive_role_card(self, information):
        with open('cards/AdaptiveCardTemplate.json') as json_file:
            data = json.load(json_file)
        print(information)
        print(data['body'][1]['items'][1])
        data['body'][1]['items'].append(self.create_column_set())
        return data

    def set_url(self, card, url):
        """
            Method adds a URL to any Action.OpenUrl field

            @param card: the card where the url needs to be set
            @param url: the url to set in the card
            @return: the given card with the url set
        """
        # TODO: find url tag and change it
        return card

    def create_column_set(self):
        columnitem = [{
            'type': "TextBlock",
            'text': "HIER TEXT",
            'wrap': 'true'
        }]
        column = {
            'type': "Column",
            'width': "stretch",
            'items': columnitem
        }
        columns = []
        columns.append(column)
        columns.append(column)
        columns.append(column)
        columnset = {
            'type': "ColumnSet",
            'columns': columns
        }
        return columnset

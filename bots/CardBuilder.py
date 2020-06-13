import json


class CardBuilder():
    def build_adaptive_role_card(self, information):
        with open('cards/AdaptiveCardTemplate.json') as json_file:
            data = json.load(json_file)
        for x in information:
            data['body'][0]['items'].append(self.create_column_set(x[0], x[1], x[2]))
        # data['body'][1]['items'].append(self.create_column_set())
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

    def create_column_set(self, column1, column2, column3):
        column1 = {
            'type': "Column",
            'width': "stretch",
            'items': [{
                'type': "TextBlock",
                'text': column1,
                'wrap': 'true'
            }]
        }
        column2 = {
            'type': "Column",
            'width': "stretch",
            'items': [{
                'type': "TextBlock",
                'text': column2,
                'wrap': 'true'
            }]
        }
        column3 = {
            'type': "Column",
            'width': "stretch",
            'items': [{
                'type': "TextBlock",
                'text': column3,
                'wrap': 'true'
            }]
        }
        columns = []
        columns.append(column1)
        columns.append(column2)
        columns.append(column3)
        columnset = {
            'type': "ColumnSet",
            'columns': columns
        }
        return columnset

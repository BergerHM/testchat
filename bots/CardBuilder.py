import json


class CardBuilder():
    def build_adaptive_role_card(self, information):
        with open('cards/AdaptiveCardTemplate.json') as json_file:
            data = json.load(json_file)
        for x in information:
            # TODO: use columns depending on columns in information
            # If it is the first entry in the table print it bold
            if len(data['body'][0]['items']) == 0:
                data['body'][0]['items'].append(self.create_column_set(x[0], x[1], x[2], True))
            else:
                data['body'][0]['items'].append(self.create_column_set(x[0], x[1], x[2]))
        # data['body'][1]['items'].append(self.create_column_set())
        return data

    def build_generic_card(self, info):
        # TODO: Try to build a generic card for confluence pages
        return None

    def set_url(self, card, url):
        """
            Method adds a URL to any Action.OpenUrl field

            @param card: the card where the url needs to be set
            @param url: the url to set in the card
            @return: the given card with the url set
        """
        # TODO: find url tag and change it
        return card

    def create_column_set(self, column1, column2, column3, bold=False):
        """
        With this method you can create a columns set for AdaptiveCards

        :param column1: value of first column
        :param column2: value of second column
        :param column3: value of third column
        :param bold: if True the line will be bold
        :return: column set to add in a card
        """
        weight = "default"
        if bold:
            weight = "bolder"
        column1 = {
            'type': "Column",
            'width': "stretch",
            'items': [{
                'type': "TextBlock",
                'text': column1,
                'weight': weight,
                'wrap': 'true'
            }]
        }
        column2 = {
            'type': "Column",
            'width': "stretch",
            'items': [{
                'type': "TextBlock",
                'text': column2,
                'weight': weight,
                'wrap': 'true'
            }]
        }
        column3 = {
            'type': "Column",
            'width': "stretch",
            'items': [{
                'type': "TextBlock",
                'text': column3,
                'weight': weight,
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

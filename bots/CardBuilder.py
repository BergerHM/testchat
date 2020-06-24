import json


class CardBuilder():
    def build_table_card(self, information):
        with open('cards/AdaptiveCardTemplate.json') as json_file:
            data = json.load(json_file)
        for x in information:
            # If it is the first entry in the table print it bold
            if len(data['body'][0]['items']) == 0:
                data['body'][0]['items'].append(self.create_column_set(x, True))
            else:
                data['body'][0]['items'].append(self.create_column_set(x))
        # data['body'][1]['items'].append(self.create_column_set())
        return data

    def build_generic_card(self, typ, data):
        # TODO: Try to build a generic card for confluence pages
        #jsondata = '{"$schema": "http://adaptivecards.io/schemas/adaptive-card.json","type": "AdaptiveCard","version": "1.0","body": [{"type": "Container","items": [{"type": "TextBlock","text": "Hier könnte Ihre Information stehen.","weight": "bolder","size": "medium"},{"type": "TextBlock","text": "Diese Karte ist noch in Arbeit","wrap": true}]}]}'
        #data = json.loads(jsondata)
        if typ == "table":
            return self.build_table_card(data[0])
        elif typ == "picture":
            return self.build_picture_card(data)
        elif typ == "text":
            return self.build_text_card(data)
        else:
            raise ValueError("Data Typ could not be regonized")

    def build_text_card(self, data):
        with open('cards/TextCardTemplate.json') as json_file:
            card = json.load(json_file)
            card['body'][1]['items'][0]['text'] = data
        return card

    def build_picture_card(self, data):
        return None

    def build_person_card(self):
        # TODO: Hier werden Informationen über einen Kontakt wieder gegeben
        jsondata = '{"$schema": "http://adaptivecards.io/schemas/adaptive-card.json","type": "AdaptiveCard","version": "1.0","body": [{"type": "Container","items": [{"type": "TextBlock","text": "Hier könnte Ihre Information stehen.","weight": "bolder","size": "medium"},{"type": "TextBlock","text": "Diese Karte ist noch in Arbeit","wrap": true}]}]}'
        data = json.loads(jsondata)
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

    def create_column_set(self, data, bold=False):
        """
        With this method you can create a columns set for AdaptiveCards

        :param column1: value of first column
        :param column2: value of second column
        :param column3: value of third column
        :param bold: if True the line will be bold
        :return: column set to add in a card
        """
        columns = []
        for x in data:
            columns.append(self.create_column(x, bold))
        columnset = {
            'type': "ColumnSet",
            'columns': columns
        }
        return columnset

    def create_column(self, text, bold=False):
        """
        Create column for AdaptiveCard

        :param text: value of  column
        :param bold: if True the line will be bold
        :return: column in json format
        """
        weight = "default"
        if bold:
            weight = "bolder"
        column = {
            'type': "Column",
            'width': "stretch",
            'items': [{
                'type': "TextBlock",
                'text': text,
                'weight': weight,
                'wrap': 'true'
            }]
        }
        return column

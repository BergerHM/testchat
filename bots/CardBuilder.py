import json

from connector import ConfluenceSearch


class CardBuilder():
    def build_table_card(self, information):
        """
        Build a adaptive card that contains a table
        :param information: for the table as dict
        :return: data that contains the card as json string
        """
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
        """
        Determine the content from the generic search and build a card for it
        :param typ: content type
        :param data: the content itself
        :return: card as json string
        """
        if typ == "table":
            return self.build_table_card(data[0])
        elif typ == "picture":
            return self.build_picture_card(data)
        elif typ == "text":
            return self.build_text_card(data)
        else:
            raise ValueError("Data Typ could not be regonized")

    def build_text_card(self, data):
        """
        Build AdaptiveCard that contains text
        :param data: the text for the card
        :return: card that contains the adaptive card as json string
        """
        with open('cards/TextCardTemplate.json') as json_file:
            card = json.load(json_file)
            card['body'][1]['items'][0]['text'] = data
        return card

    def build_picture_card(self, data):
        return None

    def build_person_card(self, info):
        """
        Build adaptive card for person information
        :param info: person information
        :return: data that contains adaptive card  as json string
        """
        # TODO: Hier werden Informationen über einen Kontakt wieder gegeben
        jsondata = '{"$schema":"http://adaptivecards.io/schemas/adaptive-card.json","type":"AdaptiveCard","version":"1.0","body":[{"type":"Container","items":[{"type":"TextBlock","text":"Max Musterman","weight":"bolder","wrap":true},{"type":"FactSet","facts":[{"title":"E-Mail:","value":"lukas.altenstrasser@hm.edu"},{"title":"Profil:","value":"profilurl"}]}]}]}'
        data = json.loads(jsondata)
        #picture = ConfluenceSearch().get_profile_picture(info["profilePicture"]["path"])
        data["body"][0]["items"][1]["facts"][0]["value"] = info["email"]
        data["body"][0]["items"][1]["facts"][1]["value"] = "https://ccwi.atlassian.net/wiki/people/" + info["accountId"]
        data["body"][0]["items"][0]["text"] = info["publicName"]
        return data

    def create_column_set(self, data, bold=False):
        """
        With this method you can create a columns set for AdaptiveCards
        :param data: data for the columns
        :param bold: if True the line will be bold
        :return: columnset to add in a card
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

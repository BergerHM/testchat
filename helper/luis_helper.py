from enum import Enum
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import TurnContext


class Intent(Enum):
    CONFUSED = "None"
    SEARCH_ROLE = "SearchRole"
    SEARCH_PERSON = "SearchPerson"
    HELP = "Utilities.Help"
    NONE_INTENT = "NoneIntent"
    WHO = "WhoIs"
    HOW = "HOWRU"
    USERANSWER_Y = "USER_ANSWER_Positive"
    USERANSWER_N = "USER_ANSWER_Negative"
    SEARCH_TEXT = "SearchText"


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
            luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        entity = None
        intent = None

        recognizer_result = await luis_recognizer.recognize(turn_context)

        intent = (
            sorted(
                recognizer_result.intents,
                key=recognizer_result.intents.get,
                reverse=True,
            )[:1][0]
            if recognizer_result.intents
            else None
        )

        # We need to get the result from the LUIS JSON which at every level returns an array.

        entity = recognizer_result.entities.get("$instance", {}).get(
            "expert", []
        )

        if len(entity) > 0:
            entity = entity[0]["text"].capitalize()

        return intent, entity

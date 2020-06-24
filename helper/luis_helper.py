import json
from enum import Enum
from typing import Dict

from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import TurnContext, IntentScore, TopIntent


class Intent(Enum):
    CONFUSED = "None"
    SEARCH_ROLE = "SearchRole"
    SEARCH_PERSON = "SearchPerson"
    HELP = "Utilities_Help"
    NONE_INTENT = "NoneIntent"
    WHO = "WhoIs"
    HOW = "HOWRU"
    USERANSWER_Y = "USER_ANSWER_Positive"
    USERANSWER_N = "USER_ANSWER_Negative"
    SEARCH_TEXT = "SearchText"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


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

        if intent == Intent.SEARCH_ROLE.value:
            entity = recognizer_result.entities.get("$instance", {}).get(
                "role", []
            )

        elif intent == Intent.SEARCH_PERSON.value:
            entity = recognizer_result.entities.get("$instance", {}).get(
                "name", []
            )

        if entity and len(entity) > 0:
            entity = entity[0]["text"].lower()

        return intent, entity

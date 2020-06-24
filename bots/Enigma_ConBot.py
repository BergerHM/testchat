# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Test
import random

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, ConversationState, UserState
from botbuilder.schema import ChannelAccount, Attachment

from bots.CardBuilder import CardBuilder
from connector import ConfluenceSearch
from data_models import Conversation
from helper.luis_helper import LuisHelper, Intent
from recognizer import luis_recognizer_enigma


class Enigma_ConBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState,
                 luis_recognizer2: luis_recognizer_enigma.LuisRecognizerEnigma):

        if conversation_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. user_state is required but None was given"
            )

        self._luis_recognizer = luis_recognizer2
        self.conversation_state = conversation_state
        self.user_state = user_state
        self.cardbuilder = CardBuilder()
        self.flow_accessor = self.conversation_state.create_property("ConversationFlow")
        self.profile_accessor = self.user_state.create_property("UserProfile")

    async def on_members_added_activity(
            self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hi and welcome. My Name is Enigma. I am pleased to meet you.")
                await turn_context.send_activity(
                    "I'll help you find information in confluence, just type what you are searching for.")

    async def on_message_activity(self, turn_context: TurnContext):

        # Get the state properties from the turn context.
        # info = await self.profile_accessor.get(turn_context, SearchInfo)
        flow = await self.flow_accessor.get(turn_context, Conversation)

        await self._fill_out_information(flow, turn_context)

        # Save changes to UserState and ConversationState
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def _fill_out_information(
            self, flow: Conversation, turn_context: TurnContext
    ):

        user_text = turn_context.activity.text.strip()

        intent, search_info = await LuisHelper.execute_luis_query(
            self._luis_recognizer, turn_context
        )
        # Luis Debug
        ########################################
        recognizer_result = await self._luis_recognizer.recognize(turn_context)

        await turn_context.send_activity(
            MessageFactory.text(f"Intent: {intent}")
        )
        await turn_context.send_activity(
            MessageFactory.text(f"Entity: {search_info}")
        )

        await turn_context.send_activity(
            MessageFactory.text(f"Luis had this to say: {recognizer_result}")
        )
        # Luis Debug
        ########################################

        # Spezifische Rollensuche
        if intent == Intent.SEARCH_ROLE.value:

            information = ConfluenceSearch().get_roles()
            await turn_context.send_activity(
                MessageFactory.text(information)
            )

            if search_info != "" and search_info in information:
                information = ConfluenceSearch().get_role(search_info)
                response = self.cardbuilder.build_adaptive_role_card(information)
                attachment = Attachment(content_type='application/vnd.microsoft.card.adaptive', content=response)
                await turn_context.send_activity(
                    MessageFactory.attachment(attachment)
                )
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Enjoy!")
                )
            else:

                response = "It seems you're searching for a specific role.\n\nHere are the current roles:  "
                for x in information:
                    response += "\n\n - " + x
                await turn_context.send_activity(
                    MessageFactory.text(f"{response}")
                )

        # Personensuche
        # TODO: Methoden einfügen um Inhalt aus Confluence für PErsonensuche zu erhalten
        elif intent == Intent.SEARCH_PERSON.value:

            await turn_context.send_activity(
                MessageFactory.text(
                    "I'll look up the account of " + search_info)
            )

        # Show help message
        elif intent == Intent.HELP.value:
            await turn_context.send_activity(
                MessageFactory.text("At some point there will be text here explaining what i can do")
            )

        elif intent == Intent.WHO.value:
            await turn_context.send_activity(
                MessageFactory.text(
                    "Actually my Daddies are: Lukas Altenstrasser, Adiran Berger, Justin Bitterlich and Michaela "
                    "Saenger")
            )

        elif intent == Intent.HOW.value:
            list1 = ("Same old, same old.", "I’m alive!", "Quite well, old chap, quite well indeed!",
                     "Are we pretending i have moods?", "Never been better, let us get to work.")
            result = random.choice(list1)
            await turn_context.send_activity(
                MessageFactory.text(result)

            )

        elif intent == Intent.USERANSWER_Y.value:
            await turn_context.send_activity(
                MessageFactory.text(
                    "That's perfect. So do you have a question for me?")
            )

        elif intent == Intent.USERANSWER_N.value:
            await turn_context.send_activity(
                MessageFactory.text(
                    "Oh I am very sorry, I hope you will get well soon! Please don't hesitate to ask me something.")
            )



        # Default Suche für allgm. Confluence-Suche (+wenn nur ein Wort eingegeben wird welches er nicht kennt)
        # TODO: Default Suche muss mit Confluence funktionieren
        else:

            await turn_context.send_activity(
                MessageFactory.text(
                    "I'll look up " + user_text + " in confluence for you.")
            )
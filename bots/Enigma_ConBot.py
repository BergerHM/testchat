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

        # Returns the Intent and Entity recognized by Luis
        intent, search_info = await LuisHelper.execute_luis_query(
            self._luis_recognizer, turn_context
        )

        recognizer_result = await self._luis_recognizer.recognize(turn_context)
        # Luis Score for the Intent
        scoring = recognizer_result.get_top_scoring_intent().score

        # Score threshold a prediction needs to be reliable
        score_threshold = 0.5

        # Luis Debug
        ########################################
        '''await turn_context.send_activity(
            MessageFactory.text(f"Intent: {intent}")
        )
        await turn_context.send_activity(
            MessageFactory.text(f"Entity: {search_info}")
        )
        await turn_context.send_activity(
            MessageFactory.text(f"why: {recognizer_result}")
        )'''

        # Luis Debug
        ########################################

        # Spezifische Rollensuche
        if intent == Intent.SEARCH_ROLE.value and scoring > score_threshold:

            information = ConfluenceSearch().get_roles()

            if search_info != "" and search_info in information:
                # Get role information from Confluence API
                information = ConfluenceSearch().get_role(search_info)
                # Create AdaptiveCard out of Confluence Information
                response = self.cardbuilder.build_table_card(information)
                attachment = Attachment(content_type='application/vnd.microsoft.card.adaptive', content=response)
                await turn_context.send_activity(
                    MessageFactory.attachment(attachment)
                )
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Enjoy!")
                )
            else:

                response = "It seems you're searching for a specific role.\n\nHere are all the current roles:  "
                for x in information:
                    response += "\n\n - " + x
                await turn_context.send_activity(
                    MessageFactory.text(f"{response}")
                )

        # Personensuche
        elif intent == Intent.SEARCH_PERSON.value and scoring > score_threshold:
            await turn_context.send_activity(
                MessageFactory.text(
                    "I'll look up the account of " + search_info)
            )
            information = ConfluenceSearch().get_person(search_info)
            if not information is None:
                person_card = self.cardbuilder.build_person_card(information)
                attachment = Attachment(content_type='application/vnd.microsoft.card.adaptive', content=person_card)
                await turn_context.send_activity(
                    MessageFactory.attachment(attachment)
                )
            else:
                await turn_context.send_activity(
                    MessageFactory.text("Could not find any Person with the name " + search_info)
                )



        # Show help message
        elif intent == Intent.HELP.value and scoring > score_threshold:
            await turn_context.send_activity(
                MessageFactory.text("Hi, im trying to help you find info in confluence.\n\n\n\n"
                                    "Textsearch:\n\n Just type what you are searching for: \"java\", \"ostern\", ..."
                                    "\n\nYou can also ask me in a sentence: \"Can you search for hausbauer\"?"

                                    "\n\nPersonsearch:\n\n To find the account of someone you can use one of the "
                                    "following exampels or sentences with a similar structure: "
                                    "\"Can you look up Michael Huber\"?, \"Find the account of Bina Schulz\""

                                    "\n\nRolesearch:\n\n To find a person with a specific Job you can use one of the "
                                    "following examples or sentences with a similar structure: "
                                    "\"Who is responsible for innovationen\"?, \"Show me everyone working as scrum "
                                    "master.\"")

            )
        elif intent == Intent.WHO.value and scoring > score_threshold:
            await turn_context.send_activity(
                MessageFactory.text(
                    "Actually my Daddies are: Lukas Altenstrasser, Adiran Berger, Justin Bitterlich and Michaela "
                    "Saenger")
            )

        elif intent == Intent.HOW.value and scoring > score_threshold:
            list1 = ("Same old, same old.", "I’m alive!", "Quite well, old chap, quite well indeed!",
                     "Are we pretending i have moods?", "Never been better, let us get to work.",
                     "I'm fine thanks, and you?")
            result = random.choice(list1)
            await turn_context.send_activity(
                MessageFactory.text(result)

            )

        elif intent == Intent.USERANSWER_Y.value and scoring > score_threshold:
            await turn_context.send_activity(
                MessageFactory.text(
                    "That's perfect. So do you have a question for me?")
            )

        elif intent == Intent.USERANSWER_N.value and scoring > score_threshold:
            await turn_context.send_activity(
                MessageFactory.text(
                    "Oh I am very sorry, I hope you will get well soon! Please don't hesitate to ask me something.")
            )

        elif intent == Intent.BYE.value and scoring > score_threshold:
            await turn_context.send_activity(
                MessageFactory.text(
                    "You are Welcome. Have a nice Day, Bye bye.")
            )

        elif intent == Intent.GREET.value and scoring > score_threshold:
            list2 = ("Hi, nice to meet you!", "Hello, it is nice meeting you! Please ask me something.",
                     "Servus, it is nice meeting you")
            result = random.choice(list2)
            await turn_context.send_activity(
                MessageFactory.text(result)
            )

        # Default Suche für allgm. Confluence-Suche (+wenn nur ein Wort eingegeben wird welches er nicht kennt)
        elif intent == Intent.SEARCH_TEXT.value and scoring > score_threshold and search_info != "":
            await turn_context.send_activity(
                MessageFactory.text(
                    "I'll look up \"" + search_info + "\" in confluence for you.")
            )
            try:
                typ, response = ConfluenceSearch().generic_search(search_info)
                result = self.cardbuilder.build_generic_card(typ, response)
                attachment = Attachment(content_type='application/vnd.microsoft.card.adaptive', content=result)
                await turn_context.send_activity(
                    MessageFactory.attachment(attachment)
                )
            except Exception as exception:
                await turn_context.send_activity(
                    MessageFactory.text(
                        "I can't find what you are searching for in confluence.")
                )
        else:

            await turn_context.send_activity(
                MessageFactory.text(
                    "I'll look up \"" + user_text + "\" in confluence for you.")
            )
            try:
                typ, response = ConfluenceSearch().generic_search(user_text)
                result = self.cardbuilder.build_generic_card(typ, response)
                attachment = Attachment(content_type='application/vnd.microsoft.card.adaptive', content=result)
                await turn_context.send_activity(
                    MessageFactory.attachment(attachment)
                )
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Enjoy!")
                )
            except Exception as exception:
                await turn_context.send_activity(
                    MessageFactory.text(
                        "I can't find what you are searching for in confluence.")
                )

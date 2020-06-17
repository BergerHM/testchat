# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Test
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, ConversationState, UserState, MemoryStorage
from botbuilder.schema import ChannelAccount, Attachment
from helper.luis_helper import LuisHelper
from recognizer import luis_recognizer_enigma
from bots.CardBuilder import CardBuilder
from connector import ConfluenceSearch
from data_models import SearchInfo, Question, Conversation


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
                await turn_context.send_activity("Hi! Welcome my Name is Enigma. Please tell me what you search for?")

    async def on_message_activity(self, turn_context: TurnContext):

        # Get the state properties from the turn context.
        info = await self.profile_accessor.get(turn_context, SearchInfo)
        flow = await self.flow_accessor.get(turn_context, Conversation)

        await self._fill_out_information(flow, info, turn_context)

        # Save changes to UserState and ConversationState
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def _fill_out_information(
            self, flow: Conversation, info: SearchInfo, turn_context: TurnContext
    ):

        user_input = turn_context.activity.text.strip()

        # Hier muss der erste eingegebene Text an Luis gesendet werden
        # MIt der Antwort von Luis müssen die Variablen Story und search_info befüllt werden

        recognizer_result = await self._luis_recognizer.recognize(turn_context)
        story, search_info = await LuisHelper.execute_luis_query(
            self._luis_recognizer, turn_context
        )

        await turn_context.send_activity(
            MessageFactory.text(f"Intent: {story}")
        )
        await turn_context.send_activity(
            MessageFactory.text(f"Entity: {search_info}")
        )
        await turn_context.send_activity(
            MessageFactory.text(f"Luis had this to say: {recognizer_result}")
        )

        if flow.last_question_asked == Question.NONE:
            if story == "experte" and search_info == "":
                await turn_context.send_activity(
                    MessageFactory.text("What Expert do you want to search?")
                )
            if search_info != "":
                info.rolle = search_info
            flow.last_question_asked = Question.EXPERT

        elif flow.last_question_asked == Question.EXPERT:

            information = ConfluenceSearch().get_rolles()
            # print(information)

            if info.rolle in information:
                await turn_context.send_activity(
                    MessageFactory.text(f"So you search for this Experts '{info.rolle}' information?")
                )
                flow.last_question_asked = Question.ACCEPT
            else:
                # Alle vorhandenen Rollen ausgeben
                # await turn_context.send_activity(
                #     MessageFactory.text("Specify your search please. I find this experts roles:")
                # )
                response = "Specify your search please.\n\nI found this roles you can search for:  "
                for x in information:
                    response += "\n\n - " + x
                await turn_context.send_activity(
                    MessageFactory.text(f"{response}")
                )
                flow.last_question_asked = Question.EXPERT

        elif flow.last_question_asked == Question.ACCEPT:

            story, search_info = await LuisHelper.execute_luis_query(
                self._luis_recognizer, turn_context
            )

            if story == "bestaetigung":
                information = ConfluenceSearch().get_rolle(info.rolle)
                response = self.cardbuilder.build_adaptive_role_card(information)
                attachment = Attachment(content_type='application/vnd.microsoft.card.adaptive', content=response)
                await turn_context.send_activity(
                    MessageFactory.attachment(attachment)
                )
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Are you happy with this information?")
                )
                flow.last_question_asked = Question.HAPPY
            else:
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Your input equals with nothing in the list. Please try again. What Expert do you want to search?")
                )
                flow.last_question_asked = Question.EXPERT

        elif flow.last_question_asked == Question.HAPPY:
            if story == "bestaetigung":
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Perfect. It was nice to meet you. Have a nice day!")
                )

            else:
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Please don't hesitate to ask again.")
                )
            flow.last_question_asked = Question.NONE

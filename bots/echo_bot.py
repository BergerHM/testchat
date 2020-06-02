# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, ConversationState, UserState
from botbuilder.schema import ChannelAccount
from connector import ConfluenceSearch
from data_models import SearchInfo, Question, Conversation


class EchoBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        if conversation_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. user_state is required but None was given"
            )

        self.conversation_state = conversation_state
        self.user_state = user_state

        self.flow_accessor = self.conversation_state.create_property("ConversationFlow")
        self.profile_accessor = self.user_state.create_property("UserProfile")

    async def on_members_added_activity(
            self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Welcome to search in Confluence!")

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

        # ask for name
        if flow.last_question_asked == Question.NONE:
            if user_input == "Hi":
                await turn_context.send_activity(
                    MessageFactory.text("Hi.")
                )
            await turn_context.send_activity(
                MessageFactory.text("Let's get started. But first, what is your name?")
            )
            flow.last_question_asked = Question.NAME


        elif flow.last_question_asked == Question.NAME:

            info.name = user_input

            await turn_context.send_activity(
                MessageFactory.text(f"Hello {info.name}")
            )
            await turn_context.send_activity(
                MessageFactory.text("Which Role do you want to search?")
            )
            flow.last_question_asked = Question.ROLLE


        elif flow.last_question_asked == Question.ROLLE:

            info.rolle = user_input

            await turn_context.send_activity(
                MessageFactory.text(f"You will search for the Role {info.rolle}.")
            )
            await turn_context.send_activity(
                MessageFactory.text("I wait for information from Confluence")
            )
            search = ConfluenceSearch()
            information = search.get_rolle(f"{info.rolle}")
            print(information)
            for x in information:
                await turn_context.send_activity(
                    MessageFactory.text(f"{x}")
                )

            flow.last_question_asked = Question.NONE

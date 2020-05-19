# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import json

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

import test_luis_recognizer


class EchoBot(ActivityHandler):

    def __init__(
            self, luis_recognizer: test_luis_recognizer.TestLuisRecognizer
    ):

        self._luis_recognizer = luis_recognizer

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):

        await turn_context.send_activity(
            MessageFactory.text(f"Echo: {turn_context.activity.text}")
        )

        if not self._luis_recognizer.is_configured:
            await turn_context.send_activity(
                MessageFactory.text(f"Echo: Luis not configured!")
            )

        recognizer_result = await self._luis_recognizer.recognize(turn_context)
        await turn_context.send_activity(
            MessageFactory.text(f"Luis had this to say: {recognizer_result}")
         )


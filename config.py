#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = "d7e37f51-7f27-47ef-802b-5519f76f383f"
    APP_PASSWORD = "AtLeastSixteenCharacters_0"
    LUIS_APP_ID = os.environ.get("36901912-db40-4303-8dac-58b3bcc43390", "")
    LUIS_API_KEY = os.environ.get("23d11aa114794c4fa1fcab35a09b9e97", "")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("westus.api.cognitive.microsoft.com", "")
    LUIS_ENDPOINT_KEY = os.environ.get("westus.api.cognitive.microsoft.com", "")
    #https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/25f67858-9fec-49f7-baca-060732aadda0?subscription-key=ffeea86052d243349a06c5be013b82ca


#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = "abc596b2-7f1a-49d2-89fd-8ab41ef8d068"
    APP_PASSWORD = "_cj1G-E0AxkCJVV?OMpUGdyYnKn-nR47"
    LUIS_APP_ID = os.environ.get("36901912-db40-4303-8dac-58b3bcc43390", "")
    LUIS_API_KEY = os.environ.get("d108bb0f1d774d519db79d4d6753bb98", "")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("westus.api.cognitive.microsoft.com", "")
    LUIS_ENDPOINT_KEY = os.environ.get("westus.api.cognitive.microsoft.com", "")



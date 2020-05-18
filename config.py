#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = "6044e27c-bd2f-442f-9b98-f05a0ec3f406"
    APP_PASSWORD = "7?3s0@Ex/?dsN3hN@0IeAmI3oC42xbQR"
    LUIS_APP_ID = os.environ.get("f32b05b9-013f-4efd-b963-28513e3e3a2c", "")
    LUIS_API_KEY = os.environ.get("87902cb7cc9440debacce84750946d69", "")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("westus.api.cognitive.microsoft.com", "")
    LUIS_ENDPOINT_KEY = os.environ.get("westus.api.cognitive.microsoft.com", "")
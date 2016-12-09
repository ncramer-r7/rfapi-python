# Copyright 2016 Recorded Future, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Auth provider for RF tokens stored in environment."""
import os
import requests

# pylint: disable=too-few-public-methods
class RFTokenAuth(requests.auth.AuthBase):
    """Authenticate using a token stored in an environment variable.

    The class will look for tokens in RF-TOKEN and RECFUT_TOKEN (legacy).
    """
    def __init__(self, token):
        self.token = self._find_token() if token == 'auto' else token

    def __call__(self, r):
        # If we still haven't a token we need to bail.
        if not self.token:
            raise MissingTokenError
        r.headers['Authorization'] = "RF-TOKEN token=%s" % self.token
        return r

    @staticmethod
    def _find_token():
        if 'RECFUT_TOKEN' in os.environ:
            return os.environ['RECFUT_TOKEN']
        if 'RF_TOKEN' in os.environ:
            return os.environ['RF_TOKEN']
        return None


class MissingTokenError(Exception):
    """No token was supplied."""

    def __str__(self):
        """Format the error message."""
        return 'no Recorded Future API key was provided.'

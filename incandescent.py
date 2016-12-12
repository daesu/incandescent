from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object

import base64
from hashlib import sha1
import hmac
import requests
import time
import urllib.request
import urllib.parse
import urllib.error

ADD_ENDPOINT = "https://incandescent.xyz/api/add/"
GET_ENDPOINT = "https://incandescent.xyz/api/get/"

# How long to wait before re-requesting API for result
WAIT_TIME = 10
VERIFY_CERT = True


class Client(object):

    def __init__(self, uid, apikey):

        self.uid = uid
        self.apikey = apikey
        self.data = {}

    def addImageUrl(self, imageUrl):

        self.imageUrl = imageUrl
        self.data['images'] = self.imageUrl

    def makeRequestData(self):

        # Set expiry time (unixtime now + value)
        expiresSeconds = int(time.time())
        expiresSeconds = expiresSeconds + 1000  # max is 1200

        stringToSign = str(self.uid) + "\n" + str(expiresSeconds)

        hashed = hmac.new(self.apikey.encode(), stringToSign.encode(), sha1)

        # The signature
        encoded = base64.b64encode(hashed.digest())
        signature = urllib.parse.quote_plus(encoded)

        self.data['uid'] = self.uid
        self.data['expires'] = expiresSeconds
        self.data['signature'] = signature

        print(self.data)

    def makeRequest(self):

        try:
            r = requests.post(ADD_ENDPOINT, json=self.data, verify=VERIFY_CERT)

            if r.status_code == 200:
                response = r.json()

                if 'project_id' in response:
                    project_id = response['project_id']
                    self.data['project_id'] = project_id

                    self.project_id = project_id
                    self.data['images'] = None  # Remove from request

                elif 'error' in response:
                    self.project_id = None
                    print(response['error'])

        except Exception as err:  # TODO handle errors
            self.project_id = None
            print (err)

    def getResults(self):

        try:
            self.data['project_id'] = self.project_id

            r = requests.post(GET_ENDPOINT, json=self.data, verify=VERIFY_CERT)
            response = r.json()

            if 'status' not in response:
                # Should have result
                print(response)

            elif response['status'] == 710:
                print("Waiting ... ", WAIT_TIME, " Seconds")
                time.sleep(WAIT_TIME)
                self.getResults()  # Retry

            elif response['status'] == 755:
                print("No Results for image")

        except Exception as err:
            print(err)
            self.project_id = None

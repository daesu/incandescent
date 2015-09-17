#!/usr/bin/python
from hashlib import sha1
import urllib
import hmac
import json
import time
import requests

ADD_ENDPOINT = "https://incandescent.xyz/api/add/"
GET_ENDPOINT = "https://incandescent.xyz/api/get/"

# How long to wait before re-requesting API for result
WAIT_TIME = 10

class Client:

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
			expiresSeconds = expiresSeconds + 1000 # max is 1200

			stringToSign = str(self.uid) + "\n" + str(expiresSeconds);

			hashed = hmac.new(self.apikey, stringToSign, sha1)

			# The signature
			signature = urllib.quote_plus(hashed.digest().encode("base64").rstrip('\n'))

			self.data['uid'] = self.uid;
			self.data['expires'] = expiresSeconds;
			self.data['signature'] = signature;

			print self.data

	def makeRequest(self):

			try:
				r = requests.post(ADD_ENDPOINT, json=self.data)

				if r.status_code == 200:
					response = json.loads(r.content)

					if 'project_id' in response:
						project_id = response['project_id']

						self.project_id = project_id
						self.data['images'] = None # Remove from request

					elif 'error' in response:
						self.project_id = None 
						print response['error']

			except StandardError, err: # TODO handle errors
					self.project_id = None 

	def getResults(self):

			try:
				self.data['project_id'] = self.project_id;

				r = requests.post(GET_ENDPOINT, json=self.data)

				response = json.loads(r.content)

				if 'status' not in response:
					# Should have result
					print response
					
				elif response['status'] == 710:
					print "Waiting ... ", WAIT_TIME, " Seconds"
					time.sleep(WAIT_TIME) 
					self.getResults() #Retry  

				elif response['status'] == 755:
					print "No Results for image"

			except StandardError, err:
				print err
				self.project_id = None 			
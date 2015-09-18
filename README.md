# incandescent python client
A simple python client for the [Incadescent](http://incandescent.xyz/) reverse image search API.

## Installation
pip install -r requirements.txt 

## Usage
See `example.py`

				# Add credentials
			  search = Client(uid, apikey)

			  # Add an image URL
			  search.addImageUrl(<image_url>)

			  # Generate the request and POST
			  search.makeRequestData()
			  search.makeRequest()

			  # Request the result 
			  search.getResults()
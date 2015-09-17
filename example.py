from incandescent import Client

def main():
        # Config
        uid = "YOUR_UID"
        apikey = "YOUR_APIKEY"

        search = Client(uid, apikey)
        search.addImageUrl("https://upload.wikimedia.org/wikipedia/commons/2/2b/Jupiter_and_its_shrunken_Great_Red_Spot.jpg")
        search.makeRequestData()
        search.makeRequest()

        if 'project_id' in search.data:
        	search.getResults()
      	else:
      		print "No Project ID"

if __name__ == "__main__":
        main()
import os, time, json, sys
from datetime import datetime
import random
from atproto import Client
import requests 


def load_settings():
    # gets application settings from json file
    local = "path/to/settings/file.json"
    with open(local, "r") as f:
        settings = json.load(f)

    return settings


class Unsplash_Link:
    def __init__(self, keyword, settings):

        #class variables for Unsplash API query 
        self.settings = settings
        key = self.settings["usplash_key"]
        self.data = None
        self.name = str(random.randint(0,1000))+".jpg"
        self.location = None
        self.tags = []
        self.keyword = keyword
        self.blacklist = self.settings["blacklist"]
        self.hashtags_str = ""
        self.hashtags_list = []
        self.facets = []
        self.param_dict={
            "client_id": key,
            "query": keyword
        }

    #Getters and setters for class variables
    def get_hashtag_str(self):
        return self.hashtags_str
    
    def get_hashtags_list(self):
        return self.hashtags_list

    def set_hashtags_str(self, value):
        self.hashtags_str = value

    def set_hashtags_list(self, value):
        self.hashtags_list = value

    def get_param_dict(self):
        return self.param_dict

    def get_data(self):
        return self.data

    def set_data(self, value):
        self.data = value

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_location(self):
        return self.location

    def set_location(self, value):
        self.location = value

    def set_tags(self, value):
        self.tags = value

    def get_tags(self):
        return self.tags
    
    def get_blacklist(self):
        return self.blacklist
    
    def set_facets(self, value):
        self.facets = value
    
    def get_facets(self):
        return self.facets

    def query(self):
        #queries Unsplash API for image data, sets class variables for image name and location on drive
        r = requests.get("https://api.unsplash.com/photos/random", params=self.get_param_dict())
        if r.status_code == 200:
            
            print("Running Unsplash query - Status Code 200 for query.")
            self.set_data(r.json())
            self.set_tags(self.get_data().get("tags", []))
            self.set_location(self.settings["image_location"] + self.get_name())
            print(f"Image name set to '{self.get_name()}' and location set to '{self.get_location()}'")
            #print(r.json())

        else:
            print(f"Status code '{r.status_code}' for query")
            with open("failed.txt", "a") as f:
                f.write(self.keyword + "\n")

            sys.exit("image query failed! Exiting...." + self.keyword)
            
    def _hashtags(self, terms):
        
        t_list=[]
        t_str=""
        for tag in terms: #interates over tags and posts to local list
            t_list.append(tag['title'])


        t_list.sort(key=lambda x: len(x)) #sorts list by size
        self.set_hashtags_list(t_list) 
        
        for tag in t_list: #Iterates over local sorted list and creates string
            t_str += f"#{tag} "
        
        tags = t_str.strip()
            #makes class variable
        self.set_hashtags_str(tags) #strips white space from string

        Facet_list = []

        for h in t_list:
            tag_text = f"#{h}"
            bytestart = t_str.encode('utf-8').find(tag_text.encode('utf-8'))
            byteend = bytestart+len(tag_text.encode('utf-8'))

            facet_dict = {
                "index":{
                    "byteStart": bytestart,
                    "byteEnd": byteend
                },
                "features": [
                    {
                        "$type": "app.bsky.richtext.facet#tag",
                        "tag": h
                    }
                ]
            }
            
            Facet_list.append(facet_dict)
        
        if not Facet_list:
            print("We have no facets!")
            return []
        else:
            print("Facets cut!")
            return self.set_facets(Facet_list)

    def keyword_check(self):
        #runs hashtag facets & checks for banned/blacklisted words in keywords in an effort to reduce unwanted images
        
        self._hashtags(self.get_tags()) #creates richtext data for hashtag use
        tags_list = self.get_hashtags_list() #string of hashtags for post text content
        
        file1 = self.get_blacklist()
        list1 = []
        flag = False

        with open(file1, "r") as f:
            for line in f:
                list1.append(line.strip())

        for l in list1:
            if l in tags_list:
                print(l + " is in blacklist, canceling picture post")
                flag = True
        
        return flag
    

    def dwnld(self):
        #downloads image from Unsplash API using data from query, checks for successful download and returns image name and location on drive
        #run after query function to ensure class variables are set

        if self.get_data()["urls"]["regular"] != None:
            r = requests.get(self.get_data()["urls"]["regular"])
            if r.status_code == 200:
                with open(self.get_location(), "wb") as f:
                    f.write(r.content)
                print(f"image downloaded successfully to '{self.get_location()}' !")
                return r.status_code
            else: 
                print ("Image download failed! Exiting.....")
                return r.status_code
        else:    
            with open("failed.txt", "a") as f:
                f.write(self.keyword + "\n")
            return r.status_code

            sys.exit("image download failed! Exiting...." + self.keyword)

    def keyword_cycle(self):
        flag = True
        code = None
        i = 0

        while flag and i < 3: #will keep attempting to post unless main returns false or 3 attempts
            code, flag = self.main()
            i += 1
            print("Cycling: " + str(i) + " with flag: " + str(flag))


    def main(self):
        
        self.query()    
        flag = self.keyword_check()

        if flag == False:

            resp = self.dwnld()
            return resp, flag
        
        return None, flag
        

class Followers: #bsky_test

    def __init__ (self, settings):
        #sets class variables and creates client session for ATPROTO
        self.settings = settings #settings
        usr = self.settings["bsky_usr"]
        passw = self.settings["bsky_pass"]
        
        self.follows = set() #for the follow back functions
        self.followers = set()
        self.client = Client() #client session object
        self.client.login(usr, passw)
        self.user_did = self.client.me.did
    
    def get_client(self):
        return self.client

    def get_follows(self):
        return self.follows

    def set_follows(self, value):
        self.follows = value

    def get_followers(self):
        return self.followers

    def set_followers(self, value):
        self.followers = value

       
    def post_img(self, img_path, facets = [], text_c=""):
        #posts img and richtext facets to profile. 
        with open(img_path, 'rb') as f:
            img_data = f.read()

        img_post = self.client.send_image(text=text_c, image=img_data, image_alt="A picture of a magnificient plant or flower.", facets=facets)
        print(f"URI {img_post.uri} & CID {img_post.cid}")


    def get_all_follows(self, usr:str):
        #retrieves the follows of the specified user and adds them to the class variable self.follows
        
        cursor = None
        follows = self.get_follows()
        client = self.get_client()

        while True:
            response = client.app.bsky.graph.get_follows(params={'actor': usr, 'cursor': cursor})
            for follow in response.follows:
                follows.add(follow.did)

            if not response.cursor:
                break
            cursor = response.cursor

        self.set_follows(follows)
    

    def get_all_followers(self, usr:str):
        #retreives the followers of the specified user and adds them to the class variable self.followers
        cursor = None
        client = self.get_client()
        followers = self.get_followers()    
        while True:
            # Use client.get_followers for the user's followers
            response = client.app.bsky.graph.get_followers(params={'actor': usr, 'cursor': cursor})
            for follower in response.followers:
                followers.add(follower.did)
            if not response.cursor:
                break
            cursor = response.cursor
        self.set_followers(followers)

    
    def follow_back(self):
        
        client = self.get_client()
        user_did = client.me.did
        print("Beginning follow back sequence.....")
        
        self.get_all_follows(user_did)
        self.get_all_followers(user_did)
        my_followers = self.get_followers()
        my_follows = self.get_follows()

        to_follow_back = my_followers - my_follows

        if not to_follow_back:
            print("No new followers to follow back.")
            return

        print(f"Found {len(to_follow_back)} new followers to follow back!")

        for did in to_follow_back:
            try:
                # The client.follow method handles the app.bsky.graph.follow createRecord procedure
                client.follow(did)
                print(f"Followed back DID: {did}")
                time.sleep(1) # Add a small delay to avoid hitting rate limits
            except Exception as e:
                print(f"Error following {did}: {e}")    

    def get_thread(self):
        
        threads = self.client.app.bsky.feed.get_author_feed(params={"actor":self.user_did, "limit": 1})
        print(threads)

    def main(self):

        self.get_thread()


class main:

    def __init__(self, settings):
        self.dt =  str(datetime.now())
        self.settings = settings
        self.blacklist_use = self.settings["blacklist_use"]
        
    def get_authors(self, data):
        #gets author name, url and returns. 
        photographer = data.get('user', {})
        name = photographer.get('name')
        username = photographer.get('username')
        portfolio_url = photographer.get('links', {}).get('html')

        print(f"Photographer: {name} (@{username})")
        print(f"Portfolio: {portfolio_url}")
        return name, username, portfolio_url

    def remove_photo(self, location):
        try:
            os.remove(location)
            print(f"File '{location}' deleted successfully.")
        except OSError as e:
            print(f"Error deleting file '{location}': {e}")

    def posting(self, location, facets, tags, name, p_url, settings):
        bsky = Followers(settings)
        bsky.post_img(location, facets, tags + "\n\nPhoto by " + name + " on Unsplash\n" + p_url)
        print("Image successfully posted!")
        bsky.follow_back()

        self.remove_photo(location)

    def main_blacklist(self, search_term = "flower"):
        spacer = "-------------"
        print(spacer+self.dt+spacer)
        
        #unsplash data retrieval and image download

        unsplash = Unsplash_Link(search_term, self.settings)
        code, keyword_flag = unsplash.main() # returns response code and keyword check flag. 
        
        name = unsplash.get_name() #Identifier of posted img
        location = unsplash.get_location() #location on drive of img
        facets = unsplash.get_facets()
        tags = unsplash.get_hashtag_str()

        name, username, portfolio_url = self.get_authors(unsplash.get_data()) #prints photographer info to console
        

        if code == 200 and keyword_flag == False: #checks if request was successful.
            self.posting(location, facets, tags, name, portfolio_url, self.settings)
            return keyword_flag
        else:
            print("Posting failed!")
            self.remove_photo(location)
            return keyword_flag

    def main_(self, search_term):
        spacer = "-------------"
        print(spacer+self.dt+spacer)

        unsplash = Unsplash_Link(search_term, self.settings)
        unsplash._hashtags(self.get_tags()) #creates richtext data for hashtag use
        tags_list = unsplash.get_hashtags_list() #string of hashtags for post text content

        unsplash.query()
        resp = unsplash.dwnld()

        name = unsplash.get_name() #Identifier of posted img
        location = unsplash.get_location() #location on drive of img
        facets = unsplash.get_facets()
        tags = unsplash.get_hashtag_str()

        name, username, portfolio_url = self.get_authors(unsplash.get_data()) #prints photographer info to console

        if resp == 200: #checks if request was successful.
            self.posting(location, facets, tags, name, portfolio_url, self.settings)
            
        else:
            print("Posting failed!")
            self.remove_photo(location)

    
    def main0(self, search_term):

        flag = True
        i = 0

        while flag and i < 3: #will keep attempting to post unless main returns false or 3 attempts
            flag = self.main_blacklist(search_term)
            i += 1
            print("Cycling: " + str(i) + " with flag: " + str(flag))

    def main1(self, search_term):
        
        if self.blacklist_use == "True":
            self.main0(search_term)
        else:
            pass

        if self.blacklist_use == "False":
            self.main_(search_term)
        else:
            pass
        


def compare(list1, list2):
    #function to compare two lists and return a list of items that are in list1 but not in list2
    #return [item for item in list1 if item not in list2]

    return list(set(list1) - set(list2))

def compare_lists(search_list, fail_list):
    list1 = []
    list2 = []
    file1= search_list
    file2 = fail_list
    
    with open(file1, "r") as f:
        for line in f:
            list1.append(line.strip())

    with open(file2, "r") as f2:
        
        for line in f2:
            list2.append(line.strip())

        diff = compare(list1, list2)
    
    return diff

def execute(settings):
    """
    Determine between using a search list or mono term. Reflects on using error list
    """
    if settings['searchlist_use'] == "True":
        
        if settings["searchterm_err_use"] == "True":
            list1 = compare_lists(settings["searchlist"], settings["searchterm_err"])
            term = random.choice(list1) #chooses random term
            Q = main(settings)
            Q.main1(term) 
            print(f"Selected search term: {term}")
        
        if settings["searchterm_err_use"] == "False":
            list1 = [] #list to capture all list items
            with open(settings["searchlist"], "r") as f:
                for line in f:
                    list1.append(line.strip())

            term = random.choice(list1) #chooses random term
            Q = main(settings)
            Q.main1(term) 
            print(f"Selected search term: {term}")     
    
    elif settings['searchlist_use'] == "False":
        term = settings["static_term"]
        Q = main(settings)
        Q.main1(term) 
        print(f"Static search term: {term}")  
    else:
        print("Unable to comply due to settings. Please review settings document for complete options.")

if __name__ == "__main__":
    settings = load_settings()
    execute(settings)
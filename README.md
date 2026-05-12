# <b>FlowersBSKY</b>
Script that posts random images from unsplash.com with various options to tailor your posting experience. 

## Features
- Basic function: Searches Unsplash.com using the random api endpoint and returns an image that is then posted to your BSKY account. 
- Hashtag Blacklist to filter images with multiple attempts to get acceptable content
- Follow back feature when someone follows your BSKY profile
- Search Term List: A document populated with terms of the users choice that is used to pull an image from UNSPLASH API
- Search Term Error List: A list of terms that have caused errors in searches (used for massive search term lists)

## Set Up the settings.json

- "image_location": "needs to be path/to/file",  -Where on your hard drive your files will be stored.
- "usplash_key": "USPLASHKEY",   -UNSPLASH.com developer key
- "bsky_usr": "USRNM.bsky.social", - BSKY user name 
- "bsky_pass": "bskypass", - BSKY password
- "blacklist": "needs to be path/to/file", -Blacklist for hashtags from UNSPLASH users
- "blacklist_use": "True", - Do we want to use a blacklist? Can only be "True" or "False"
- "searchlist_use": "True", -Similar to blacklist. Can only be "True" or "False"
- "searchlist": "needs to be path/to/file",  -This is a list of terms used for searches. Terms are randomly chosen by function
- "searchterm_err_use": "True", -Want to use a search term error list? Can only be "True" or "False"
- "searchterm_err": "needs to be path/to/file",   -Path to error term list
- "static_term": "Flower"   -Want to search the same term all the time? Here is where we put it.

## Additional notes.

- path to settings.json needs to be determined before running the script in the load_settings() function.
```python
  def load_settings():
    # gets application settings from json file
    local = "path/to/settings/file.json"
    with open(local, "r") as f:
        settings = json.load(f)

    return settings
```
- This script was meant to be run with a task scheduler or [cronjob](https://www.howtogeek.com/devops/what-is-a-cron-job-and-how-do-you-use-them/) (howtogeek). If you would like to help make it a service or Daemon please let me know.
- Use of searchlist_use needs to be "False" for static_term use.
- You will see preset examples in each list. Feel free to clear them out and follow the formatting example.

## Stack
![Static Badge](https://img.shields.io/badge/Python-purple) ![Static Badge](https://img.shields.io/badge/ATPROTO-orange) ![Static Badge](https://img.shields.io/badge/Requests-blue)



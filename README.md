# <b>FlowersBSKY</b>
Script that posts random images from unsplash.com with various options to tailor your posting experience 

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

- path to settings.json needs to be determined before running the script in the loadsettings() function.
- This script was meant to be run with a task scheduler or chronjob. If you would like to help make it a service or Daemon please let me know.
-  

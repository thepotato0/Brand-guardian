#  Brand guardian
an automatic brand guardian script made in python

## what is brand guarding ?

It's controlling how the brand looks, feels, and sounds everywhere.

## how does this script work ?

  

- The tray icon (icon.png) will appear in your system tray.

  

- The app runs a background thread that continuously monitors Reddit.

  

- When your keywords appear in new comments, you’ll receive a desktop alert.



- Clicking the notification opens the Reddit comment directly in your browser.

## how to run (for testing)
- run `pip install -r requirements.txt` in /src directory
- create an enviroment file according to "./example_env_file.txt" (format should be .env) [how to get reddit api secrets](https://www.geeksforgeeks.org/python/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/)
- run src/main.py, a config.json file with defaults should be created
- change the configs to your liking 
- run the script again
- report issues you come across


## todo (by priority)

 - [x] make source code more readable 
 - [x] fix bugs
 - [x] add sentiment analysis logic
 - [x] add email and sms alerting logic 
 - [ ] add cross-platform clickable dekstop notification
 - [ ] make compiled version for installation
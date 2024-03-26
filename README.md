# apollo-notifications

A simple python script that polls your reddit inbox for new comments/messages
and then sends notifications via Pushover with the urls formatted for Apollo.

When opening these notifications the links will automatically redirect to the
Apollo app.

## install dependencies

````
pip3 -r requirements.txt
````

## setup

1. create a "personal use script" app here: https://old.reddit.com/prefs/apps/

note the client id/secret

2. buy the awesome pushover app for iOS and make an account here: https://pushover.net

3. create an application for apollo on https://pushover.net and give it a cool
Apollo icon

note your pushover account user id and the key for the app you created there

4. edit the code and change the parameters as per comments

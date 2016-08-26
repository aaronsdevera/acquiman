# Usage: python acquiman-botEngage.py aaronsdevera "sup" False


########################
# CONFIGURATION
########################

# Variable intake from command line
import sys

# Import the python-twitter library
## requires installation via "pip install python-twitter"
import twitter

# Import the Twitter API keys from local file 'keys'
keys=[]
f = open('keys')
for each in f:
    if each[-1:] == '\n':
        keys.append(each[:-1])
    else:
        keys.append(each)

# Activate api usage with instrument authenticated by keys
api = twitter.Api(consumer_key=keys[0],consumer_secret=keys[1],access_token_key=keys[2],access_token_secret=keys[3])

########################
# parse arguments
########################

target_handle = ''
form_engagement = ''
safety = 'x'
if len(sys.argv) == 4:
    target_handle = sys.argv[1]
    form_engagement = sys.argv[2]
    safety = sys.argv[3]
    if safety == 'True':
        safety = True
    if safety == 'False':
        safety = False
else:
    print '[+] Too few args'

########################
# ENGAGEMENT
########################

if safety == True:
    print '[-] Message not sent to %s; safety is %s' % (target_handle,safety)
elif safety == False:
    print '[+] Targeting: %s' % target_handle
    print '[+] Message: %s' % form_engagement
    api.PostDirectMessage(form_engagement,screen_name=target_handle)
    print '[+] Message sent to %s.' % target_handle
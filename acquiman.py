######################################################################
# ACQUIMAN.PY
#
# aggressive customer acquisition model via twitter
# by Aaron DeVera
# @aaronsdevera
#
# The intent of this program is to:
#    A) Identify users tweeting about a subject
#    B) Direct message targeted users about the subject,
#       with the goal of promoting a related product.
#
# The message sent to the users is dynamic in content,
# in order to establish allusion of human operation to
# the targeted user.
#
# Messages witll me stored in your default direct message box.
# After initial contact with a targeted user, it is up to
# engagement teams to follow up with the user.
#
# Usage:
# acquiman.py -u "<username>" -c "<city>" -s "<subject>" -x
# -x : engages safety, will not message targeted user
# eg. $ python acquiman.py -u "aaronsdevera" -c "San Francisco" -s "burritos"
######################################################################


########################
# CONFIGURATION
########################

# Variable intake from command line
import sys, getopt

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
# ACQUISTION FUNCTION
########################

# Acquisition function
## intakes 'subject_prepped' variable, passed through command line and prepared above
## returns user meta data and content
def acqurieRaw(subject_prepped):
    # Clarify pool size
    # by grabbing 2 elements and choosing the first, we ensure at least 1 target
    pool = 2

    # Grab the search results for the passed subject variable
    results = api.GetSearch(raw_query='q='+subject_prepped+'%20&result_type=recent&count='+str(pool))
    # 1 target selected from 2
    results = results[0]

    # Establish tweet data + contextual info
    user_handle = results.user.screen_name
    tweet_content = results.text
    tweet_location = results.location
    user_location = api.GetUser(screen_name='EatDrinkSF').location

    return user_handle,tweet_content,tweet_location,user_location

###########################
# COMMANDLINE MAIN FUNCTION
###########################
def main(argv):
    # make these variables available for definition by command line args
    self_user = ''
    city = ''
    subject = ''
    safety = False

    try:
        opts, args = getopt.getopt(argv,'hxu:c:s:',['username=','city=','subject='])
    except getopt.GetoptError:
        print 'acquiman.py -u "<username>" -c "<city>" -s "<subject>" -x'
        print '-x : engages safety, will not message targeted user' 
        sys.exit(2)
    for opt, arg in opts:
        # help arg
        if opt == '-h':
            print '[+] acquiman.py -u "<username>" -c "<city>" -s "<subject>" -x '
            sys.exit()
        # username arg
        elif opt in ('-u', '--username'):
            self_user = arg
        # city arg
        elif opt in ('-c', '--city'):
            city = arg            
        # subject arg
        elif opt in ('-s', '--subject'):
            subject = arg
        # safety arg
        elif opt in ('-x', '--x'):
            safety = True

    # prepare search terms for usage in api call
    query = city + ' ' + subject
    query = query.replace(' ','%20')

    # Print out details of your query and your target
    target_handle,tweet_content,tweet_location,user_location = acqurieRaw(query)
    print '[+] Agent handle: %s' % (self_user)
    print
    print '[+] Targeting subject: %s' % (subject)
    print '[+] Targeting city: %s' % (city)
    print
    print '[+] Target handle: %s' % (target_handle)
    print '[+] Tweet: %s' % (tweet_content)
    print '[+] Tweet location: %s' % (tweet_location)
    print '[+] User location: %s' % (user_location)

    ########################
    # ENGAGEMENT
    ########################

    # this section assumes you are configuring the tool to engage targets on behalf of your organization.
    # in this example, we are Sam from Bring A Towel, a crowdsoucred travel site.

    # agent configuration
    ## who are you?
    agent = 'Sam'
    agency = 'Bring a Towel'

    ## what to send to the targeted user
    form_engagement = 'hey! my name is %s from %s. I saw you tweeting about %s in %s! we\'re compiling a list of places to visit in the city. would you be interested in contributing?' % (agent,agency,subject,city)
    print '[+] Draft message: \n\n%s\n' % (form_engagement)
    
    # Check for safety is on
    if safety != True:
        # Safety is not on, so go ahead and direct message the target
        api.PostDirectMessage(target_handle, form_engagement)
        print '[+] Direct message sent.'
    else:
        # Safety is on, so DO NOT direct message the target
        print '[+] Message not sent; safety is engaged.'


# Body for command line program
if __name__ == '__main__':
    main(sys.argv[1:])


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
# Messages will be stored in your default direct message box.
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


def getCol(col_name):
    import csv
    tmp = []
    with open('acquire-list.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tmp.append(row[col_name])
    return tmp


########################
# ACQUISTION FUNCTION
########################

# Acquisition function
## intakes 'subject_prepped' variable, passed through command line and prepared above
## returns user meta data and content
def acqurieRaw(subject_prepped):

    # Make sure the leads are new
    isNew = False
    count = 0
    pool = 90
    resultsBatch = api.GetSearch(raw_query='q='+subject_prepped+'%20&result_type=recent&count='+str(pool))
    #print len(resultsBatch)
    while isNew == False:
        
        # Clarify pool size
        # by grabbing 2 elements and choosing the first, we ensure at least 1 target
        #pool = count + 2

        # Grab the search results for the passed subject variable
        #results = api.GetSearch(raw_query='q='+subject_prepped+'%20&result_type=recent&count='+str(pool))
        # 1 target selected from pool
        results = resultsBatch[count]
        

        # Establish tweet data + contextual info
        user_handle = results.user.screen_name
        status_id = results.id
        tweet_content = results.text
        tweet_location = results.location
        user_location = api.GetUser(screen_name=user_handle).location
        create_time = results.created_at

        #print getCol('status_id')
        #print status_id
        if str(status_id) in getCol('status_id'):
            # still false
            isNew = False
            count += 1
        else:
            isNew = True
            return create_time,user_handle,status_id,tweet_location,user_location
            #return create_time,user_handle,status_id,tweet_content,tweet_location,user_location

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
    create_time,target_handle,status_id,tweet_location,user_location = acqurieRaw(query)
    #create_time,target_handle,status_id,tweet_content,tweet_location,user_location = acqurieRaw(query)
    tweet_url = 'https://twitter.com/%s/status/%s' % (target_handle,status_id)
    
    """
    print '[+] Agent handle: %s' % (self_user)
    print
    print '[+] Created on: %s' % (create_time)
    print '[+] Targeting subject: %s' % (subject)
    print '[+] Targeting city: %s' % (city)
    print
    print '[+] Target handle: %s' % (target_handle)
    print '[+] Status ID: %s' %(status_id)
    print '[+] Tweet: %s' % (tweet_content)
    print '[+] Tweet location: %s' % (tweet_location)
    print '[+] User location: %s' % (user_location)
    print '[+] Tweet url: %s' % (tweet_url)
    """

    # agent configuration
    ## who are you?
    agent = 'Sam'
    agency = 'Bring a Towel'

    ## what to send to the targeted user
    form_engagement = 'Hey! My name is %s from %s. I saw you tweeting about %s in %s! we\'re compiling a list of places to visit in the city. would you be interested in contributing?' % (agent,agency,subject,city)
    
    file_output='%s,%s,%s,"%s"' % (status_id,target_handle,tweet_url,form_engagement)
    #file_output='%s,%s,%s,"%s",%s,%s,%s,%s,%s,"%s"' % (create_time,target_handle,status_id,tweet_content,tweet_location,user_location,tweet_url,agent,agency,form_engagement)
    #print_output='[%s,%s,%s,"%s",%s,%s,%s,%s,%s,"%s"]' % (create_time,target_handle,status_id,tweet_content,tweet_location,user_location,tweet_url,agent,agency,form_engagement)
    
    with open('acquire-list.csv','a+') as f:
        f.write('%s\n' % (file_output))

    return tweet_url

# Body for command line program
if __name__ == '__main__':
    main(sys.argv[1:])


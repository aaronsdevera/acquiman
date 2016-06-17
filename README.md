# acquiman
aggressive customer acquisition model via twitter

![no need for atlantean telepathy for acquiman to see all!](http://static1.comicvine.com/uploads/original/10/100439/2506703-tumblr_lvthmxokc21qko4x4o1_500.gif)

## Usage

    acquiman.py -u "<username>" -c "<city>" -s "<subject>" -x
    -x : engages safety, will not message targeted user
  
  eg. 
    
    $ python acquiman.py -u "aaronsdevera" -c "San Francisco" -s "burritos"
    $ 
        [+] Agent handle: aaronsdevera
        
        [+] Targeting subject: burritos
        [+] Targeting city: San Francisco
        
        [+] Target handle: UnusedPotential
        [+] Tweet: @stillinbeta the best San Francisco style burritos coffee from Denver. #fact
        [+] Tweet location: None
        [+] User location: San Francisco, CA
        [+] Draft message: 
        
        hey! my name is Sam from Bring a Towel. I saw you tweeting about burritos in San Francisco! we're compiling a list of places to visit in the city. would you be interested in contributing?
        
        [+] Message not sent; safety is engaged.
    $
  
  
  
  

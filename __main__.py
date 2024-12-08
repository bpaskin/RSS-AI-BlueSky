from atproto import Client
from datetime import datetime, timedelta
from openai import OpenAI
from requests import get  
from rss_parser import RSSParser

# variables 
OPENAI_API_KEY="OpenAIKey"
BSUSER="Username.bsky.social"
BSPW="tpassword"
FEEDS=["https://rss.politico.com/politics-news.xml", 
       "https://www.washingtontimes.com/rss/headlines/news/politics/", 
       "https://www.cbsnews.com/latest/rss/politics", 
       "https://moxie.foxnews.com/google-publisher/politics.xml",
       "https://slate.com/feeds/news-and-politics.rss", 
       "https://www.ansa.it/sito/notizie/mondo/mondo_rss.xml",
       "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
       "https://www.thenation.com/subject/politics/feed/",
       "https://feeds.npr.org/1014/rss.xml",
       "https://www.realclearpolitics.com/index.xml"
    ]
KEYWORDS=["Trump", "McDonald's"]

def main():
    # create an OpenAI client
    oaclient = OpenAI(api_key=OPENAI_API_KEY)

    # create Blue Sky client 
    bsclient = Client()
    bsclient.login(BSUSER, BSPW)

    # twenty minutes ago
    twenty_minutes_ago = datetime.now(pytz.timezone("UTC")) - timedelta(minutes=20)

    # Go through the RSS feeds one at a time
    for RSS_URL in FEEDS:
        try:
            response = get(RSS_URL)
            rss = RSSParser.parse(response.text)
        except:
            print("Error processing feed from : " + RSS_URL)
            continue

        # loop through rss feed
        for item in rss.channel.items:
            
            # clear out the vars
            title = ""
            description = ""
            combined_string = ""
            link = ""

            # Some pubDates use the timezone and some the offset.  Account for both
            pub_date = parser.parse(item.pub_date.content)

            # check if the post was from more than 20 minutes ago
            if pub_date > twenty_minutes_ago:
                
                # make sure the title and description are not null
                if item.title is not None:
                    title = item.title.content + "." 

                if item.description is not None:
                    description = item.description.content

                combined_string = title + description

                link = item.links[0].content
                
                # Check if the word we are searching for exists in the title or description, if so call ChatGPT
                if any(substring in combined_string for substring in KEYWORDS):
                    completion = oaclient.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "user", "content": "create a black metal or death metal song title based on the following passage: " + combined_string}                        ]
                    )
                    
                    # post the results to Blue Sky
                    post = bsclient.send_post(completion.choices[0].message.content + "\r\n" + link)
if __name__ == "__main__":
    main()

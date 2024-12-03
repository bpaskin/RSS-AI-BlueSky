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
       "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml"
    ]
KEYWORD="pizza"

def main():
    # create an OpenAI client
    oaclient = OpenAI(api_key=OPENAI_API_KEY)

    # create Blue Sky client 
    bsclient = Client()
    bsclient.login(BSUSER, BSPW)

    # twenty minutes ago
    twenty_minutes_ago = datetime.now() - timedelta(minutes=20)

    # Go through the RSS feeds one at a time
    for RSS_URL in FEEDS:
        response = get(RSS_URL)
        rss = RSSParser.parse(response.text)

        # loop through rss feed
        for item in rss.channel.items:
            
            # clear out the vars
            title = ""
            description = ""
            combined_string = ""
            link = ""

            # Some pubDates use the timezone and some the offset.  Account for both
            try:
                pub_date = datetime.strptime(item.pub_date.content, "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError:
                pub_date = datetime.strptime(item.pub_date.content, "%a, %d %b %Y %H:%M:%S %z")
            
            # check if the post was from more than 20 minutes ago
            if pub_date.isoformat() > twenty_minutes_ago.isoformat():
                
                # make sure the title and description are not null
                if item.title is not None:
                    title = item.title.content + "." 

                if item.description is not None:
                    description = item.description.content

                combined_string = title + description

                link = item.links[0].content
                
                # Check if the word we are searching for exists in the title or description, if so call ChatGPT
                if KEYWORD in combined_string:
                    completion = oaclient.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "user", "content": "create a black metal song title based on the following passage:" + combined_string}
                        ]
                    )
                    
                    # post the results to Blue Sky
                    print(completion.choices[0].message.content + "\r\n" + link)
                    post = bsclient.send_post(completion.choices[0].message.content + "\r\n" + link)

if __name__ == "__main__":
    main()
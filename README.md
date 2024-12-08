### RSS AI Bot for Blue Sky

This is a bot that is invoked from a scheduler every 20 minutes and then reads a list of [RSS](https://rss.com/blog/how-do-rss-feeds-work/) feeds and selects the articles that fall within the last 20 minutes.  It then searches those articles for a keyword.  If the keyword is found it sends the title and description of the artcile to [ChatGPT](https://chatgpt.com) to change it into a black metal song title, in this case, and then posts it to [Blue Sky](https://bsky.app).  

---

- The `variables` section in the code needs to be updated with the proper OpenAI key, Blue Sky username and password, and search term.
- Why every 20 miniutes?  Blue Sky has [rate limits](https://docs.bsky.app/blog/rate-limits-pds-v3) and to prevent from hitting the rate limit in a day it is set for 20 minutes.
- Can other LLMs be used?  Yes, I originally tried with [Ollama](https://ollama.com), but I could not find a good model to use.  The code is not too difficult to change the call to another LLM via a REST call.
- Example: [Black Metal Trump](https://bsky.app/profile/blackmetaltrump.bsky.social) - non political changing to black metal song titles.

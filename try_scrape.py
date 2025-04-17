import asyncio
from twikit import Client
from twikit.tweet import Tweet

import asyncio
from twikit import Client

async def main():
    client = Client('fr-FR')
    await client.login(auth_info_1='bitronou', password='BiteMolleDuQ88!') 

    # Optional: Save cookies to avoid re-logging in every time
    client.save_cookies('cookies.json')
    client.load_cookies(path='cookies.json')

    # Example tweet ID
    tweet_id = '327031890622164993'

    # Fetch the tweet (already returns a Tweet object)
    tweet = await client.get_tweet_by_id(tweet_id)

    print("Tweet text:", tweet.text)
    
asyncio.run(main())




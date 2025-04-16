import asyncio
from twikit import Client
from twikit.tweet import Tweet

async def main():
    client = Client('en-US')
    await client.login(auth_info_1='pacoulot', password='KouyOku14')

    # Optional: Save cookies to avoid re-logging in every time
    client.save_cookies('cookies.json')
    client.load_cookies(path='cookies.json')

    # Example tweet ID (replace this with the ID you want to look up)
    tweet_id = '327031890622164993'

    # Fetch the tweet data using the client
    tweet_data = await client.get_tweet_by_id(tweet_id)

    # Now pass that data to the Tweet class
    tweet = Tweet(client=client, data=tweet_data)

    print("Tweet text:", tweet.text)

asyncio.run(main())



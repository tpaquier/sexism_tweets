import asyncio
import pandas as pd
import numpy as np
import random
import os
from twikit import Client
import tqdm

df_ids_whole = pd.read_csv('data_id.csv')
tweet_ids = list(df_ids_whole['id'])

#fetch the tweets
async def fetch_tweets_text_only(tweet_ids):
    client = Client('fr-FR')

    cookies_path = 'tweet_text_cookies_true.json'
    if os.path.exists(cookies_path):
        client.load_cookies(path=cookies_path)
    else:
        await client.login(auth_info_1='username', password='password')
        client.save_cookies(cookies_path)

    results = []

    for tweet_id in tqdm.tqdm(tweet_ids):
        try:
            tweet = await client.get_tweet_by_id(tweet_id)
            results.append({'tweet_id': tweet_id, 'text': tweet.text})
        except Exception as e:
            results.append({'tweet_id': tweet_id, 'text': np.nan})

        await asyncio.sleep(random.uniform(1.0, 2.5))

    return results
#save the results to a csv file
def save_results_to_csv(tweets_data, filename='tweets_text_only.csv'):
    df = pd.DataFrame(tweets_data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    tweets_data = asyncio.run(fetch_tweets_text_only(tweet_ids))
    save_results_to_csv(tweets_data)

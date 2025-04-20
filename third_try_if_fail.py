import asyncio
import pandas as pd
import numpy as np
import random
import os
import time
from twikit import Client
import tqdm

# Load the full list of tweet IDs
df_ids_whole = pd.read_csv('data_id.csv')
tweet_ids = list(df_ids_whole['id'])

# Parameters
BATCH_SIZE = 10000  # Change this if needed
SLOWDOWN_THRESHOLD = 10.0  # Seconds; if average request time exceeds this, pause
SLOWDOWN_CHECK_WINDOW = 10  # Check slowdown every N tweets
SLOWDOWN_PAUSE = 300  # Pause duration in seconds if slowdown is detected
MAX_RETRIES = 5  # For backoff strategy
BASE_WAIT = 2  # Base wait for exponential backoff

# Fetch a batch of tweets
async def fetch_tweets_text_only(batch_ids, batch_num=0):
    client = Client('fr-FR')
    cookies_path = 'tweet_text_cookies_true.json'

    if os.path.exists(cookies_path):
        client.load_cookies(path=cookies_path)
    else:
        await client.login(auth_info_1='ex', password='ex')
        client.save_cookies(cookies_path)

    results = []
    durations = []

    for idx, tweet_id in enumerate(tqdm.tqdm(batch_ids, desc=f"Batch {batch_num+1}")):
        retries = 0
        success = False

        while retries <= MAX_RETRIES:
            start_time = time.time()
            try:
                tweet = await client.get_tweet_by_id(tweet_id)
                duration = time.time() - start_time
                durations.append(duration)
                results.append({'tweet_id': tweet_id, 'text': tweet.text})
                success = True
                break  # Exit retry loop on success
            except Exception as e:
                retries += 1
                wait_time = BASE_WAIT * (2 ** retries) + random.uniform(0, 1)
                print(f"Error fetching tweet {tweet_id}, retry {retries}/{MAX_RETRIES}. Waiting {wait_time:.2f}s.")
                await asyncio.sleep(wait_time)

        if not success:
            results.append({'tweet_id': tweet_id, 'text': np.nan})

        # Add random delay between tweets
        await asyncio.sleep(random.uniform(1.0, 2.5))

        # Check slowdown
        if len(durations) >= SLOWDOWN_CHECK_WINDOW:
            recent_avg = np.mean(durations[-SLOWDOWN_CHECK_WINDOW:])
            if recent_avg > SLOWDOWN_THRESHOLD:
                print(f"Slowdown detected (avg {recent_avg:.2f}s per request). Pausing for {SLOWDOWN_PAUSE}s.")
                await asyncio.sleep(SLOWDOWN_PAUSE)

    return results

def save_results_to_csv(tweets_data, filename):
    df = pd.DataFrame(tweets_data)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} tweets to {filename}")

# Split into batches
def chunkify(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

if __name__ == "__main__":
    all_results = []
    batches = list(chunkify(tweet_ids, BATCH_SIZE))

    for i, batch_ids in enumerate(batches):
        print(f"\nStarting batch {i+1}/{len(batches)} ({len(batch_ids)} tweets)")
        tweets_data = asyncio.run(fetch_tweets_text_only(batch_ids, batch_num=i))
        save_results_to_csv(tweets_data, filename=f'tweets_text_batch_{i+1}.csv')
        all_results.extend(tweets_data)

    # Optionally, combine all batches into one file
    save_results_to_csv(all_results, filename='tweets_text_all.csv')

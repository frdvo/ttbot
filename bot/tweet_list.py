import tweepy
import logging
import time
import sys
import click
from configparser import ConfigParser
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
sys.tracebacklimit = 0

def create_api(key_file):
    file_exists = os.path.exists(key_file)
    if file_exists:
        cfg = ConfigParser()
        cfg.read(key_file)
        consumer_key = cfg.get("credential","CONSUMER_KEY")
        consumer_secret = cfg.get("credential","CONSUMER_SECRET")
        access_token = cfg.get("credential","ACCESS_TOKEN")
        access_token_secret = cfg.get("credential","ACCESS_TOKEN_SECRET")
    else:
        click.echo(f"File {key_file} not found, trying to get credentials from environment variables")
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("Authentication OK - API created")
    return api

def get_list(tweets_list):
    file = open(tweets_list, "r")
    tweets_list_loaded = file.readlines()[:280]
    return tweets_list_loaded

def update_status(tweets_list, api):   
    count = 0
    for tweet_post in tweets_list:
        count +=1
        try:
            print(f"{tweet_post}")
            api.update_status(tweet_post)
            click.echo(f"Tweet {count}/{len(tweets_list)} published\n")
        except Exception as e:
            logger.error("Error posting tweet", exc_info=True)
            click.echo(f"Tweet {count}/{len(tweets_list)} failed\n")


@click.command()
@click.option("--key-file", envvar="TWITTER_KEY_FILE", default="key.ini", help="File name with Twitter keys Default: key.ini")
@click.option("--tweets-list", envvar="TWEETS_LIST", default="tweets.txt", help="File name  with the List of Tweets. Default: tweets.txt")
# @click.option("--proxy", envvar="TWEET_PROXY", default=null", help="HTTPS proxy to connect to Twitter API")
# @click.option("--shuffle-list", envvar="SHUFFLE_LIST", default=True", help="Shuffle Tweet List Order")
# @click.option("--max-random-time", envvar="MAX_RANDOM_TIME", default=9", help="Max random time between tweets")
# click.echo("Tweep Message Test\n")

def main(tweets_list, key_file):
    api = create_api(key_file)
    tweets_list_loaded = get_list(tweets_list)
    update_status(tweets_list_loaded, api)

if __name__ == "__main__":
    main()
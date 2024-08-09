from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv

url = "https://www.funnytweeter.com"
all_tweets = []

def get_tweets(url_page):
    response = requests.get(url_page)
    soup = BeautifulSoup(response.text, 'html.parser')
    tweets = soup.find_all('blockquote')

    i = 0
    for tweet in tweets:
        # get only tweets without pictures 
        media_div = tweet.find('div', class_="media-fe flex-row")
        if not media_div:
            tweet_text = tweet.get_text().strip()
            all_tweets.append(tweet_text)
            # print(tweet_text)

def save_tweets():
    # save array to csv
    pd.DataFrame({"tweets": all_tweets}).to_csv('data/all_tweets.csv', index=False)

# how many pages to scrape
pages = 100
page_prefix = "/page/"

def main():
    # get first page of tweets
    get_tweets(url)
    for i in range(2, pages):
        new_url = url + page_prefix + str(i)
        get_tweets(new_url)
        save_tweets()
        print(i)
main()

df = pd.read_csv("data/all_tweets.csv")

from dotenv import load_dotenv
import os
import praw
import random

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET = os.getenv('SECRET')
USER_AGENT = os.getenv('USER_AGENT')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=SECRET,
                     user_agent=USER_AGENT,
                     username=REDDIT_USERNAME,
                     password=REDDIT_PASSWORD)

with open('subreddit.txt', 'r') as f:
    subreddit_name = f.readline().strip()

if not subreddit_name:
    raise ValueError("Subreddit name is empty. Please check the contents of subreddit.txt.")

subreddit = reddit.subreddit(subreddit_name)

posts = list(subreddit.hot(limit=100))

short_posts = [
    post for post in posts
    if len(post.selftext) > 200
]

if short_posts:
    random_post = random.choice(short_posts)

    title = random_post.title
    text = random_post.selftext

    with open('inputText.txt', 'w') as f:
        f.write(f"{title}\n\n{text}")

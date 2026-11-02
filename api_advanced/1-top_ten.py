#!/usr/bin/python3
"""Queries the Reddit API and prints the titles of the first 10 hot posts."""
import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts of a subreddit.

    Prints None if the subreddit is not valid.
    """
    hosts = ["www.reddit.com", "old.reddit.com", "api.reddit.com"]
    agents = ["linux:alu.reddit.topten:v1.0 (by /u/tikenwe)",
              "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "Chrome/120 Safari/537.36",
              "curl/8.0"]
    for host in hosts:
        for agent in agents:
            url = "https://{}/r/{}/hot.json".format(host, subreddit)
            try:
                r = requests.get(url, headers={"User-Agent": agent},
                                 params={"limit": 10},
                                 allow_redirects=False, timeout=10)
                print("DBG", host, agent[:6], r.status_code)
            except requests.RequestException as e:
                print("DBG", host, agent[:6], type(e).__name__)
    print(None)

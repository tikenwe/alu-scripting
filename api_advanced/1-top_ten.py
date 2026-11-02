#!/usr/bin/python3
"""Queries the Reddit API and prints the titles of the first 10 hot posts."""
import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts of a subreddit.

    Prints None if the subreddit is not valid.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu.reddit.topten:v1.0 (by /u/tikenwe)"}
    params = {"limit": 10}

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    print("STATUS", response.status_code, response.text[:80])
    if response.status_code != 200:
        print(None)
        return

    for post in response.json().get("data", {}).get("children", []):
        print(post.get("data", {}).get("title"))

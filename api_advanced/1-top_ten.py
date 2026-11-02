#!/usr/bin/python3
"""Queries the Reddit API and prints the titles of the first 10 hot posts."""
import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts of a subreddit.

    Prints None if the subreddit is not valid.
    """
    if subreddit is None or not isinstance(subreddit, str):
        print(None)
        return

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                             "AppleWebKit/537.36 Chrome/120 Safari/537.36"}
    hosts = ["www.reddit.com", "old.reddit.com", "api.reddit.com"]

    for host in hosts:
        url = "https://{}/r/{}/hot.json".format(host, subreddit)
        try:
            response = requests.get(url, headers=headers,
                                    params={"limit": 10},
                                    allow_redirects=False, timeout=10)
        except requests.RequestException:
            continue

        if response.status_code == 200:
            try:
                posts = response.json().get("data", {}).get("children", [])
            except ValueError:
                continue
            for post in posts[:10]:
                print(post.get("data", {}).get("title"))
            return
        if response.status_code in (301, 302, 303, 307, 308, 404):
            print(None)
            return
        # 403/429 etc.: blocked, try the next host

    print(None)

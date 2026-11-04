#!/usr/bin/python3
"""Recursively queries the Reddit API for the titles of all hot articles."""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of the titles of all hot articles of a subreddit.

    Calls itself once per page of results, following the pagination token.
    Returns None if the subreddit is not valid or has no results.
    """
    if hot_list is None:
        hot_list = []
    if subreddit is None or not isinstance(subreddit, str):
        return None

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu.reddit.recurse:v1.0 (by /u/tikenwe)"}
    params = {"limit": 100}
    if after:
        params["after"] = after

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False
        )
        if response.status_code != 200:
            return hot_list or None
        data = response.json().get("data", {})
    except (requests.RequestException, ValueError):
        return hot_list or None

    for post in data.get("children", []):
        hot_list.append(post.get("data", {}).get("title"))

    after = data.get("after")
    if after:
        return recurse(subreddit, hot_list, after)
    return hot_list or None

#!/usr/bin/python3
"""Recursively counts keywords in the titles of a subreddit's hot articles."""
import requests


def print_counts(counts, word_list):
    """Print keyword counts, sorted by count (desc) then word (asc)."""
    lowered = [word.lower() for word in word_list]
    totals = {}
    for word, count in counts.items():
        total = count * lowered.count(word)
        if total > 0:
            totals[word] = total
    for word in sorted(totals, key=lambda w: (-totals[w], w)):
        print("{}: {}".format(word, totals[word]))


def count_words(subreddit, word_list, after=None, counts=None):
    """Print a sorted count of keywords found in the hot article titles.

    Calls itself once per page of results, following the pagination token.
    Prints nothing if the subreddit is invalid or no keyword matches.
    """
    if counts is None:
        counts = {}
    if subreddit is None or not isinstance(subreddit, str):
        return

    keywords = set(word.lower() for word in word_list)
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu.reddit.count:v1.0 (by /u/tikenwe)"}
    params = {"limit": 100}
    if after:
        params["after"] = after

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False
        )
        if response.status_code != 200:
            print_counts(counts, word_list)
            return
        data = response.json().get("data", {})
    except (requests.RequestException, ValueError):
        print_counts(counts, word_list)
        return

    for post in data.get("children", []):
        title = post.get("data", {}).get("title") or ""
        for token in title.lower().split():
            if token in keywords:
                counts[token] = counts.get(token, 0) + 1

    after = data.get("after")
    if after:
        return count_words(subreddit, word_list, after, counts)
    print_counts(counts, word_list)

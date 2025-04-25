import requests
from bs4 import BeautifulSoup

class NTScraper:
    def __init__(self, instance="nitter.net"):
        self.instance = instance
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        })

    def search(self, query, mode="search", limit=10):
        base_url = f"https://{self.instance}/{mode}?q={query}&f=tweets"
        tweets = []

        response = self.session.get(base_url)
        soup = BeautifulSoup(response.content, "html.parser")
        tweet_blocks = soup.find_all("div", class_="timeline-item")

        for block in tweet_blocks[:limit]:
            text = block.find("div", class_="tweet-content").text.strip()
            user = block.find("a", class_="username").text.strip().lstrip("@")
            time_tag = block.find("span", class_="tweet-date").find("a")
            time = time_tag.get("title") if time_tag else "Unknown"

            tweets.append({
                "text": text,
                "user": {"username": user},
                "time": time,
            })

        return {"tweets": tweets}

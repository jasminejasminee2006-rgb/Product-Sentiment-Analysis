
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

url = "https://quotes.toscrape.com/"
response = requests.get(url, timeout=15)

soup = BeautifulSoup(response.text, "html.parser")
quotes = soup.select(".quote .text")

print("\nSCRAPED TEXT SENTIMENT ANALYSIS\n")

for number, item in enumerate(quotes, start=1):
    text = item.get_text(strip=True)
    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        sentiment = "Positive"
    elif score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    print(f"{number}. {text}")
    print("Sentiment:", sentiment)
    print("-" * 50)


import requests
from bs4 import BeautifulSoup

# Demo website for learning web scraping
url = "https://quotes.toscrape.com/"

response = requests.get(url, timeout=15)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    reviews = soup.select(".quote .text")

    print("\nWEB SCRAPING RESULTS\n")

    for number, review in enumerate(reviews, start=1):
        print(f"{number}. {review.get_text(strip=True)}")

    print("\nScraping completed successfully!")

else:
    print("Unable to access website:", response.status_code)

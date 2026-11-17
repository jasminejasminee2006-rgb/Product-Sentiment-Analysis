
from flask import Flask, render_template, request, make_response
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
import sqlite3
import csv
from io import StringIO
from pathlib import Path

app = Flask(__name__)

analyzer = SentimentIntensityAnalyzer()
DATABASE = Path(__file__).with_name("reviews.db")


# 1. Create Database
def create_database():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT,
                review TEXT,
                sentiment TEXT
            )
        """)


# 2. Sentiment Analysis
def analyze_sentiment(review):
    score = analyzer.polarity_scores(review)["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


# 3. Web Scraping
def scrape_reviews():
    url = "https://quotes.toscrape.com/"

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    return [
        item.get_text(strip=True)
        for item in soup.select(".quote .text")
    ]


# 4. Main Dashboard
@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    product = ""

    counts = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0
    }

    error = None

    if request.method == "POST":

        product = request.form.get("product", "").strip()

        if product:
            try:
                reviews = scrape_reviews()

                with sqlite3.connect(DATABASE) as conn:

                    for review in reviews:

                        sentiment = analyze_sentiment(review)

                        conn.execute("""
                            INSERT INTO reviews
                            (product, review, sentiment)
                            VALUES (?, ?, ?)
                        """, (product, review, sentiment))

                        results.append({
                            "review": review,
                            "sentiment": sentiment
                        })

                        counts[sentiment] += 1

            except requests.RequestException:
                error = "Unable to collect demo text. Please try again."

    # Total reviews stored in database
    with sqlite3.connect(DATABASE) as conn:
        total_reviews = conn.execute(
            "SELECT COUNT(*) FROM reviews"
        ).fetchone()[0]

    return render_template(
        "index.html",
        results=results,
        product=product,
        counts=counts,
        error=error,
        total_reviews=total_reviews
    )


# 5. Review History with Search and Filter
@app.route("/history")
def history():

    search = request.args.get("search", "").strip()
    sentiment = request.args.get("sentiment", "").strip()

    query = "SELECT * FROM reviews WHERE 1=1"
    params = []

    if search:
        query += " AND product LIKE ?"
        params.append("%" + search + "%")

    if sentiment in ["Positive", "Negative", "Neutral"]:
        query += " AND sentiment = ?"
        params.append(sentiment)

    query += " ORDER BY id DESC"

    with sqlite3.connect(DATABASE) as conn:

        conn.row_factory = sqlite3.Row

        records = conn.execute(
            query, params
        ).fetchall()

    return render_template(
        "history.html",
        records=records,
        search=search,
        selected_sentiment=sentiment
    )


# 6. Download CSV Report
@app.route("/download")
def download():

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Review ID",
        "Product Name",
        "Customer Review",
        "Sentiment"
    ])

    with sqlite3.connect(DATABASE) as conn:

        records = conn.execute("""
            SELECT id, product, review, sentiment
            FROM reviews
            ORDER BY id DESC
        """).fetchall()

    for record in records:
        writer.writerow(record)

    response = make_response(
        "\ufeff" + output.getvalue()
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=review_report.csv"
    )

    response.headers["Content-Type"] = (
        "text/csv; charset=utf-8"
    )

    return response


# 7. Run Application
if __name__ == "__main__":

    create_database()

    app.run(debug=True)

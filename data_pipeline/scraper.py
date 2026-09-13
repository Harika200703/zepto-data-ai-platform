import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
BASE_URL = "https://books.toscrape.com/"
books_data = []

for page in range(1, 4):
    url = BASE_URL if page == 1 else f"{BASE_URL}catalogue/page-{page}.html"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    for book in books:
        title = book.h3.a["title"]
        price_text = book.select_one(".price_color").text.strip()
        price_gbp = float(price_text.replace("£", "").replace("Â", ""))

        books_data.append({
            "title": title,
            "price_gbp": price_gbp,
            "price_inr": round(price_gbp * 105.50, 2),
        })

print("Total books scraped:", len(books_data))

for book in books_data[:5]:
    print(book)
with open("data_pipeline/books.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["title", "price_gbp", "price_inr"]
    )

    writer.writeheader()
    writer.writerows(books_data)

print("Data saved to data_pipeline/books.csv")    
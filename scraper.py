import csv
import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

def get_page(url: str) -> str:
    response = requests.get(url, timeout=10)
    # timeout=10 means give up after 10 seconds
    
    response.raise_for_status()
    # if a site returns an error (404 or 500)
    # instead of continuing with bad data
    # .raise_for_status() stops the program with an error message
    
    return response.text
    # return html page in text format


def parse_books(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    # turn html page into a searhable object
    # html.parser is a built-in reader
    
    books = []
    for item in soup.select('article.product_pod'):
    # find every <article> tag with the class product_pod.
    
        title = item.h3.a['title']
        # inside each book go to <h3> tag then <a> link inside it
        # and read the title attribute
        
        price = item.select_one('p.price_color').text
        # find the first <p> tag with class price_color
        # inside the book and take its text.
        
        books.append({'title': title, 'price': price})
    return books


def save_to_csv(books: list, filename: str) -> None:
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price"])
        # create a writer object that turns dictionaries into csv rows
        # fieldnames = column names.
        
        writer.writeheader()
        # write the heading (only once)
        
        writer.writerows(books)
        # write one row for ever book in the list


def main():
    html = get_page(URL)
    books = parse_books(html)
    for book in books:
        print(f'Price: {book['price']:<7} - Title: {book['title']}')
    save_to_csv(books, 'books.csv')
    print(f'Saved {len(books)} books to books.csv')


if __name__ == "__main__":
    main()
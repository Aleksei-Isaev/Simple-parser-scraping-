from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/allinone")


@dataclass
class Product:
    title: str
    description: str
    price: float
    rating: int
    num_of_reviews: int


def parse_single_product(product_soup: BeautifulSoup) -> Product:
    return Product(
        title=product_soup.select_one(".title")["title"],
        description=product_soup.select_one(".description").text,
        price=float(product_soup.select_one(".price").text.replace("$", "")),
        rating=int(product_soup.select_one("p[data-rating]")["data-rating"]),
        num_of_reviews=int(product_soup.select_one(
            ".ratings > p.pull-right"
        ).text.split()[0])
    )


def get_home_products() -> [Product]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")

    products = soup.select(".thumbnail")

    return [parse_single_product(product_soup) for product_soup in products]


def main():
    print(get_home_products())


if __name__ == '__main__':
    main()

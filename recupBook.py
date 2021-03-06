import csv
import os
import time
import urllib.request
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

FILE_PATH = "images/"
if not os.path.exists(FILE_PATH):
    os.mkdir(FILE_PATH)

urlAccueil = "https://books.toscrape.com/"
page = requests.get(urlAccueil)
soup = BeautifulSoup(page.content, "html.parser")

title = []
category = []
number_available = []
price_including_max = []
price_excluding_max = []
review_rating = []
universal_product_code = []
product_page_url = []
image_url = []
product_description = []
en_tete = [
    "title", "category", "number_available", "price_including_max", "price_excluding_max", "review_rating",
    "universal_product_code", "product_page_url", "image_url", "product_description"
]


def urlSoup(u):
    pageUrl = requests.get(u)
    soupPage = BeautifulSoup(pageUrl.content, "html.parser")

    img = soupPage.img.get("src").lstrip("../")
    urlImg = urlAccueil + img
    descriptionBook = soupPage.find("article", class_="product_page").find_all("p")[3].get_text().strip()
    categoryBook = soupPage.find("ul", class_="breadcrumb").find_all("li")[2].a.get_text()
    td = soupPage.find_all("td")
    title.append(soupPage.h1.get_text())
    category.append(categoryBook)
    number_available.append(td[5].get_text())
    price_including_max.append(td[2].get_text())
    price_excluding_max.append(td[3].get_text())
    review_rating.append(td[6].get_text())
    universal_product_code.append(td[0].get_text())
    product_page_url.append(u)
    image_url.append(urlImg)
    product_description.append(descriptionBook)


for li in soup.find("ul", class_="nav-list").ul.find_all("li"):
    a = li.a.get("href")
    url = urlAccueil + a
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    allh3 = soup.find_all("h3")
    for h3 in allh3:
        urlBook = h3.a.get("href").strip("../")
        url = urlAccueil + "catalogue/" + urlBook
        urlSoup(url)

    next = soup.find("li", class_="next")
    currentPage = soup.find("li", class_="current")
    
    if next and currentPage:
        currentPage = soup.find("li", class_="current").get_text().strip()[-2:].strip()
        
        for i in range(int(currentPage) + 1):
            if i > 1:
                url = "https://books.toscrape.com/" + a.strip("index.html") + "page-{}".format(i) + ".html"
                page = requests.get(url)
                soup = BeautifulSoup(page.content, "html.parser")
                allh3 = soup.find_all("h3")
                for h3 in allh3:
                    urlNextBook = h3.a.get("href").strip("../")
                    url = urlAccueil + "catalogue/" + urlNextBook
                    urlSoup(url)

for i in range(len(image_url)):
    FILENAME = "image-{}".format(i) + ".jpg"
    FULL_PATH = FILE_PATH + FILENAME
    urllib.request.urlretrieve(image_url[i], FULL_PATH)

for i in tqdm(title, desc="All the books"):
    time.sleep(0.1)

with open("data.csv", "w", encoding="utf-8") as csvFile:
    w = csv.writer(csvFile, delimiter=",")
    w.writerow(en_tete)
    for t, c, na, pim, pem, rr, upc, ppu, iu, pd in zip(
        title, category, number_available, price_including_max,
        price_excluding_max, review_rating, universal_product_code,
        product_page_url, image_url, product_description
    ):
        w.writerow([t, c, na, pim, pem, rr, upc, ppu, iu, pd])





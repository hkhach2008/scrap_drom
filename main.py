from bs4 import BeautifulSoup
import requests 
from time import sleep
import csv


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
}

count = 0

def get_url():
    for count in range(1, 11):
        sleep(3)
        url = f"https://auto.drom.ru/bmw/all/page{count}/"
        response = requests.get(url, headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("a", class_="css-xb5nz8 ewrty961")
        for i in data:
            yield i.get("href")



def get_data():
    for card_url in get_url():
        response = requests.get(card_url)
        soup = BeautifulSoup(response.text, "lxml")
        tbody = soup.find("tbody")

        for i in range(0, 9):
            try:
                name = soup.find("h1", class_="css-1tjirrw e18vbajn0").find("span", class_="css-1kb7l9z e162wx9x0").text
                price = soup.find("div", class_="css-eazmxc e162wx9x0").text
                subkey = tbody.find_all("tr", class_="css-11ylakv ezjvm5n0")[i] 
                key = subkey.find("th", class_="css-38heja ezjvm5n2").text
                subvalue = tbody.find_all("tr", class_="css-11ylakv ezjvm5n0")[i]
                value = subvalue.find("td", class_="css-lm1m3k ezjvm5n1").text
                with open("data.csv", "a") as file:
                    writer = csv.writer(file)
                    if(count == 0):
                        writer.writerow(
                            (
                                name,
                                price, 
                                key,
                                value,
                            )
                        )
                        count = 1
                    else:
                        writer.writerow(
                            (
                                key,
                                value,
                            )
                        )
            except: 
                break
        count = 0



def main():
    get_data()



if __name__ == "__main__":
    main()
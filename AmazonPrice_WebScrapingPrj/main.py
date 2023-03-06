from bs4 import BeautifulSoup
import requests
import smtplib

url = "https://www.amazon.com/MSI-Stealth-Studio-Gaming-Laptop/dp/B0BT3DFR8W/ref=sr_1_7?qid=1677755760&refinements=p_36%3A200000-&rnid=386442011&s=computers-intl-ship&sr=1-7"
web_page = requests.get(url=url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"}).text
soup = BeautifulSoup(web_page, "lxml")

price = soup.find(name="span", class_="a-offscreen").getText()
price_as_float = float(price.split()[0])

title = soup.find(id="productTitle").getText().strip()
print(title)

BUY_PRICE = 2000

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login("/removed email for github upload/", "/removed password for github upload/")
        connection.sendmail(
            from_addr="/removed email for github upload/",
            to_addrs="/removed email for github upload/",
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}"
        )

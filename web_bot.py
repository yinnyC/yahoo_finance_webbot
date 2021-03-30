import requests
from bs4 import BeautifulSoup
import concurrent.futures


def current_price_crawler(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    try:
        page = requests.get(url)
        page.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
    except requests.exceptions.ConnectionError as e:
        print("Error Connecting:", e)
    except requests.exceptions.Timeout as e:
        print("Timeout Error:", e)
    except requests.exceptions.RequestException as e:
        print("Request exception: ", e)

    soup = BeautifulSoup(page.content, "lxml")
    quote_info = soup.find("div", attrs={"id": "quote-header-info"})
    price = quote_info.find("span", attrs={"data-reactid": "50"}).text
    price = price.replace(",", "")
    return float(price)


def current_price_fetcher(stocks):
    """
    Return the current price of the stocks in the parameter lists
    Input: A list of stocks
    Output: A list of stocks' current prices (Integer)
    """
    prices = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for stock in stocks:
            future = executor.submit(current_price_crawler, stock)
            prices.append(future.result())
    print(prices)


current_price_fetcher(["GOOG", "AAPL", "AMC"])

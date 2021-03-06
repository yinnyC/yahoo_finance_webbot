import requests
from bs4 import BeautifulSoup
import queue
from threading import Thread
import time


def crawler(symbol):
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
    price = soup.find(
        "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}
    ).text
    price = price.replace(",", "")
    return float(price)


def current_price_fetcher(stocks):
    """
    Return the current price of the stocks in the parameter lists
    Input: A list of stocks
    Output: A list of stocks' current prices (Integer)
    """
    threads = []
    prices = []
    que = queue.Queue()
    for stock in stocks:
        t = Thread(target=lambda q, arg1: q.put(crawler(arg1)), args=(que, stock))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    while len(prices) != len(stocks):
        prices.append(que.get())
    return prices


if __name__ == "__main__":
    start_time = time.time()
    print(
        current_price_fetcher(
            ["GOOG", "AAPL", "AMC", "DDOG", "TSLA", "ABNB", "SEAC", "HOFV"]
        )
    )
    elapsed_time = time.time() - start_time
    print(f"elapsed_time= {elapsed_time}")

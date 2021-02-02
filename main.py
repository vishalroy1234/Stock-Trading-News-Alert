import requests
from twilio.rest import Client

account_sid = "ACb8881f1d8e465828f59751f7c1b1a402"
auth_token = "4fca1bb9bfbadad6e0c35f80c9aa05dc"

STOCKS_API_KEY = "NIZQHGR7LJA6RVC7"
NEWS_API_KEY = "8548ff4d21f445298f489ff01c750cb3"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stocks_url = "https://www.alphavantage.co/query"
news_url = "http://newsapi.org/v2/everything"

stocks_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCKS_API_KEY
}

response = requests.get(url=stocks_url, params=stocks_parameters)
response.raise_for_status()
stocks_data = response.json()
latest_closing_price = float(stocks_data['Time Series (Daily)'][list(stocks_data['Time Series (Daily)'])[0]]['4. close'])
day_before_latest_closing_price = float(stocks_data['Time Series (Daily)'][list(stocks_data['Time Series (Daily)'])[1]]['4. close'])
percentage_change_in_closing_price = round(((latest_closing_price - day_before_latest_closing_price)/latest_closing_price)*100, 2)
print(f"{percentage_change_in_closing_price}%")


news_parameters = {
    "qInTitle": COMPANY_NAME,
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY,
    "from": list(stocks_data['Time Series (Daily)'])[0],
    "to": list(stocks_data['Time Series (Daily)'])[1]
}
if abs(percentage_change_in_closing_price) > 5:
    response = requests.get(url=news_url, params=news_parameters)
    response.raise_for_status()
    news_data = response.json()
    for news in range(3):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"{STOCK}: {abs(percentage_change_in_closing_price)}%️\nHeadline: {news_data['articles'][news]['title']}\nBrief: {news_data['articles'][news]['description']}",
            from_='+18329254054',
            to='Your number'
        )

        print(message.status)
        print(news_data['articles'][news]['title'])
        print(news_data['articles'][news]['description'])



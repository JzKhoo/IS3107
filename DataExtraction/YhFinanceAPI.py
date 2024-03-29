import requests
import pandas as pd
import configparser
# from google.cloud import bigquery
import yfinance as yf
from datetime import timedelta, datetime

# url = "https://yh-finance.p.rapidapi.com/stock/v3/get-historical-data"

# querystring = {"symbol":"meta","region":"US"} #Currently reading Meta stock data

# config = configparser.ConfigParser()
# config.read('config.ini')

# headers = {
# 	"X-RapidAPI-Key": f"{config['yhFinance']['RAPID_API_KEY']}",
# 	"X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# Define the list of tickers for the top 25 most watched stocks
tickers = ['TSLA', 'MSFT' ,'PG' ,'META' ,'AMZN' ,'GOOG' ,'AMD' ,'AAPL' ,'NFLX' ,'TSM' ,'KO'
,'F' ,'COST' ,'DIS', 'VZ' ,'CRM' ,'INTC' ,'BA' ,'BX' ,'NOC', 'PYPL' ,'ENPH', 'NIO',
'ZS' ,'XPEV']

stocks_data = pd.DataFrame()

# Set start & end date of stock market data
end_date = datetime.now()
start_date = end_date - timedelta(days=15*365)

def formatDate(date):
    date= datetime.strptime(str(str(date).replace(" 00:00:00", "")), '%Y-%m-%d')
    return str(date.strftime('%Y-%m-%d'))

# Download data from Yahoo Finance
for ticker in tickers:
    history = yf.download(ticker, start=start_date, end=end_date, interval='1d', prepost=False)
    history = history.loc[:, ['Open', 'Close', 'Volume']]
    history.reset_index(inplace=True)
    history['Date'] = history['Date'].apply(formatDate)
    history = history.dropna()
    history["Date"] = pd.to_datetime(history["Date"])
    history['Symbol'] = ticker
    # sorted_hist = history.sort_values(by='Symbol', ascending=True)
    sorted_hist = history.sort_values(by='Date', ascending=False)

    stocks_data = pd.concat([stocks_data, sorted_hist], axis=0)

    # history['Date'] = history['Date'].astype(str)
    # print(type(sorted_hist['Date'][0]))
    # print(sorted_hist)



    
stocks_data.to_gbq("is3107-project-383009.Dataset.StockData", project_id="is3107-project-383009", if_exists='replace')

# responseJson = response.json()
# filtered_data = []
# for day in responseJson["prices"]:
#     day_data = {
#                 'date': day['date'], #Date in number of seconds since epoch
#                 'open': day['open'],
#                 'close': day['close'],
#                 'volume': day['volume'],
#                 }
#     filtered_data.append(day_data)

# df = pd.DataFrame(data=filtered_data)
# print(df)
# df.to_csv("YhFinance.csv", index=False)
# df.to_gbq("is3107-project-383009.Dataset.test2", project_id="is3107-project-383009")

# Alternative way to push data to BigQuery

# client = bigquery.Client(project="is3107-project-383009")
# dataset_ref = client.dataset(dataset_id="is3107-project-383009.Dataset")
# table_ref = dataset_ref.table(table_id="is3107-project-383009.Dataset.YhFinance")
# loadjob = client.load_table_from_dataframe(df, table_ref).result()
# print("Loadjob ID" + loadjob)
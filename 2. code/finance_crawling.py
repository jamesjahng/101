import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup

class DailyPrice():
    def __init__(self, date, open, high, low, close):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    @classmethod
    def from_csv(cls, csv):
        pass

    @classmethod
    def from_html(cls, tag):
        date, close, _, open_, high, low, volume = tag.find_all('td')
        date = datetime.datetime.strptime(date.span.get_text(), '%Y.%m.%d')
        open_ = int(open_.span.get_text().replace(',', ''))
        high = int(high.span.get_text().replace(',', ''))
        low = int(low.span.get_text().replace(',', ''))
        close = int(close.span.get_text().replace(',', ''))
        return cls(date, open_, high, low, close)
    
    def __str__(self):
        return f'{self.date} {self.open} {self.high} {self.low} {self.close}'
    
    def is_past(self, date_to_compare):
        return self.date < date_to_compare 

def get_stock_code_and_end_date():
    # stock_code = input('검색할 종목 코드: ')
    # end_date = input('언제까지 검색할까요? (YYYY-MM-DD): ')
    stock_code = '005380'
    end_date = '2017-01-25'
    return stock_code, datetime.datetime.strptime(end_date, '%Y-%m-%d')

def scrap_from_naver_finance(stock_code, end_date):
    prices = list()
    url = 'https://finance.naver.com/item/sise_day.nhn'
    current_page = 1
    completed = False
    while not completed:
        data_table = BeautifulSoup(requests.get(url, {'code': stock_code, 'page': current_page}).text, 'lxml')
        daily_prices = data_table.find('table').find_all('tr', attrs={'onmouseover' : 'mouseOver(this)'})
        for daily_price in daily_prices:
            current_date_price = DailyPrice.from_html(daily_price)
            if current_date_price.is_past(end_date):
                completed = True
                break
            else:
                prices.append(current_date_price)
        current_page += 1
    return prices

def scrap_from_naver_finance2(stock_code, end_date):
    current_page = 1
    completed = False
    datatable = None
    while not completed:
        url = f'https://finance.naver.com/item/sise_day.nhn?code={stock_code}&page={current_page}'
        current_page_datatable = pd.read_html(url)[0].dropna()
        current_page_datatable = current_page_datatable.astype({'날짜': str, '종가': int, '전일비': int, '시가': int, '고가': int, '저가': int, '거래량': int})
        current_page_datatable['날짜'] = pd.to_datetime(current_page_datatable['날짜'], format="%Y.%m.%d")
        del current_page_datatable['전일비']
        datatable = current_page_datatable if datatable is None else datatable.append(current_page_datatable, ignore_index=True)
        current_page += 1
        date_at_last_data = list(datatable.tail(1)['날짜'])[0]
        if date_at_last_data < end_date:
            break
    return datatable

def generate_moving_average(dataframe, window_size):
    return dataframe.rolling(window=window_size).mean().dropna().astype({'종가': int})

if __name__ == "__main__":
    stock_code, end_date = get_stock_code_and_end_date()
    datatable = scrap_from_naver_finance2(stock_code, end_date)
    mv_15 = generate_moving_average(datatable['종가'], 15)
    mv_50 = generate_moving_average(datatable['종가'], 50)
    datatable['mv_15'] = mv_15
    datatable['mv_50'] = mv_50
    datatable = datatable.dropna().iloc[::-1]

    #억
    fund = 10000000000
    stock = 0
    position = 'SELL'

    for i, row in datatable.iterrows():
        if row['mv_15'] > row['mv_50'] and position == 'SELL':
            stock += fund // row['종가'] 
            fund -= stock * row['종가']
            print('삿따!', row, stock, fund)
            position = 'BUY'
            input()
            
        if row['mv_15'] < row['mv_50'] and position == 'BUY':
            fund += stock * row['종가']
            stock = 0
            print('팔아따!', row, stock, fund)
            position = 'SELL'
            input()

    

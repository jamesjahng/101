import requests
import datetime
from bs4 import BeautifulSoup

class DailyPrice():
    def __init__(self, date, open, high, low, close):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close

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
        return f'{self.date} {self.open} {self.high} {self.low} {self.close}' #파이썬 업데이트 하자
        # return '{} {} {} {} {}'.format(self.date, self.open, self.high, self.low, self.close)

    def is_past(self, date_to_compare):
        return self.date < date_to_compare # 날짜끼리 비교 datetime

def get_stock_code_and_end_date():
    # stock_code = input('검색할 종목 코드:')
    # end_date = input('언제까지 검색할까요? (YYYY-MM-DD): ')
    stock_code = '005930'
    end_date = '2017-01-25'
    return stock_code, datetime.datetime.strptime(end_date, '%Y-%m-%d') # 튜플로 리턴됨

def scrap_from_naver_finance(stock_code, end_date):
    prices = list()
    url = 'https://finance.naver.com/item/sise_day.nhn'
    current_page = 1
    completed = False
    while not completed:
        data_table = BeautifulSoup(requests.get(url, {'code': stock_code, 'page': current_page}).text, 'html.parser')
        daily_prices = data_table.find('table').find_all('tr', attrs={'onmouseover' : 'mouseOver(this)'}) # tr을 다 찾으면 짜바리들도 섞이기 때문에 공통 attrs로 가공
        for daily_price in daily_prices:
            current_date_price = DailyPrice.from_html(daily_price)
            if current_date_price.is_past(end_date):
                completed = True
                break
            else:
                prices.append(DailyPrice.from_html(daily_price))
        current_page += 1
    return prices
        

if __name__ == "__main__":
    # 사용자한테 물어보자 : 어떤 종목? 언제까지?
    stock_code, end_date = get_stock_code_and_end_date()
    # 데이터 수집
    prices = scrap_from_naver_finance(stock_code, end_date)
    # 데이터 표현
    for price in prices:
        print(price)

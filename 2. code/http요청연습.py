import requests
#from selenium import webdriver
from bs4 import BeautifulSoup

#url = 'https://www.devex.com/api/public/search/articles?page%5Bsize%5D=20'
#url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
res = requests.get('https://finance.naver.com/item/sise_day.nhn?code=005930')
#print(res.text)
#html = res.read().decode('euc-kr')


#driver = webdriver.Chrome('./chromedriver')
#driver.get(url)
#id_input = driver.find_element_by_xpath('//*[@id="id"]')
#id_input.send_keys('zzangy92')
#pw_input = driver.find_element_by_xpath('//*[@id="pw"]')
#pw_input.send_keys('asdasd')
#login_btn = driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input')
#login_btn.click()


bs = BeautifulSoup(res.text, 'html.parser')
table = bs.find('table', attrs={'class': 'type2'})
#print(table)
# print(bs.head.title)
for tag in table:
    # date = tag.findAll(tr:).get_text()
    # end = tag.findAll('tr', attrs={'}).get_text()
    # start = tag.find('tr', attrs={''}).get_text()
    # high = tag.find('tr', attrs={'class': 'tah p11'}).get_text()
    # low = tag.find('tr', attrs={'class': 'tah p11'}).get_text()

# print(date, end, start, high, low)
##rows = [row for index, row in enumerate(rows) if index % 2 == 0]
##for row in rows:
 ##   post_no = row.find('div', attrs={'class': 'inner_number'}).get_text()
 ##   post_title = row.find('a', attrs={'class': 'article'}).get_text().strip()
 ##   post_author = row.find('a', attrs={'class': 'm-tcol-c'}).get_text()
 ##  post_date = row.find('td', attrs={'class': 'td_date'}).get_text()
 ##   print(post_no, post_title, post_author, post_date)
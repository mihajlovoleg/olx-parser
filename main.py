import requests
from bs4 import BeautifulSoup
import pandas as pd
from html.parser import HTMLParser

main_url = "https://www.olx.pl/nieruchomosci/poznan/?search%5Bdistrict_id%5D=327"

response = requests.get(main_url)

main_soup = BeautifulSoup(response.content, 'html.parser')

pages_a = main_soup.find_all('a', {'class':'css-1mi714g'})

ad_titles = []
ad_prices = []
ad_hrefs = []

for classes in pages_a:
	pages_href = classes.get('href')
	pages_url = requests.get('https://www.olx.pl' + pages_href)

	pages_soup = BeautifulSoup(pages_url.content, 'html.parser')

	ad_title = pages_soup.find_all('h6',{'class':'css-16v5mdi er34gjf0'})

	price_p = pages_soup.find_all('p',{'class':'css-10b0gli er34gjf0'})

	hrefs_a = pages_soup.find_all('a',{'class':'css-rc5s2u'})

	

	for prices in price_p:
		page_ad_price = prices.text
		ad_prices.append(page_ad_price)

	for titles in ad_title:
		page_ad_titles = titles.text
		ad_titles.append(page_ad_titles)

	for hrefs in hrefs_a:
		ad_href = 'https://www.olx.pl' + hrefs.get('href')
		ad_hrefs.append(ad_href)

excel_data = {'Name':ad_titles,
              'Price':ad_prices,
              'Ad url':ad_hrefs}

add_df = pd.DataFrame(excel_data)

add_df.to_excel('ads.xlsx', index=True)





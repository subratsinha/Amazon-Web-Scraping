import csv
import requests
from bs4 import BeautifulSoup

def extract_record(item):
    atag=item.h2.a
    # print(atag)
    
    description=atag.text.strip()
    # print(description)
    
    product_url='https://www.amazon.in/'+ atag.get('href')
    # print(product_url)
    
    try:
        price_parent=item.find('span','a-price')
        product_price=price_parent.find('span','a-offscreen').text
    
    except AttributeError:
        return
    
    try:
        product_rating=item.i.text
        product_review=item.find('span',{'class':'a-size-base'}).text
        print(product_review)
        
    except AttributeError:
        rating=''
        review_count=''
        

    result=(description,product_url,product_price,product_rating,product_review)
    
    return result



    
URL = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

webpage = requests.get(URL, headers=headers)
soup = BeautifulSoup(webpage.content, "lxml")
#print(soup)
    
records=[]

for page in range(1,21):
    URL+='&page={}'
    webpage = requests.get(URL, headers=headers)
    soup = BeautifulSoup(webpage.content, "lxml")
    results=soup.find_all('div',{"data-component-type":"s-search-result"})
    # print(results)
for item in results:
    record=extract_record(item)
    if record:
        records.append(record)
with open('results.csv','w', newline='', encoding='utf8') as f:
    writer=csv.writer(f)
    writer.writerow(['Description','url','price','rating','review'])
    writer.writerows(records)
                

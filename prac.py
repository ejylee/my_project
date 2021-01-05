import requests
from bs4 import BeautifulSoup

# 크롤링 데이터를 넣을 DB 연결하기
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# ?! 기존 db에 저장되어있던 최신값 가져오기 어떻게하지? -> db.foo.find().sort({x:-1})
# ?! 가져온 값들을 리스트형태로 어떻게 만들지? -> dbBags 리스트 만들기

# 새로 크롤링하기 (newBags 리스트 만들기)
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.freitag.ch/ko/f41?items=showall',headers=headers)
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
path = "./chromedriver"
driver = webdriver.Chrome(path)
driver.get("https://www.freitag.ch/ko/f41?items=showall")
time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')
bags = soup.select('#products-selector > ul > li')
productId = []
dataDimension17 = []
dataDimension18 = []
img = []
for bag in bags:
    productId.append(bag['data-product-id'])
    dataDimension17.append(bag['data-dimension17'])
    dataDimension18.append(bag['data-dimension18'])
    img.append(bag.select_one('img'))
newBags = {'productId': productId}
print(newBags)

# ?! 기존 db에서 가져온 리스트 (dbBags) - 새로 크롤링한 리스트 (newBags) 비교하기
    #updated = list(set(newBags) - set(dbBags))
    #print(updated)
    #db.bags.insert_one(doc)
driver.quit()

# ?! 차이나는 값의 productId, datadimension17, datadimension18, img 이메일로 보내주기


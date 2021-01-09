import requests
from bs4 import BeautifulSoup

# 크롤링 데이터를 넣을 DB 연결하기
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta


# 기존 db에 저장되어있던 최신값 가져오기
db_data = list(db.bags.find().limit(1))
# 가져온 값들 중 productID 리스트로 만들기
list1 = db_data[0]['productId']
print("여기는 list1")
print(list1)

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

list2 = productId
list2.append("가짜수")

newBags = {'productId': productId}
print("여기는newBags")
print(newBags)

# ?! 기존 db에서 가져온 리스트 (dbBags) - 새로 크롤링한 리스트 (newBags) 비교하기
updated = list(set(list2) - set(list1))
print(list2)
print("결과값!!!!@#!@#!@#!@$!@$!@")
print(updated)
if len(updated) == 0 :
    print("no change")
else :
    print("변한게 있어서 메일 보내줘야함!!!!")
#db.bags.insert_one(newBags)
driver.quit()

# ?! 차이나는 값의 productId, datadimension17, datadimension18, img 이메일로 보내주기


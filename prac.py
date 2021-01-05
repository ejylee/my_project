import requests
from bs4 import BeautifulSoup

# 크롤링 데이터를 넣을 DB 연결하기
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# 타겟 URL을 읽어서 HTML 받아오
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.freitag.ch/ko/f41?items=showall',headers=headers)

# 브라우저 제어하여 크기롤링 해오기
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

path = "./chromedriver"
driver = webdriver.Chrome(path)
driver.get("https://www.freitag.ch/ko/f41?items=showall")
time.sleep(3)

# 크롤링 해온 정보 튜닝해서 DB에 집어넣기
#soup = BeautifulSoup(driver.page_source, 'html.parser')
#bags = soup.select('#products-selector > ul > li')
#for bag in bags:
#    productId = bag['data-product-id']
#    dataDimension17 = bag['data-dimension17']
#    dataDimension18 = bag['data-dimension18']
#    img = bag.select_one('img')
    #print(productId,dataDimension17,dataDimension18,img) 크롤링 결과값 확인해보기
#    doc = {
#       'productId': productId,
#        'dataDimension17': dataDimension17,
#        'dataDimension18': dataDimension18,
#        'img': img["src"]
#    }
#    db.bags.insert_one(doc)
#driver.quit()

#DB에 넣어둔 값과 새로 크롤링한 값 비교하기
while True :
    dbBags = list(db.bags.find({}))
    #print(dbBags) db에 저장된 값이 잘 불러와지는지 확인
    time.sleep(3)
    newBags = []
    path = "./chromedriver"
    driver = webdriver.Chrome(path)
    driver.get("https://www.freitag.ch/ko/f41?items=showall")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    bags = soup.select('#products-selector > ul > li')
    for bag in bags:
        productId = bag['data-product-id']
    dataDimension17 = bag['data-dimension17']
    dataDimension18 = bag['data-dimension18']
    img = bag.select_one('img')
    doc = {
        'productId': productId,
        'dataDimension17': dataDimension17,
        'dataDimension18': dataDimension18,
        'img': img["src"]}

    updated = list(set(newBags) - set(dbBags))
    print(updated)
    db.bags.insert_one(doc)
driver.quit()
# if len(C) != 0 :
# print("메일쏴주기!!!")

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# url = input("크롤링할 URL을 기입하거라")

# url = "http://mulamen.com/shop/shopdetail.html?branduid=10182780&xcode=006&mcode=002&scode=&type=Y&sort=manual&cur_code=006002&GfDT=bG13VQ%3D%3D"

url = "https://mulamen.com/shop/shopdetail.html?branduid=10182737&xcode=008&mcode=001&scode=&type=Y&sort=manual&cur_code=008001&GfDT=bm1%2FW10%3D"

driver = webdriver.Chrome('/Users/BAT_202008/Desktop/PythonWorkspace/chromedriver')
driver.implicitly_wait(1)
driver.get(url)
driver.implicitly_wait(1)

url_review = driver.find_element_by_xpath('//*[@id="crema-product-reviews-1"]')
url_review_source = url_review.get_attribute('src')
driver.get(url_review_source)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

reviews = []

while True:
    try:
        reviewArray = soup.find_all("div", {"class" : "review_message review_message--collapsed review_message--collapsed3 js-translate-review-message"})
        for data in reviewArray:
            reviews.append(data.get_text())
        temp = reviewArray
        next_page_btn = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[3]/div/div/a[last()]').click()
        time.sleep(1)
        driver.get(driver.current_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
    except:
        print("리뷰수집끝남")
        break

print(len(reviews))

df = pd.DataFrame({'Review' : reviews})
df = df.replace('\n', ' ', regex=True)
df.to_csv('Reviews.csv')

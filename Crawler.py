from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 如果你的電腦夠快的話你可以自己調整time.sleep的時間
# 抓不同idol的時候


def download_images_selenium(url, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    driver_path = '/Users/baizonghan/Desktop/爬蟲專案/chromedriver-mac-arm64/chromedriver'
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    time.sleep(10) 

    login_buttons = driver.find_elements(By.XPATH, '//*[@id="__next"]/section/div[1]/div/div/div[2]/p/span')

    if len(login_buttons) > 0:  
        login_buttons[0].click()  

        username_field = driver.find_element(By.XPATH, '//*[@id="__next"]/section/div[6]/div[2]/div/form/div[1]/input')
        password_field = driver.find_element(By.XPATH, '//*[@id="__next"]/section/div[6]/div[2]/div/form/div[2]/input')
        login_button = driver.find_element(By.XPATH, '//*[@id="__next"]/section/div[6]/div[2]/div/form/button') 

        username_field.send_keys(" ")       #在這邊填你的帳號
        password_field.send_keys(" ")       #在這邊填你的密碼
        login_button.click()
    
        time.sleep(20) 
    
    driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/a[3]').click()  
    time.sleep(10)   
    SearchBar = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/section/div/div/div[1]/input')
    SearchBar.send_keys('IVE') #在這邊更改要搜尋的團體名稱
    time.sleep(10)
    SearchBar.send_keys(Keys.ENTER)
    time.sleep(25)

    # 引導至團體頁面
    #點團體
    driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/section/div/div/div[2]/div[1]/div[2]/a/div').click()
    time.sleep(20) 
    #點member類別
    driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/section/div[3]/div/div/div[1]/div[2]').click() 
    time.sleep(10) 
    driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/section/div[3]/div/div/div[2]/div[2]/div/div[1]').click()
    #點成員
    time.sleep(60)
    
    card_containers = driver.find_elements(By.CLASS_NAME, 'Member_cardContainer__1pirl')
    
    # 定位到非浮水印的標籤
    images = driver.find_elements(By.CSS_SELECTOR, "a .Image_image__xxTfb:first-of-type")

    for i, img in enumerate(images):
        img_url = img.get_attribute('src')
        if img_url:
            # 圖片下載與寫入
            img_data = requests.get(img_url).content
            img_name = f'image_{i+1}.jpg' #在此處更改圖片的存儲名稱
            img_path = os.path.join(save_folder, img_name)
            with open(img_path, 'wb') as file:
                file.write(img_data)
            print(f'下載完成：{img_path}')
    
    driver.quit()


url = 'https://kcollect.net/dashboard/browse' #勿改
save_folder = 'IVE_Gaeul'  # 新增保存下載圖片的文件夾，自行更改資料夾名稱
download_images_selenium(url, save_folder)
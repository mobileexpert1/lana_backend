from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def get_card_product(url):
    mobile_emulation = {
        "deviceName": "Nexus 5"
    }
    driver_path = r"D:\chromedriver-win64/chromedriver.exe"

    driver_service = Service(driver_path)
    driver_service.start()

    ua = UserAgent()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'user-agent={ua.random}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--enable-automation')

    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36")
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(
        url)
    WebDriverWait(driver, 10).until(lambda x: x.execute_script("return document.readyState") == "complete")

    try:
        popup = driver.find_element(By.CSS_SELECTOR, 'popup-close-button-class')
        popup.click()
    except:
        pass

    try:
        body_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        WebDriverWait(driver, 1).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        body_content = body_element.get_attribute('innerHTML')
        print("Body content after load:\n", body_content)
    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(20)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    with open("test.html", 'w', encoding='utf-8') as file:
        file.write(str(soup.prettify()))

    section = soup.find('section', class_='container')
    data = []
    if section:
        # print("Section content:\n", section.prettify())
        product_section = section.find_all("div", class_="product-item")
        for p_section in product_section:
            time.sleep(1)
            p_name = p_section.find("span", class_="goods-name__text")
            # price = p_section.find("span", class_="price-amount")
            price = p_section.find("span", class_="price-sale discount")

            product = {
                "name": p_name.text, "price": price.text
            }

            # product img
            img = p_section.find("img", class_="lazyload series-tag")
            if img:
                product['img'] = img.get('src')

            # color and size
            color_div = p_section.find("div", class_="goods-sale-attr sale-attr")
            color_img = color_div.find("img")
            if color_img:
                product['color_img'] = color_img.get("src")

            color_size = color_div.find("span")
            if color_size:
                product['color_size'] = color_size.text.strip()



            data.append(product)

    else:
        print("Section not found.")

    # time.sleep(50)
    driver.close()

    return data


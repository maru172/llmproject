from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time



class CrawlingData:
    def bs_Setup(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def crawling_Setup():
        options = Options()
        options.add_argument("--headless")  
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")  
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(120)  
        print("드라이버 시작")
        return driver

    def category_set(driver, category):
        url_map = {
            'Politics': "https://www.yahoo.com/news/politics/",
            'World': "https://www.yahoo.com/news/world/",
            'Us': "https://www.yahoo.com/news/us/"
        }
        if category in url_map:
            driver.get(url_map[category])
        return driver

    def scroll_down(driver, iterations):
        for _ in range(iterations):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.2)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'news')]"))
            )
            print("down")

    def news_access(driver, url, i, mode):
        path = url.split("https://www.yahoo.com")[-1]
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="module-stream"]/ul/li[{i}]/div/div/h3/a[@href="{path}"]'))
        )
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', { bubbles: true }));", element)
        time.sleep(0.5)

    def yahoo_news_home_page_urls(driver):
        main_page_urls = []
        main_page_titles = []
        main_page_press = []
        ul_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="module-stream"]/ul'))
        )
        li_tags = ul_element.find_elements(By.TAG_NAME, 'li')
        for li in li_tags:
            try:
                span_tag = li.find_elements(By.TAG_NAME, 'span')
                h3_tag = li.find_element(By.TAG_NAME, 'h3')
                a_tag = h3_tag.find_element(By.TAG_NAME, 'a')
                href_value = a_tag.get_attribute('href')
                main_page_titles.append(h3_tag.text)
                main_page_urls.append(href_value)
                main_page_press.append(span_tag[1].text if len(span_tag) > 1 else "Unknown Press")
            except:
                pass
        return main_page_urls, main_page_titles, main_page_press

    def news_title(driver):
        elements = driver.find_elements(By.CSS_SELECTOR, "[class='caas-title-wrapper']")
        return elements[0].text if elements else "No title"

    def news_author_date_time(driver, soup):
        author_name = soup.select_one('.text-sm.font-semibold') or \
                      soup.select_one('.caas-attr-meta .caas-attr-item-author')
        date_time = soup.select_one('.inline-block time') or \
                    soup.select_one('.caas-attr-meta time')

        return (author_name.text if author_name else "Unknown Author",
                date_time.text if date_time else "Unknown Date")

    def news_original_text(driver, soup):
        p_tags = soup.select('.col-body p')
        if not p_tags:
            return "No content available"
        return ''.join(p.text for p in p_tags)

    def news_caption(driver, soup):
        caption_div = soup.select_one('figcaption div[style="max-height:none;overflow:visible"]')
        return caption_div.text.strip() if caption_div else "No caption"

    @staticmethod    
    def news_imageURL(self, soup):
        img_tag = soup.select_one('img[data-nimg="fill"][fetchpriority="high"]')
        return img_tag['src'] if img_tag and 'src' in img_tag.attrs else "No image"
    
    
    ## 뉴스 날짜, 시간 추출
    # def news_date_time(driver):
    #     ## caas-attr-time-style 클래스 내부 값 저장
    #     elements = driver.find_elements(By.CSS_SELECTOR, "[class='caas-attr-time-style']")
    #     date_time = elements[0].text.split('·')[0]
        
    #     return date_time.split(' at ')
    

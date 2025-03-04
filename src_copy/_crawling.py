from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import requests
from bs4 import BeautifulSoup
import time

class CrawlingData:
    @staticmethod
    def bs_Setup(url):
        """BeautifulSoup 객체 생성"""
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')

    @staticmethod
    def crawling_Setup():
        """Selenium 드라이버 셋업 (Firefox)"""
        service = Service('/snap/bin/geckodriver')
        options = Options()
        options.headless = True  # 헤드리스 모드
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_page_load_timeout(120)  # 페이지 로딩 시간 120초로 증가
        print("드라이버 시작")
        return driver

    @staticmethod
    def category_set(driver, category):
        """카테고리에 따라 Yahoo 뉴스 페이지 로드"""
        categories = {
            'Politics': "https://www.yahoo.com/news/politics/",
            'World': "https://www.yahoo.com/news/world/",
            'Us': "https://www.yahoo.com/news/us/",
        }
        driver.get(categories.get(category, "https://www.yahoo.com/news/"))
        return driver

    @staticmethod
    def scroll_down(driver, iterations):
        """일정 횟수만큼 스크롤 다운"""
        for _ in range(iterations):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.2)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'news')]")
            ))
            print("down")

    @staticmethod
    def news_access(driver, url, i):
        """뉴스 페이지로 이동"""
        path = url.split("https://www.yahoo.com")[-1]
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="module-stream"]/ul/li[{i}]/div/div/h3/a[@href="{path}"]'))
        )
        driver.execute_script("arguments[0].click();", element)
        time.sleep(0.5)

    @staticmethod
    def yahoo_news_home_page_urls(driver):
        """Yahoo 뉴스 홈페이지에서 기사 목록 추출"""
        main_page_urls, main_page_titles, main_page_press = [], [], []
        ul_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="module-stream"]/ul'))
        )
        li_tags = ul_element.find_elements(By.TAG_NAME, 'li')

        for li in li_tags:
            try:
                h3_tag = li.find_element(By.TAG_NAME, 'h3')
                a_tag = h3_tag.find_element(By.TAG_NAME, 'a')
                span_tag = li.find_elements(By.TAG_NAME, 'span')
                
                main_page_titles.append(h3_tag.text)
                main_page_urls.append(a_tag.get_attribute('href'))
                main_page_press.append(span_tag[1].text if len(span_tag) > 1 else "")
            except Exception:
                continue

        return main_page_urls, main_page_titles, main_page_press

    @staticmethod
    def news_title(driver):
        """뉴스 제목 추출"""
        element = driver.find_element(By.CSS_SELECTOR, ".caas-title-wrapper")
        return element.text if element else "No title"

    @staticmethod
    def news_author_date_time(soup):
        """기자 이름 및 날짜 추출"""
        author = soup.select_one('.inline-block .text-sm.font-semibold') or soup.select_one('.caas-attr-meta .caas-attr-item-author')
        date_time = soup.select_one('.inline-block time') or soup.select_one('.caas-attr-meta time')
        return (author.text if author else "Unknown"), (date_time.text if date_time else "Unknown")

    @staticmethod
    def news_original_text(soup):
        """뉴스 원문 추출"""
        return " ".join([p.text for p in soup.select('.col-body p')])

    @staticmethod
    def news_caption(soup):
        """뉴스 캡션 추출"""
        caption_div = soup.select_one('figcaption div[style="max-height:none;overflow:visible"]')
        return caption_div.text.strip() if caption_div else "No photo"

    @staticmethod    
    def news_imageURL(soup):
        """뉴스 이미지 URL 추출"""
        img_tag = soup.select_one('img[data-nimg="fill"][fetchpriority="high"]')
        return img_tag['src'] if img_tag else "No image"

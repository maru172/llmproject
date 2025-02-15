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
    def bs_Setup(url):
        # 페이지 요청
        response = requests.get(url)
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return soup
    ## 셀레니움 드라이버 셋업
    def crawling_Setup():
        ## chrome driver activate
        # driver = webdriver.Chrome()
        # ChromeDriver 설정
        options = Options()
        options.headless = True  # 헤드리스 모드
        print("옵션설정")
        # Firefox 드라이버 실행
        service = Service('/snap/bin/geckodriver')
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_page_load_timeout(120)  # 페이지 로딩 시간 120초로 증가
        print("드라이버 시작")
        return driver

    def category_set(driver, category):
        if category == 'Politics':
            ## 야후 뉴스(정치) 홈페이지 가져오기
            driver.get("https://www.yahoo.com/news/politics/") 
        elif category == 'World':
            ## 야후 뉴스(세계) 홈페이지 가져오기
            driver.get("https://www.yahoo.com/news/world/")
        elif category == 'Us':
            ## 야후 뉴스(세계) 홈페이지 가져오기
            driver.get("https://www.yahoo.com/news/us/")
        
        return driver
    
    def scroll_down(driver, iterations):
        seq = 0
        while iterations > seq:
            ## 스크롤 내리기 (맨 끝으로)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.2)
            # 새로운 뉴스 기사가 로드될 때까지 대기
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'news')]")))
            print("down")
            seq = seq + 1 
        
    def news_access(driver, url, i, mode):
        path = url.split("https://www.yahoo.com")[-1]
        
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="module-stream"]/ul/li[{i}]/div/div/h3/a[@href="{path}"]'))
        )
                
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', { bubbles: true }));", element)
        time.sleep(0.5)
        
    
    ## 뉴스 홈페이지에서 url 목록 추출
    def yahoo_news_home_page_urls(driver):
        main_page_urls = []
        main_page_titles = []
        main_page_press = []
        # 특정 요소가 로드될 때까지 대기
        ul_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="module-stream"]/ul'))
        )
         # ul 안의 모든 li 태그 찾기
        li_tags = ul_element.find_elements(By.TAG_NAME, 'li')
        
        # 각 li 태그의 텍스트 출력
        for li in li_tags:
            try:
                span_tag = li.find_elements(By.TAG_NAME, 'span')
                h3_tag = li.find_element(By.TAG_NAME, 'h3')
                a_tag = h3_tag.find_element(By.TAG_NAME, 'a')
                href_value = a_tag.get_attribute('href')
                
                main_page_titles.append(h3_tag.text)
                main_page_urls.append(href_value)
                main_page_press.append(span_tag[1].text)
            except:
                pass
        return main_page_urls, main_page_titles, main_page_press
        
    ## 뉴스 제목 추출
    def news_title(driver):
        ## caas-title-wrapper 클래스 내부 값 저장
        elements = driver.find_elements(By.CSS_SELECTOR, "[class='caas-title-wrapper']")

        return elements[0].text
    
    ## 뉴스 저자 추출
    def news_author_date_time(driver, soup):
        try:
            # 기자 이름
            author_name = soup.select_one('.inline-block .text-sm.font-semibold')
            # 날짜 추출
            date_time = soup.select_one('.inline-block time')
            
            return author_name.text, date_time.text
        except:
            # 기자 이름
            author_name = soup.select_one('.caas-attr-meta .caas-attr-item-author')
            # 날짜 추출
            date_time = soup.select_one('.caas-attr-meta time')
            return author_name.text, date_time.text
        
        ## 뉴스 원문 추출
    def news_original_text(driver, soup):
        original = ''
        # ## caas-body 클래스 내부 값 저장
        # elements = driver.find_elements(By.CSS_SELECTOR, "[class='caas-body']")
        
        # return elements[0].text
        
        # col-body 클래스의 div 내부의 모든 p 태그 찾기
        p_tags = soup.select('.col-body p')

        # 각 p 태그에서 텍스트 추출
        for p in p_tags:
            original = original + p.text
            
        return original
    
    ## 뉴스 캡션 추출
    def news_caption(driver, soup):
        ## caption-collapse 클래스 내부 값 저장
        try:
            # elements = driver.find_elements(By.CSS_SELECTOR, "[class='caption-collapse']")
            # return elements[0].text
            # figcaption 내부의 div에서 텍스트 추출
            caption_div = soup.select_one('figcaption div[style="max-height:none;overflow:visible"]')

            # 텍스트 출력
            if caption_div:
                return caption_div.text.strip()
        except:
            return "No photo"
        
    @staticmethod    
    def news_imageURL(self, soup):
        """뉴스 이미지 URL 추출"""
        img_tag = soup.select_one('img[data-nimg="fill"][fetchpriority="high"]')
        return img_tag['src'] if img_tag else "No image"

    
    
    ## 뉴스 날짜, 시간 추출
    # def news_date_time(driver):
    #     ## caas-attr-time-style 클래스 내부 값 저장
    #     elements = driver.find_elements(By.CSS_SELECTOR, "[class='caas-attr-time-style']")
    #     date_time = elements[0].text.split('·')[0]
        
    #     return date_time.split(' at ')
    

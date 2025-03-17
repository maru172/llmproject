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
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers)
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
        elements = driver.find_elements(By.CSS_SELECTOR, "header h1")
        return elements[0].text if elements else "No title"

    def news_author_date_time(driver, soup):
        author_name = soup.select_one(".text-sm.font-semibold") or soup.select_one(".caas-attr-item-author")
        date_time = soup.select_one("time") or \
                    soup.select_one('.caas-attr-meta time')

        return (author_name.text if author_name else "Unknown Author",
                date_time.text if date_time else "Unknown Date")

    @staticmethod
    def news_original_text(driver, soup):
        p_tags = soup.select('.caas-body p')  # 본문을 가져오기 위한 선택자
        if not p_tags:
            return "No content available"
        return ' '.join(p.get_text(strip=True) for p in p_tags)  # 본문 내용을 연결하여 반환

    def news_caption(driver, soup):
        caption_div = soup.select_one('figcaption div[style="max-height:none;overflow:visible"]')
        return caption_div.text.strip() if caption_div else "No caption"

    @staticmethod    
    def news_imageURL(self, soup):
        img_tag = soup.select_one('img[data-nimg="fill"][fetchpriority="high"]')
        return img_tag['src'] if img_tag and 'src' in img_tag.attrs else "No image"
    
    
    
    
if __name__ == "__main__":
    category = "Politics"  # 테스트할 카테고리 (Politics, World, Us 중 선택)
    
    # 드라이버 실행
    driver = CrawlingData.crawling_Setup()
    
    # 카테고리 페이지 접속
    driver = CrawlingData.category_set(driver, category)
    time.sleep(2)  # 페이지 로드 대기

    # 뉴스 목록 크롤링
    news_urls, news_titles, news_presses = CrawlingData.yahoo_news_home_page_urls(driver)
    
    if not news_urls:
        print("❌ 뉴스 URL을 찾을 수 없습니다.")
        driver.quit()
        exit()

    print(f"✅ 총 {len(news_urls)}개의 뉴스 기사 발견!")
    
    # 첫 번째 뉴스 기사 접속
    # first_news_url = news_urls[0]
    first_news_url = 'https://www.yahoo.com/news/look-history-greenland-viking-raiders-060712827.html'
    print(f"📰 첫 번째 뉴스 기사: {first_news_url}")
    
    # 뉴스 기사로 이동
    driver.get(first_news_url)
    time.sleep(2)  # 로드 대기

    # 뉴스 페이지 파싱
    soup = CrawlingData.bs_Setup(first_news_url)

    # 뉴스 제목 가져오기
    title = CrawlingData.news_title(driver)
    print(f"📌 뉴스 제목: {title}")

    # 기자명 & 날짜 가져오기
    author, date_time = CrawlingData.news_author_date_time(driver, soup)
    print(f"✍ 기자: {author}")
    print(f"🕒 날짜: {date_time}")

    # 본문 가져오기
    news_text = CrawlingData.news_original_text(driver, soup)
    print(f"📄 뉴스 본문: {news_text[:200]}...")  # 너무 길 경우 200자까지만 출력

    # 이미지 URL 가져오기
    news_image = CrawlingData.news_imageURL(driver, soup)
    print(f"🖼 이미지 URL: {news_image}")

    # 드라이버 종료
    driver.quit()
    

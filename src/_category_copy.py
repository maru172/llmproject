import logging
from _crawling_copy import CrawlingData
from _summary import Summary
from _excel import excel
from _captioning import Captioning
from _save_db import SaveDB
import os

import datetime

Bug_df = excel.Bug_excel_setup()
class News:
    @staticmethod
    def process_news_category(driver, df, category, sequence, prev_news):
        """
        특정 뉴스 카테고리를 크롤링하고, 요약 후 DB 및 엑셀에 저장하는 함수
        
        Args:
            driver: Selenium WebDriver
            df: pandas DataFrame (엑셀 저장용)
            category: 뉴스 카테고리 ('politics', 'world', 'US' 등)
            sequence: True면 모든 뉴스 크롤링, False면 새로운 뉴스만 크롤링
            prev_news: 이전에 크롤링한 뉴스 URL 리스트
        
        Returns:
            list: 이번 크롤링에서 가져온 뉴스 URL 목록
        """
        logging.info(f"Processing category: {category}")
        driver = CrawlingData.category_set(driver, category)
       
        if sequence:
            CrawlingData.scroll_down(driver, 200)
        
        main_page_urls, main_page_titles, main_page_press = CrawlingData.yahoo_news_home_page_urls(driver)
        
        # 새로운 뉴스가 없을 경우 종료
        if not sequence and main_page_urls == prev_news:
            print(f'새로운 {category} 뉴스 없음')
            return prev_news
        
        # 새로운 URL 필터링 (sequence=True이면 전체 크롤링)
        new_urls = main_page_urls if sequence else list(set(main_page_urls) - set(prev_news))
        total_urls = len(new_urls)  # 전체 URL 개수
        for i, url in enumerate(new_urls):
            try:
                remaining = total_urls - (i + 1)  # 남은 반복 횟수
                today = datetime.date.today().strftime("%m_%d")
                soup = CrawlingData.bs_Setup(url)
                _news_author, _news_date_time = CrawlingData.news_author_date_time(driver, soup)
                _news_caption = CrawlingData.news_caption(driver, soup)
                _news_original_text = CrawlingData.news_original_text(driver, soup)
                _news_summary = Summary.summary_Short(_news_original_text)
                _image_url = CrawlingData.news_imageURL(driver, soup)
                _generated_caption = Captioning.generate_caption(_image_url)
                
                folder_path = f"/home/llmproject/Desktop/Transformer/llmproject2/databases_date/{today}"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # 디버깅용 출력
                print("\n\n*****************************************************************")
                print(f"현재 url: {driver.current_url}")
                print(f"현재 처리 중: {i + 1}/{total_urls}, 남은 개수: {remaining}")
                # print(f"- url: {url}\n- press: {main_page_press[i]}\n- title: {main_page_titles[i]}")
                # print(f"- author: {_news_author}\n- date_time: {_news_date_time}\n- caption: {_news_caption}")
                # print(f"- original text: {_news_original_text}\n- summary: {_news_summary}")
                
                # SQLite 저장
                SaveDB.save_news_to_db(category, main_page_urls[i], main_page_titles[i], main_page_press[i], _news_author, _news_date_time,
                            _image_url, _news_original_text, _news_summary, _news_caption, _generated_caption,  
                            f"/home/llmproject/Desktop/Transformer/llmproject2/databases/{category}.db", category)
                
                SaveDB.save_news_to_db(category, main_page_urls[i], main_page_titles[i], main_page_press[i], _news_author, _news_date_time,
                            _image_url, _news_original_text, _news_summary, _news_caption, _generated_caption,  
                            f"{folder_path}/{category}.db", category)
                
                print("DB 저장 완료")

            except Exception as e:
                    print("\n\n*****************************************************************")
                    SaveDB.save_log_failed(f"{folder_path}/Bug.db",main_page_urls[i],e)
                    print(f"[오류 발생] {type(e).__name__}: {e}")

        return main_page_urls

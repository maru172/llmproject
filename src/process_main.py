from _crawling_copy import CrawlingData
from _category_copy import News
from _excel import excel
import time

US_df = excel.US_excel_setup()
Politics_df = excel.Politics_excel_setup()
World_df = excel.World_excel_setup()

# 이전 뉴스 URL 목록
US_pre_news = []
Politics_pre_news = []
World_pre_news = []

# 전역 변수로 WebDriver 선언
driver = None  

def init_driver():
    """WebDriver를 초기화하는 함수"""
    global driver
    if driver is not None:
        try:
            driver.quit()  # 기존 WebDriver 종료
        except:
            pass  # 드라이버가 이미 종료된 경우 예외 무시
    driver = CrawlingData.crawling_Setup()
    
def F_sequence():
    """첫 번째 크롤링 실행 (모든 뉴스 크롤링)"""
    print("US 뉴스 처리 중...")
    News.process_news_category(driver, US_df, "Us", True, '')
    print("정치 뉴스 처리 중...")
    News.process_news_category(driver, Politics_df, "Politics", True, '')
    print("세계 뉴스 처리 중...")
    News.process_news_category(driver, World_df, "World", True, '')

def S_sequence():
    global US_pre_news
    global Politics_pre_news
    global World_pre_news
   
    while True:
        try:
            print("US 뉴스 처리 중...")
            US_pre_news = News.process_news_category(driver, US_df, "Us", False, US_pre_news)
            print("정치 뉴스 처리 중...")
            Politics_pre_news = News.process_news_category(driver, Politics_df, "Politics", False, Politics_pre_news)
            print("세계 뉴스 처리 중...")
            World_pre_news = News.process_news_category(driver, World_df, "World", False, World_pre_news)

        except Exception as e:
            print(f"에러 발생: {e}")
            break  # 예외 발생 시 루프 종료

        
def main():
    global driver
    try:
        print('*** First Sequence Operation ***')
        F_sequence()
        
        print('*** Second Sequence Operation ***')
        S_sequence()
    except Exception as e:
            print(f"[오류 발생] {e}")   
            
if __name__ == "__main__":
    init_driver()  # 최초 WebDriver 초기화

    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("프로그램 종료 명령어 입력됨")
            break  # 키보드 인터럽트 시 종료
        except Exception as e:
            print(f"[오류 발생] {e}. 5초 후 재시도...")
            time.sleep(5)  # 5초 대기 후 다시 실행

    # 프로그램 종료 시 WebDriver 종료
    if driver is not None:
        driver.quit()
        print("WebDriver 종료. 프로그램 종료...")
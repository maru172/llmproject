import logging
import time
from _crawling import CrawlingData
from _category import News
from _excel import excel

# 로깅 설정
logging.basicConfig(
    filename="/home/llmproject/Desktop/Transformer/llmproject2/src_copy/news_crawler.log",  # 로그 파일 저장
    level=logging.INFO,  # INFO 이상의 로그를 기록
    format="%(asctime)s - %(levelname)s - %(message)s",  # 로그 형식
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 엑셀 데이터프레임 설정
US_df = excel.US_excel_setup()
Politics_df = excel.Politics_excel_setup()
World_df = excel.World_excel_setup()

# 이전 뉴스 URL 목록
US_pre_news, Politics_pre_news, World_pre_news = [], [], []

# 전역 WebDriver 선언
driver = None  

def init_driver():
    """WebDriver를 초기화하는 함수"""
    global driver
    if driver is not None:
        try:
            driver.quit()
            logging.info("기존 WebDriver 종료 완료")
        except Exception:
            logging.warning("WebDriver 종료 중 예외 발생, 무시하고 계속 진행")

    logging.info("새로운 WebDriver 초기화 중...")
    driver = CrawlingData.crawling_Setup()
    logging.info("WebDriver 초기화 완료")


def F_sequence():
    """첫 번째 크롤링 실행 (모든 뉴스 크롤링)"""
    for category, df in [("Us", US_df), ("Politics", Politics_df), ("World", World_df)]:
        logging.info(f"{category} 뉴스 크롤링 시작 (전체 크롤링)...")
        News.process_news_category(driver, df, category, True, '')
        logging.info(f"{category} 뉴스 크롤링 완료")


def S_sequence():
    """두 번째 크롤링 실행 (새로운 뉴스만 크롤링)"""
    global US_pre_news, Politics_pre_news, World_pre_news
    category_data = [
        ("Us", US_df, US_pre_news),
        ("Politics", Politics_df, Politics_pre_news),
        ("World", World_df, World_pre_news)
    ]

    while True:
        try:
            for category, df, prev_news in category_data:
                logging.info(f"{category} 뉴스 크롤링 시작 (새로운 뉴스 체크)...")
                new_news = News.process_news_category(driver, df, category, False, prev_news)
                
                if new_news == prev_news:
                    logging.info(f"{category} 새로운 뉴스 없음")
                else:
                    prev_news[:] = new_news
                    logging.info(f"{category} 새로운 뉴스 {len(new_news)}개 업데이트 완료")

        except Exception as e:
            logging.error(f"에러 발생: {e}", exc_info=True)
            break  # 예외 발생 시 루프 종료


def main():
    """크롤링 메인 실행 함수"""
    try:
        logging.info("=== First Sequence Operation 시작 ===")
        F_sequence()
        
        logging.info("=== Second Sequence Operation 시작 ===")
        S_sequence()
    except Exception as e:
        logging.error(f"메인 실행 중 오류 발생: {e}", exc_info=True)


if __name__ == "__main__":
    init_driver()  # 최초 WebDriver 초기화

    while True:
        try:
            main()
        except KeyboardInterrupt:
            logging.info("프로그램 종료 명령어 입력됨")
            break  # 키보드 인터럽트 시 종료
        except Exception as e:
            logging.error(f"[오류 발생] {e}. 5초 후 재시도...", exc_info=True)
            time.sleep(5)  # 5초 대기 후 다시 실행

    # 프로그램 종료 시 WebDriver 종료
    if driver is not None:
        driver.quit()
        logging.info("WebDriver 종료. 프로그램 종료...")

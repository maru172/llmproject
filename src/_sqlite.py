import sqlite3

def sqlite_save(category, url, title, press, author, date_time, image_url, original_text, summary, original_caption, generated_caption, file_path, sheet_name):
    try:
        # 카테고리별 데이터베이스 파일 경로 설정
        db_file_path = file_path

        # 데이터베이스에 연결
        con = sqlite3.connect(db_file_path)
        cursor = con.cursor()

        # 카테고리별 테이블 생성 (이미 존재하면 무시)
        table_name = f"{sheet_name}_articles"
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            category TEXT,
            url TEXT,
            title TEXT,
            press TEXT,
            author TEXT,
            date_time TEXT,
            image_url TEXT,
            original_text TEXT,
            summary TEXT,
            original_caption TEXT,
            generated_caption TEXT
        )
        ''')

        # 데이터 삽입 쿼리 실행 (id 칼럼은 자동 증가)
        cursor.execute(f'''
        INSERT INTO {table_name} (category, url, title, press, author, date_time, image_url, original_text, summary, original_caption, generated_caption)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (category, url, title, press, author, date_time, image_url, original_text, summary, original_caption, generated_caption))  
        
        # 마지막 삽입된 ID 가져오기
        last_id = cursor.lastrowid
        print("The last inserted row id:", last_id)

        # 변경사항 저장
        con.commit()
        
    except sqlite3.Error as error:
        # 오류 발생 시 메시지 출력
        print("데이터 삽입 중 오류 발생:", error)
    finally:
        # 데이터베이스 연결 종료
        if con:
            con.close()
    return last_id


# 변수에 값을 할당하고 함수 호출
# url = "www.news.com/1/1"
# title = "테스트용 뉴스"
# article = "테스트를 하기 위한 뉴스의 본문"
# summary = "테하위뉴본"
# sqlite_save(url, title, article, summary)
# print("완료")
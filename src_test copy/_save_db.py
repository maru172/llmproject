import sqlite3

class SaveDB:
    @staticmethod
    def save_news_to_db(category, url, title, press, author, date_time, image_url, original_text, summary, original_caption, generated_caption, file_path, sheet_name):
        last_id = None  # 기본값 설정
        try:
            db_file_path = file_path  # 데이터베이스 파일 경로

            with sqlite3.connect(db_file_path) as con:
                cursor = con.cursor()
                table_name = f"{sheet_name}_articles"

                # 테이블 생성 (존재하지 않으면 생성)
                cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                )''')

                # 데이터 삽입
                cursor.execute(f'''
                INSERT INTO {table_name} (category, url, title, press, author, date_time, image_url, original_text, summary, original_caption, generated_caption)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (category, url, title, press, author, date_time, image_url, original_text, summary, original_caption, generated_caption))  
                
                last_id = cursor.lastrowid  # 마지막 삽입된 ID 저장
                con.commit()
        
        except sqlite3.Error as error:
            print("데이터 삽입 중 오류 발생:", error)
        
        return last_id

    @staticmethod
    def save_log_failed(file_path, url, error_message):
        """
        오류난 기사의 URL과 에러 메시지를 DB에 저장하는 함수
        
        Args:
            file_path (str): SQLite 데이터베이스 파일 경로
            url (str): 오류난 뉴스 기사 URL
            error_message (str): 발생한 에러 메시지
        """
        try:
            with sqlite3.connect(file_path) as con:
                cursor = con.cursor()

                # 오류 기록 테이블 생성 (존재하지 않으면 생성)
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS failed_articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    error_message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')

                # 오류 데이터 삽입
                cursor.execute('''
                INSERT INTO failed_articles (url, error_message)
                VALUES (?, ?)''', (url, error_message))

                con.commit()

        except sqlite3.Error as error:
            print("오류 데이터를 삽입하는 중 오류 발생:", error)
